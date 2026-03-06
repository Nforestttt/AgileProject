import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QPoint

from pages.LoginWindows import LoginWindow
from pages.MainWindows import MainWindow


class AppWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.stack = QStackedWidget()

        self.login_page = LoginWindow()
        self.main_page = MainWindow()

        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.main_page)

        self.setCentralWidget(self.stack)

        self.login_page.login_success.connect(self.slide_to_main)

    def slide_to_main(self):

        current_index = self.stack.currentIndex()
        next_index = 1

        current_widget = self.stack.widget(current_index)
        next_widget = self.stack.widget(next_index)

        width = self.stack.frameRect().width()

        next_widget.move(width, 0)
        next_widget.show()

        # 当前页面滑出
        self.anim1 = QPropertyAnimation(current_widget, b"pos")
        self.anim1.setDuration(400)
        self.anim1.setStartValue(QPoint(0, 0))
        self.anim1.setEndValue(QPoint(-width, 0))
        self.anim1.setEasingCurve(QEasingCurve.InOutCubic)

        # 新页面滑入
        self.anim2 = QPropertyAnimation(next_widget, b"pos")
        self.anim2.setDuration(400)
        self.anim2.setStartValue(QPoint(width, 0))
        self.anim2.setEndValue(QPoint(0, 0))
        self.anim2.setEasingCurve(QEasingCurve.InOutCubic)

        self.anim1.start()
        self.anim2.start()

        self.stack.setCurrentIndex(next_index)


app = QApplication(sys.argv)

window = AppWindow()
window.resize(1000, 700)
window.show()

sys.exit(app.exec())