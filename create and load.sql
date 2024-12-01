INSERT INTO actors (actor_id, actor, title, type, rating)
SELECT 
    CONCAT('a', ROW_NUMBER() OVER (ORDER BY actor)) AS actor_id,
    actor,
    title,
    type,
    rating
FROM (
    SELECT DISTINCT 
        UNNEST(STRING_TO_ARRAY(actor, ', ')) AS actor,
        title,
        type,
        rating
    FROM shows
    WHERE actor IS NOT NULL
) subquery;

INSERT INTO countries (country_id, country, title, rating)
SELECT 
    CONCAT('cn', ROW_NUMBER() OVER (ORDER BY country_split)) AS country_id, -- Custom IDs like 'cn1'
    country_split AS country,                                              -- Split country
    title,                                                                 -- Title of the show
    rating                                                                 -- Rating of the show
FROM (
    SELECT 
        title,
        UNNEST(STRING_TO_ARRAY(country, ', ')) AS country_split, -- Split countries into rows
        rating
    FROM shows
    WHERE country IS NOT NULL -- Exclude rows with NULL countries
) subquery;


INSERT INTO category (category_id, category, title, type, duration)
SELECT 
    CONCAT('ct', ROW_NUMBER() OVER (ORDER BY category_split)) AS category_id, -- Custom IDs like 'ct1'
    category_split AS category,                                              -- Individual category
    title,                                                                   -- Title of the show
    type,                                                                    -- Type (Movie/TV Show)
    duration                                                                 -- Duration
FROM (
    SELECT 
        title,
        UNNEST(STRING_TO_ARRAY(category, ', ')) AS category_split, -- Split categories into rows
        type,
        duration
    FROM shows
    WHERE category IS NOT NULL -- Avoid rows with NULL categories
) subquery;


INSERT INTO directors (director_id, title, director, category, type, duration)
SELECT 
    CONCAT('d', ROW_NUMBER() OVER (ORDER BY director_split)) AS director_id, -- Generate custom IDs like 'd1'
    title,                                                                  -- Retain the title
    director_split AS director,                                             -- Individual director
    category,                                                               -- Retain the category
    type,                                                                   -- Retain the type
    duration                                                                -- Retain the duration
FROM (
    SELECT 
        title,
        UNNEST(STRING_TO_ARRAY(director, ', ')) AS director_split,          -- Split directors into rows
        category,
        type,
        duration
    FROM shows
    WHERE director IS NOT NULL -- Exclude rows with NULL directors
) subquery;

ALTER TABLE shows ADD COLUMN country_id TEXT;  -- For referencing countries
ALTER TABLE shows ADD COLUMN director_id TEXT; -- For referencing directors
ALTER TABLE shows ADD COLUMN actor_id TEXT;    -- For referencing actors
ALTER TABLE shows ADD COLUMN category_id TEXT; -- For referencing category

-- Link country_id to countries table
ALTER TABLE shows ADD CONSTRAINT fk_country
FOREIGN KEY (country_id) REFERENCES countries(country_id);

-- Link director_id to directors table
ALTER TABLE shows ADD CONSTRAINT fk_director
FOREIGN KEY (director_id) REFERENCES directors(director_id);

-- Link actor_id to actors table
ALTER TABLE shows ADD CONSTRAINT fk_actor
FOREIGN KEY (actor_id) REFERENCES actors(actor_id);

-- Link category_id to category table
ALTER TABLE shows ADD CONSTRAINT fk_category
FOREIGN KEY (category_id) REFERENCES category(category_id);

UPDATE shows
SET country_id = countries.country_id
FROM countries
WHERE shows.title = countries.title;

UPDATE shows
SET director_id = directors.director_id
FROM directors
WHERE shows.title = directors.title;

UPDATE shows
SET actor_id = actors.actor_id
FROM actors
WHERE shows.title = actors.title;

UPDATE shows
SET category_id = category.category_id
FROM category
WHERE shows.title = category.title;



