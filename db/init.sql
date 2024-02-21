CREATE DATABASE IF NOT EXISTS quotes;
USE quotes;

CREATE TABLE IF NOT EXISTS quotes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    quote TEXT NOT NULL,
    author VARCHAR(255) NOT NULL
);

INSERT INTO quotes (quote, author)
VALUES ('Life is 10% what happens to us and 90% how we react to it.', 'Charles R. Swindoll');

