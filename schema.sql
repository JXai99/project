CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    hash TEXT NOT NULL
);
CREATE UNIQUE INDEX username ON users (username);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    matchday TEXT NOT NULL,
    home_team TEXT NOT NULL,
    away_team TEXT NOT NULL,
    home_score INTEGER,
    away_score INTEGER
);
