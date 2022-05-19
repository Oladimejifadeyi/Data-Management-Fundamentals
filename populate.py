#Import modules
import mysql.connector 
import csv 
import sys 
from datetime import datetime 

try:
    # set the user and passoword
    # connect to mySql connector
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        port = "3306"
    ) 
    cur = db.cursor() 

#check if database exist if yes drop database abd recreate database so that we have a fresh database
    cur.execute("DROP DATABASE IF EXISTS `pollution-db2`")
    cur.execute("CREATE DATABASE `pollution-db2`") 

#create an empty list
    data = []; 

# read csv file and append row to the list data and drop header

    with open('clean.csv', 'r') as csv_file: 
        reader = csv.reader(csv_file, delimiter = ',')
        next(reader)
        for row in reader: 
            data.append(row) 
      
# get database
    cur.execute("USE `pollution-db2`") 

# create station table
    stations_sql = """CREATE TABLE `stations`
            (`stationid` INT(11) NOT NULL UNIQUE,
            `location` VARCHAR(50) NOT NULL UNIQUE,
            `geo_point_2d` VARCHAR(55) NOT NULL,
            PRIMARY KEY(`stationid`));""" 

# create readings table
    readings_sql = """CREATE TABLE `readings`
        (`readingid` INT(11) NOT NULL AUTO_INCREMENT,
        `datetime` DATETIME NOT NULL,
        `nox` FLOAT,
        `no2` FLOAT,
        `no` FLOAT,
        `pm10` FLOAT,
        `nvpm10` FLOAT,
        `vpm10` FLOAT,
        `nvpm2.5` FLOAT,
        `pm2.5` FLOAT,
        `vpm2.5` FLOAT,
        `co` FLOAT,
        `o3` FLOAT,
        `so2` FLOAT, 
        `temperature` REAL,
        `rh` INT(11),
        `airpressure` INT(11),
        `datestart` DATETIME,
        `date_end` DATETIME,
        `current` TEXT(5),
        `instrument_type`VARCHAR(35),
        `station_id-fk` INT,
        PRIMARY KEY (`readingid`));""" 

    schema_sql = """CREATE TABLE `schema`
            (`measure` VARCHAR(15) NOT NULL UNIQUE,
            `description` VARCHAR(50) NOT NULL,
            `unit` VARCHAR(25) NOT NULL,
            PRIMARY KEY(`measure`));"""

    # execute tables
    cur.execute(stations_sql)
    cur.execute(readings_sql) 
    cur.execute(schema_sql)

    # add relationship
    cur.execute("ALTER TABLE readings ADD FOREIGN KEY (`station_id-fk`) REFERENCES stations(stationid);") 

    for row in data:
    #set the autocommit flag to false
        db.autocommit = False 

    # insert station

        stations_sql = "INSERT IGNORE INTO stations values(%s, %s, %s)"
        station_values = (row[4], row[17], row[18]) 

        cur.execute(stations_sql, station_values) 
    
    # get station id using SQL since using INSERT IGNORE above
        cur.execute("SELECT * FROM stations WHERE stationid = %s", (row[4],)) 
        stationid = cur.fetchone()[0]  

    #insert readings
        readings_sql =  """INSERT IGNORE INTO readings values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
        reading_values = ("", row[0], row[1], row[2], row[3], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[19], row[20], row[21], row[22], stationid) 
        
        cur.execute(readings_sql, reading_values)  

        #readings_sql = readings_sql.replace("''", "NULL")  

    # manually insert schema values 
    schema_sql = """INSERT IGNORE INTO `schema` VALUES(%s, %s, %s)""" 
    schema_value = [
        ('Date Time', 'Date and time of measurement', 'datetime'),
        ('NOx',	'Concentration of oxides of nitrogen', 'μg/m3'),
        ('NO2', 'Concentration of nitrogen dioxide', 'μg/m3'),
        ('NO',	'Concentration of nitric oxide', 'μg/m3'),
        ('SiteID', 'Site ID for the station', 'integer'),
        ('PM10'	, 'Concentration of particulate matter<10 micron diameter',	'μg/m3'),
        ('NVPM10', 'Concentration of non - volatile particulate matter <10 micron diameter', 'μg/m3'),
        ('VPM10', 'Concentration of volatile particulate matter <10 micron diameter', 'μg/m3'),
        ('NVPM2.5',	'Concentration of non volatile particulate matter <2.5 micron diameter', 'μg/m3'),
        ('PM2.5', 'Concentration of particulate matter <2.5 micron diameter', 'μg/m3'),
        ('VPM2.5',	'Concentration of volatile particulate matter <2.5 micron diameter', 'μg/m3'),
        ('CO', 'Concentration of carbon monoxide',	'mg/m3'),
        ('O3', 'Concentration of ozone', 'μg/m3'),
        ('SO2',	'Concentration of sulphur dioxide',	'μg/m3'),
        ('Temperature', 'Air temperature', '°C'),
        ('RH', 'Relative Humidity', '%'),
        ('Air Pressure', 'Air Pressure', 'mbar'),
        ('Location', 'Text description of location', 'text'),
        ('geo_point_2d', 'Latitude and longitude', 'geo point'), 
        ('DateStart', 'The date monitoring started', 'datetime'),
        ('DateEnd',	'The date monitoring ended', 'datetime'),
        ('Current',	'Is the monitor currently operating', 'text'),
        ('Instrument Type', 'Classification of the instrument', 'text')  ] 
    cur.executemany(schema_sql, schema_value) 

    db.commit()
    db.close()  
except BaseException as err:
    print(f"An error occured: {err}")
    sys.exit(1) 
