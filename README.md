# malaysia-airport-insight

# Data Ingestion
Run command below in SQL shell to create table and import data into PostgreSQL. <br>
_(Replace path-to-sql-script with full file path)_
```
\i 'path-to-sql-script/table_setup.sql'
```

Details of table_setup.sql
1. To handle foreign characters (e.g. airport name), character set is changed to 'utf8':
```
SET CLIENT_ENCODING TO 'utf8';
```
2. To create table, data description is referred [here](https://openflights.org/data.html).
3. To import data directly from public website ([airport DB](https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat)): 
    * **wget** command is used ([guide to install wget](https://www.jcchouinard.com/wget/))
    * To parse data in correct format, select data format to read in as csv by specifying the option **FORMAT csv**
    * To match null characters present in data, set null string to **\N** (default for CSV format is unquoted empty string) by specifying the option **NULL '\N'**
```
COPY airport FROM PROGRAM 'wget -q -O - https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat' WITH (FORMAT csv, NULL '\N');
```
