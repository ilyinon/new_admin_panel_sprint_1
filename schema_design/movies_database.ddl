CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE SCHEMA IF NOT EXISTS content;

SET search_path TO content,public;

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date timestamp with time zone,
    certificate TEXT,
    file_path TEXT,
    rating FLOAT CHECK ( rating >= 0 AND rating <= 100),
    type TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
); 

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    person_id uuid NOT NULL REFERENCES content.person (id) ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    created timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    genre_id uuid NOT NULL REFERENCES content.genre (id) ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    created timestamp with time zone
);

CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS genre_name_idx ON content.genre (name);

CREATE INDEX CONCURRENTLY IF NOT EXISTS  film_work_creation_date_idx ON content.film_work(creation_date);
CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS film_work_person_idx ON content.person_film_work (film_work_id, person_id, role);
CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS film_work_genre_idx ON content.genre_film_work( film_work_id, genre_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS genre_film_work_film_work_idx ON content.genre_film_work( film_work_id);