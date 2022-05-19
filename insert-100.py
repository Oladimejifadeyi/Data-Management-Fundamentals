# Import modules
import itertools
import csv 
import sys 
from datetime import datetime 

count = 1
readings = []

sql = "INSERT INTO `readings` VALUES\n" 

with open('clean.csv', 'r') as csv_file: 
    for row in itertools.islice(csv.DictReader(csv_file, delimiter = ','), 100):

        del row['Location']
        del row['geo_point_2d'] 

        dt = datetime.fromisoformat(row['Date Time'][:-6])
        dt.strftime('%Y-%m-%d  %H:%M:%S') 
        row['Date Time'] = dt 

        ds = datetime.fromisoformat(row['DateStart'][:-6])
        dt.strftime('%Y-%m-%d  %H:%M:%S') 
        row['DateStart'] = ds 

        if row['DateEnd']:
            de = datetime.fromisoformat(row['DateEnd'][:-6])
            dt.strftime('%Y-%m-%d  %H:%M:%S') 
            row['DateEnd'] = de 


        readings = [ "'" + str(x) + "'" for x in row.values()] 
        readings = ",".join(readings) 

        readings = readings.replace("''", " NULL") 
        readings = readings.replace ("'True'", " True")
        readings = readings.replace ("'False'", " False") 

        sql += '(' + str(count) + ', ' + readings + '),' + '\n'

        count += 1 


sql_file = sql[:-2] + ';'
data = open('insert-100.sql', 'w') 
data.write(sql_file + '\n')
print(sql_file) 
