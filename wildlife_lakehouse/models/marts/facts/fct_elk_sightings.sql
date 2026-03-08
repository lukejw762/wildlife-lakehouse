SELECT 
gbifID,
occurrenceID,
sighting_date,
season,
latitude,
longitude,
coordinate_uncertainty_meters,
coordinate_quality,
county,
state,
country
FROM {{ref('int_elk_sightings')}}