-- Initialize the database.
-- Drop any existing data and create empty tables.
-- .mode column
-- .header on
DROP TABLE IF EXISTS word;
DROP TABLE IF EXISTS category;

CREATE TABLE word(category, word, count);
CREATE TABLE category(category, count);