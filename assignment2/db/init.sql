CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS tasks;
CREATE TABLE tasks (
    id VARCHAR(255),
    title VARCHAR(255),
    is_completed BOOLEAN,
    notify VARCHAR(255),
    PRIMARY KEY (id)
);