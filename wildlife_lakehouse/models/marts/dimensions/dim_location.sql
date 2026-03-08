SELECT 
county,
state,
country
FROM {{ref('int_elk_sightings')}}
GROUP BY ALL
