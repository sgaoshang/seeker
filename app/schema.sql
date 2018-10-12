-- Initialize the database.
-- Drop any existing data and create empty tables.

-- DROP TABLE IF EXISTS user;

-- CREATE TABLE cases_search_date (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   search_date CHAR(10) NOT NULL,
--   component TEXT UNIQUE NOT NULL
-- );

-- 1|test|test@redhat.com|pbkdf2:sha256:50000$V9zHqcBm$18135b6fc003868a9540c9b81260f10e37e3c5110e551ce637e0076297dbc7ca|virt-who||2018-10-12 07:04:47.064705
-- INSERT INTO user (username, password_hash)
-- VALUES
--   ('test', 'pbkdf2:sha256:50000$YzoYuhUW$562e6f306f6cb9660a995affdaf6e1c5c7cfb2e21d58feef875c5d706b73752e');

--  INSERT INTO user (username, email, password_hash, last_component)
--  VALUES
--    ('test', 'test@redhat.com', 'pbkdf2:sha256:50000$YzoYuhUW$562e6f306f6cb9660a995affdaf6e1c5c7cfb2e21d58feef875c5d706b73752e', 'virt-who');

INSERT INTO component
VALUES 
  (1, 'virt-who', '2018-10-05'),
  (2, 'rhsm', '2018-10-05');

-- INSERT INTO cases
-- VALUES
--   ('01931212', 1, 1,'2017-09-01','RHEL7-99882','1308544',1,'virt-who'),
--   ('01931222', 1, 1,'2017-09-02','RHEL7-99882','1308544',1,'virt-who'),
--   ('01931232', 1, 1,'2017-09-03','RHEL7-99882','1308544',1,'virt-who'),
--   ('01931242', 1, 1,'2017-09-04','RHEL7-99882','1308544',1,'virt-who'),
--   ('01931252', 1, 1,'2017-09-05','RHEL7-99882','1308544',1,'virt-who'),
--   ('01931262', 1, 1,'2017-09-06','RHEL7-99882','1308544',1,'virt-who'),
--   ('01931272', 1, 1,'2017-09-07','RHEL7-99882','1308544',1,'virt-who'),
--   ('01931282', 1, 1,'2017-09-08','RHEL7-99882','1308544',1,'virt-who'),
--   ('01931292', 1, 1,'2017-09-09','RHEL7-99882','1308544',1,'virt-who'),
--   ('02931212', 1, 1,'2017-09-10','RHEL7-99882','1308544',1,'virt-who'),
--   ('03931212', 1, 1,'2017-09-11','RHEL7-99882','1308544',1,'virt-who'),
--   ('04931277', 1, 1,'2017-09-12','RHEL7-99882','1308544',1,'virt-who'),
--   ('05931212', 1, 1,'2017-09-13','RHEL7-99882','1308544',1,'virt-who'),
--   ('06931212', 1, 1,'2017-09-14','RHEL7-99882','1308544',1,'virt-who'),
--   ('07931222', 1, 1,'2017-09-02','RHEL7-99882','1308544',1,'virt-who');