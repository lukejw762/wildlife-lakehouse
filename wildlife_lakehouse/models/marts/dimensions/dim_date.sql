SELECT 
sighting_date,
extract(day from sighting_date) as day,
FORMAT_DATE('%A', sighting_date) as day_of_week,
extract(month from sighting_date) as month,
FORMAT_DATE('%B', sighting_date) as month_name,
extract(year from sighting_date) as year,
season
FROM {{ref('int_elk_sightings')}}
GROUP BY ALL