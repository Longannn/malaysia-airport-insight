SET CLIENT_ENCODING TO 'utf8';

CREATE TABLE IF NOT EXISTS airport(
	Airport_ID INT,
	Name VARCHAR(100),
	City VARCHAR(50),
	Country VARCHAR(50),
	IATA CHAR(3),
	ICAO CHAR(4),
	Latitude FLOAT,
	Longitude FLOAT,
	Altitude INT,
	Timezone NUMERIC, 
	DST CHAR(1),
	Tz_database_timezone VARCHAR(50),
	Type CHAR(7),
	Source CHAR(11)
);

COPY airport FROM PROGRAM 'wget -q -O - https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat' WITH (FORMAT csv, NULL '\N');