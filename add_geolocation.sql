CREATE EXTENSION IF NOT EXISTS POSTGIS;

ALTER TABLE airport ADD COLUMN Geolocation GEOGRAPHY(POINT);

UPDATE airport SET Geolocation = ST_MakePoint(Longitude, Latitude);