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
