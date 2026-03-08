SELECT 
gbifID,
occurrenceID,
sighting_date,
case 
    when extract(month from sighting_date) IN (12,1,2)
        then 'winter'
    when extract(month from sighting_date) IN (3,4,5)
        then 'spring'
    when extract(month from sighting_date) IN (6,7,8)
        then 'summer'
    when extract(month from sighting_date) IN (9,10,11)
        then 'fall'
    end as season,

latitude,
longitude,
coordinate_uncertainty_meters,
case 
    when coordinate_uncertainty_meters <= 100
        then 'high'
    when coordinate_uncertainty_meters > 100 and coordinate_uncertainty_meters <= 1000
        then 'medium'
    when coordinate_uncertainty_meters > 1000
        then 'low'
    end as coordinate_quality,
county,
state,
country,
recordedBy,
institution_code
FROM {{ref('stg_elk_sightings')}}