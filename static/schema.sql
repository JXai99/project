CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL
);
'DROP TABLE IF EXISTS scores;'

CREATE TABLE scores (
    id SERIAL PRIMARY KEY,

    api_match_id INTEGER UNIQUE NOT NULL,

    season INTEGER NOT NULL,
    matchday INTEGER NOT NULL,

    utc_date TIMESTAMP NOT NULL,

    home_team TEXT NOT NULL,
    home_short_name TEXT NOT NULL,
    home_team_id INTEGER NOT NULL,

    away_team TEXT NOT NULL,
    away_short_name TEXT NOT NULL,
    away_team_id INTEGER NOT NULL,

    home_score INTEGER,
    away_score INTEGER,

    winner TEXT,
    status TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
