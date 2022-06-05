CREATE TABLE IF NOT EXISTS houses (
    id SERIAL,
    ad_id INT NOT NULL,
    PRIMARY KEY(ad_id),
    ad_name VARCHAR,
    price INT,
    adress_title VARCHAR,
    country VARCHAR,
    region VARCHAR,
    city VARCHAR,
    street VARCHAR,
    house_num VARCHAR,
    rooms INT,
    owners_name VARCHAR,
    url TEXT,
    added_date TIMESTAMP
);

CREATE TABLE IF NOT EXISTS photos(
    id SERIAL,
    PRIMARY KEY(id),
    ad_id INT NOT NULL,
    photo_url TEXT,
    FOREIGN KEY(ad_id) REFERENCES houses(ad_id)
);

CREATE TABLE IF NOT EXISTS maps (
  id SERIAL,
  PRIMARY KEY(id),
  ad_id INT,
  lat NUMERIC(10, 8),
  lon NUMERIC(10, 8),
  zoom INT,
  FOREIGN KEY(ad_id) REFERENCES houses (ad_id)
);

