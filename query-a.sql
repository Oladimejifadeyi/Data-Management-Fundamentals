select stations.location, max(readings.nox) as highest_reading, 
max(readings.datetime) as date from readings 
join stations on readings.`station_id-fk`=stations.stationid 
where year(readings.datetime) = '2019' 
group by 1;