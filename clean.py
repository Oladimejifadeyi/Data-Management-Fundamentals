# import csv module
import csv 
# creat a list called stations for the 18 unquie site id
stations = {'188':'AURN Bristol Centre',
'203':'Brislington Depot',
'206':'Rupert Street',
'209':'IKEA M32',
'213': 'Old Market',
'215':'Parson Street School',
'228':'Temple Meads Station',
'270':'Wells Road',
'271':'Trailer Portway P&R',
'375':'Newfoundland Road Police Station',
'395':"Shiner's Garage",
'452':'AURN St Pauls',
'447':'Bath Road',
'459':'Cheltenham Road \ Station Road',
'463':'Fishponds Road',
'481':'CREATE Centre Roof',
'500':'Temple Way',
'501':'Colston Avenue'} 
# open the cropped csv file and read
with open('crop.csv', newline= '') as csv_file: 
    data = csv.reader(csv_file, delimiter = '#') 
# create new csv file called clean.csv for writing
    with open('clean.csv', 'w') as new_file: 
        csv_writer = csv.writer(new_file, delimiter = ',') 
# set line number 
        number = 1
# get header as next line
        header = next(data) 
        csv_writer.writerow(header) 
# iterate through the row in the crop csv data
        for row in data: 
            site_id = row[4]
            site_location = row[17] 
# set condition to print line numbers and mismatch field values for each dud record
            if (len(site_id) > 0) and (site_id in stations) and stations[site_id] == site_location:
                csv_writer.writerow(row) 
            else:
                if len(site_id) == 0:
                    print("line: ", number , " site id contains an empty string")
                elif site_id not in stations:
                    print("line: ", number ," site id", site_id, " does not match ", row[17])
                elif stations[site_id] != row[17]:
                    print("line: ", number ," ", stations[site_id], " does not match ", row[17])      
            number += 1 
            