CREATE TABLE actors (
    actor_id TEXT PRIMARY KEY,          -- Custom ID like 'a1', 'a2', etc.
    actor TEXT NOT NULL,
    title TEXT NOT NULL,
    type TEXT NOT NULL,
    rating TEXT
);

CREATE TABLE countries (
    country_id TEXT PRIMARY KEY,        -- Custom ID like 'cn1', 'cn2', etc.
    country TEXT NOT NULL,
    title TEXT NOT NULL,
    rating TEXT
);

CREATE TABLE category (
    category_id TEXT PRIMARY KEY,       -- Custom ID like 'ct1', 'ct2', etc.
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    type TEXT NOT NULL,
    duration TEXT
);

CREATE TABLE directors (
    director_id TEXT PRIMARY KEY,       -- Custom ID like 'd1', 'd2', etc.
    title TEXT NOT NULL,
    director TEXT NOT NULL,
    category TEXT,
    type TEXT,
    duration TEXT
);
