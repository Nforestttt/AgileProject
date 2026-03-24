2026/03/10 | Project requirement analysis and table structure design | Completed | Confirmed core tables: t_cambridge_test (test paper table) and t_cambridge_section (section detail table)
2026/03/10 | Create t_cambridge_test main table | Completed | Includes fields such as test_id, test_name, create_time; set auto-increment primary key

2026/03/11 | Create t_cambridge_section detail table | Completed | Includes fields such as section_id, test_id, audio/image path, answer JSON, and foreign key constraints

2026/03/11 | Configure table association relationship | Completed | section.test_id is associated with test.test_id, supporting cascade update/delete

2026/03/12 | Import Test1 basic data | Completed | Entered audio, images, titles, and standard answer JSON for 4 sections

2026/03/13 | Server audio path configuration | Completed | Configured static resource access for port 7777 and generated playable URLs

2026/03/14 | Batch generate initial data for Test2~Test4 | Completed | Generated audio/image paths according to rules; set name and answers to null

2026/03/14 | Write batch insert SQL scripts | Completed | Adapted to table structure; section_no uses numeric format; null values are uniformly set to 'null'

2026/03/16 | Create multi-table join view | Completed | Established section_view to associate test paper and section tables for unified query

2026/03/16 | Database structure verification and optimization | Completed | Verified unique constraints, foreign keys, and field lengths to ensure data integrity

2026/03/17 | finish all data input

2026/03/18 | modify data and test the server

2026/03/20	Insert English listening materials in batches. Sort and import listening materials corresponding to Test1~Test4; verify data integrity and association relations

2026/03/21	Organize new Cambridge materials data. Standardize audio, images, answers and paths; complete null fields for Test1~Test4

2026/03/23	Insert new Cambridge materials data. Execute batch SQL import; verify resource validity and data constraints

2026/03/24	Full database data verification. Check test data, words, resources and constraints; fix abnormal data

2026/03/25	Backup local database and resources. Export full SQL dump and package static resources (audio/images)

2026/03/26	Upload static resources to server. Upload audio and image files to server port 7777 directory; test resource access

2026/03/27	Import database to remote server. Execute SQL script on server; configure foreign keys and cascade rules