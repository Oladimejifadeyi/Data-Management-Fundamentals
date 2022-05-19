use `pollution-db2`;
select year(readings.datetime),stations.location,avg(readings.`pm2.5`),avg(readings.`vpm2.5`) 
from readings join stations on  readings.`station_id-fk`=stations.stationid 
where year(readings.datetime) = '2019'
and time(readings.datetime) = '08:00:00'
group by 1,2; 







