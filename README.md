# malaysia-airport-insight

# Data Ingestion
Run command below in SQL shell to create table and import data into PostgreSQL: <br>
_Note: Replace path-to-sql-script with full file path where table_setup.sql is stored_
```
\i 'path-to-sql-script/table_setup.sql'
```

### Explanation for table_setup.sql
1. To handle foreign characters (e.g. airport name), character set is changed to ```utf8```:
```
SET CLIENT_ENCODING TO 'utf8';
```
2. To create table, data description is referred [here](https://openflights.org/data.html).
3. To import data directly from public website ([airport DB](https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat)): 
	* ```wget``` command is used ([guide to install wget](https://www.jcchouinard.com/wget/))
	* To parse data in correct format, select data format to read in as csv by specifying the option ```FORMAT csv```
	* To match null characters present in data, set null string to ```\N``` (default for CSV format is unquoted empty string) by specifying the option ```NULL '\N'```
```
COPY airport FROM PROGRAM 'wget -q -O - https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat' WITH (FORMAT csv, NULL '\N');
```

# Data Analysis
## Analysis 1 - Number of Airports in Malaysia
To determine how many airports there are in Malaysia, run:
```
SELECT COUNT(Name) AS "NUMBER OF AIRPORTS IN MALAYSIA"
FROM airport
WHERE UPPER(Country) = 'MALAYSIA';
```
Result: <br>
![Analysis 1 Result](/result_screenshot/Output%20(airports%20num%20in%20MY).png)

## Analysis 2 - Distance between Airports in Malaysia
### Prepare Location Information
1. Install PostGIS to support geographic objects ([guide to install PostGIS](https://postgis.net/workshops/postgis-intro/installation.html)).
2. To use PostGIS, create a new column, and store longitude and latitude into points, run: <br>
_Note: Replace path-to-sql-script with full file path where add_geolocation.sql is stored_
```
\i 'path-to-sql-script/add_geolocation.sql'
```

### Calculate Distance between Airports
To calculate distance between airports in Malaysia, run:
```
WITH my_airport AS (
	SELECT Airport_id, Name, Geolocation
	FROM airport 
	WHERE UPPER(Country) = 'MALAYSIA'
)

, airport_pair AS (
	SELECT a1.Name AS Airport_1, a1.Geolocation AS Location_1, a2.Name AS Airport_2, a2.Geolocation AS Location_2
	FROM my_airport a1
	JOIN my_airport a2 ON a2.Airport_id > a1.Airport_id
)

SELECT Airport_1, Airport_2, ROUND((ST_Distance(Location_1, Location_2) / 1000)::numeric, 2) AS "Distance (KM)"
FROM airport_pair
ORDER BY Airport_1, Airport_2;
```

Result (partial, total rows = 780):
<p>
  <img src="result_screenshot/Output%20(airports%20distance)%20-partial.png" height="500">
</p>

### Explanation
1. Create 2 temporary tables using ```WITH``` statement:
	* my_airport: select all airports in Malaysia with location information
	* airport_pair: generate pair of airports without duplicate by self join with rows having larger id
2. ```ST_Distance``` function takes in two points and returns distance between the points in metres.
3. To use the ```ROUND``` function (only usable on numeric for PostgreSQL), type cast ```::numeric``` is used to convert the result to numeric. 

### References
[Geolocations Using PostGIS](https://www.youtube.com/watch?v=mFc-gGJLRE0) <br>
[PostGIS Documentation](http://postgis.net/workshops/postgis-intro/geography.html)

## Analysis 3 - Airport Traffic in Malaysia
Coming soon!
