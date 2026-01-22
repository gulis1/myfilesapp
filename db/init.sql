CREATE TABLE users (
  username TEXT PRIMARY KEY,
  password TEXT NOT NULL
);

INSERT INTO users (username, password) VALUES
  ('alice', '123'),
  ('bob', '123');

