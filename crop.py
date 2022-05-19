# import csv module
import csv
# open the bristol csv file and read
with open('bristol-air-quality-data.csv', 'r') as csv_file: 
    data = csv.reader(csv_file, delimiter = ';') 
# create new csv file called crop.csv for writing
    with open('crop.csv', 'w') as new_file: 
        csv_writer = csv.writer(new_file, delimiter = '#') 
# iterate through the lines read in bristol air quality data
        for line in data: 
# write only rows from 2010
             if line[0] >= '2010-01-01T00:00:00+00:00': 
                csv_writer.writerow(line) 
