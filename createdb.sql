CREATE TABLE IF NOT EXISTS houses (
    id SERIAL,
    ad_id INT NOT NULL,
    PRIMARY KEY(ad_id),
    type VARCHAR(255),
    ad_name VARCHAR(255),
    price INT,
    address_title VARCHAR(255),
    country VARCHAR(255),
    region VARCHAR(255),
    city VARCHAR(255),
    street VARCHAR(255),
    house_num VARCHAR(255),
    rooms INT,
    owners_name VARCHAR(255),
    url TEXT,
    added_date TIMESTAMP
);

CREATE TABLE IF NOT EXISTS photos(
    id SERIAL,
    PRIMARY KEY(id),
    ad_id INT NOT NULL,
    photo_url TEXT UNIQUE,
    FOREIGN KEY(ad_id) REFERENCES houses(ad_id)
);

CREATE TABLE IF NOT EXISTS map_data (
  id SERIAL,
  PRIMARY KEY(id),
  ad_id INT,
  lat NUMERIC(10, 8),
  lon NUMERIC(10, 8),
  zoom INT,
  FOREIGN KEY(ad_id) REFERENCES houses (ad_id)
);

CREATE TABLE IF NOT EXISTS sent_messages (
    id SERIAL,
    PRIMARY KEY(id),
    user_id INT,
    ad_id INT,
    username VARCHAR(255)
);

