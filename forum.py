# forum.py
# 纯函数版 - 只包含论坛核心业务逻辑，不依赖任何 web 框架
# 使用方式：由 Qt 前端或其他 Python 代码调用这些函数，并传入 sqlalchemy 的 session

from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from datetime import datetime

# 假设的模型（你项目里已有的，不要重复定义，这里只是类型提示用）
# from models import Post, Reply, PostLike, ReplyLike


def get_posts(db: Session, page: int = 1, page_size: int = 20) -> Dict:
    """
    分页获取所有帖子列表（最新帖在前）
    返回格式示例：
    {
        "total": 168,
        "page": 1,
        "page_size": 20,
        "posts": [
            {"id": 15, "title": "...", "author": "...", "time": "...", "reply_count": 7, "likes": 12},
            ...
        ]
    }
    """
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 20

    offset = (page - 1) * page_size

    total = db.query(func.count(Post.id)).scalar() or 0

    posts = (
        db.query(Post)
        .order_by(desc(Post.created_at))
        .offset(offset)
        .limit(page_size)
        .all()
    )

    result_posts = []
    for p in posts:
        result_posts.append({
            "id": p.id,
            "title": p.title,
            "author": p.username,          # 看user用户表
            "time": p.created_at.strftime("%Y-%m-%d"),
            "reply_count": p.reply_count,
            "likes": p.likes_count
        })

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "posts": result_posts
    }


def get_post_detail(db: Session, post_id: int) -> Optional[Dict]:
    """
    获取单个帖子详细信息
    返回示例：
    {"id":1, "title":"项目课", "author":"Alice", "time":"2026-03-10", "content":"大家有什推荐的资源？","likes":3}
    或 None（不存在）
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return None

    return {
        "id": post.id,
        "title": post.title,
        "author": post.username,
        "time": post.created_at.strftime("%Y-%m-%d"),
        "content": post.content,
        "likes": post.likes_count
    }


def get_replies(db: Session, post_id: int) -> List[Dict]:
    """
    获取某个帖子的所有回复
    返回示例：
    [
        {"author":"Bob", "content":"不错", "likes":2},
        {"author":"Cindy", "content":"我推荐TED", "likes":1}
    ]
    """

    if not db.query(Post).filter(Post.id == post_id).first():
         return []

    replies = (
        db.query(Reply)
        .filter(Reply.post_id == post_id)
        .order_by(Reply.created_at)
        .all()
    )

    result = []
    for r in replies:
        result.append({
            "author": r.username,
            "content": r.content,
            "likes": r.likes_count,
            "time": r.created_at.strftime("%Y-%m-%d %H:%M")
        })
    return result


def create_post(db: Session, title: str, content: str, user_id: int, username: str = None) -> Dict:
    """
    创建帖子
    返回示例：{"status": "ok", "post_id": 123} 或 {"status": "error", "message": "..."}
    """
    if not title or not title.strip():
        return {"status": "error", "message": "标题不能为空"}
    if not content or not content.strip():
        return {"status": "error", "message": "内容不能为空"}

    # 如果前端没传 username，这里可以简单生成或从用户表查
    if username is None:
        username = f"user_{user_id}"

    post = Post(
        title=title.strip(),
        content=content.strip(),
        user_id=user_id,
        username=username,
        likes_count=0,
        reply_count=0,
        created_at=datetime.now()
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    return {"status": "ok", "post_id": post.id}


def reply_post(db: Session, post_id: int, content: str, user_id: int, username: str = None) -> Dict:
    """
    回复帖子
    返回示例：{"status": "ok"} 或 {"status": "error", "message": "..."}
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return {"status": "error", "message": "Post not found"}

    if not content or not content.strip():
        return {"status": "error", "message": "Reply cannot be empty"}

    if username is None:
        username = f"user_{user_id}"

    reply = Reply(
        post_id=post_id,
        user_id=user_id,
        username=username,
        content=content.strip(),
        likes_count=0,
        created_at=datetime.now()
    )

    db.add(reply)
    post.reply_count += 1
    db.commit()

    return {"status": "ok"}


def like_post(db: Session, post_id: int, user_id: int) -> Dict:
    """
    点赞/取消点赞 帖子
    返回示例：{"status": "ok", "action": "liked"/"unliked", "likes": 5}
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return {"status": "error", "message": "Post not found"}

    like_record = db.query(PostLike).filter(
        PostLike.post_id == post_id,
        PostLike.user_id == user_id
    ).first()

    if like_record:
        # 取消点赞
        db.delete(like_record)
        post.likes_count = max(0, post.likes_count - 1)
        action = "unliked"
    else:
        # 点赞
        db.add(PostLike(post_id=post_id, user_id=user_id))
        post.likes_count += 1
        action = "liked"

    db.commit()
    return {"status": "ok", "action": action, "likes": post.likes_count}


def like_reply(db: Session, reply_id: int, user_id: int) -> Dict:
    """
    点赞/取消点赞 回复
    返回示例同上
    """
    reply = db.query(Reply).filter(Reply.id == reply_id).first()
    if not reply:
        return {"status": "error", "message": "Reply not found"}

    like_record = db.query(ReplyLike).filter(
        ReplyLike.reply_id == reply_id,
        ReplyLike.user_id == user_id
    ).first()

    if like_record:
        db.delete(like_record)
        reply.likes_count = max(0, reply.likes_count - 1)
        action = "unliked"
    else:
        db.add(ReplyLike(reply_id=reply_id, user_id=user_id))
        reply.likes_count += 1
        action = "liked"

    db.commit()
    return {"status": "ok", "action": action, "likes": reply.likes_count}


def search_posts(db: Session, keyword: str, page: int = 1, page_size: int = 20) -> Dict:
    """
    搜索帖子（标题包含关键词）
    返回格式：
    {
        "total": 25,
        "posts": [
            {"id":3, "title":"如何提高雅思听力", "author":"Alice", "time":"2026-03-10", "reply_count":4, "likes":2},
            ...
        ]
    }
    """
    if not keyword or not keyword.strip():
        return {"total": 0, "posts": []}

    if page < 1:
        page = 1
    offset = (page - 1) * page_size

    query = db.query(Post).filter(Post.title.ilike(f"%{keyword.strip()}%"))

    total = query.count()

    posts = (
        query.order_by(desc(Post.created_at))
        .offset(offset)
        .limit(page_size)
        .all()
    )

    result_posts = []
    for p in posts:
        result_posts.append({
            "id": p.id,
            "title": p.title,
            "author": p.username,
            "time": p.created_at.strftime("%Y-%m-%d"),
            "reply_count": p.reply_count,
            "likes": p.likes_count
        })

    return {
        "total": total,
        "posts": result_posts
    }