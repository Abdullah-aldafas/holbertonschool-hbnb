-- HBnB schema (PostgreSQL)

CREATE TABLE IF NOT EXISTS users (
  id CHAR(36) PRIMARY KEY,
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  email VARCHAR(255) UNIQUE,
  password VARCHAR(255),
  is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS places (
  id CHAR(36) PRIMARY KEY,
  title VARCHAR(255),
  description TEXT,
  price DECIMAL(10,2),
  latitude FLOAT,
  longitude FLOAT,
  owner_id CHAR(36) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS amenities (
  id CHAR(36) PRIMARY KEY,
  name VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS reviews (
  id CHAR(36) PRIMARY KEY,
  text TEXT,
  rating INT CHECK (rating BETWEEN 1 AND 5),
  user_id CHAR(36) REFERENCES users(id),
  place_id CHAR(36) REFERENCES places(id),
  CONSTRAINT uq_review_once UNIQUE (user_id, place_id)
);

CREATE TABLE IF NOT EXISTS place_amenity (
  place_id CHAR(36) REFERENCES places(id),
  amenity_id CHAR(36) REFERENCES amenities(id),
  PRIMARY KEY (place_id, amenity_id)
);


