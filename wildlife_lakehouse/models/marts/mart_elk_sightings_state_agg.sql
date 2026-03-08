SELECT 
sighting_date,
season,
state,
sum(case when coordinate_quality = 'low'
    then 1
    else 0
    end) as count_low_quality_sightings,
sum(case when coordinate_quality = 'medium'
    then 1
    else 0
    end) as count_medium_quality_sightings,
sum(case when coordinate_quality = 'high'
    then 1
    else 0
    end) as count_high_quality_sightings,
count(distinct(gbifID)) as sightings_count,
AVG(coordinate_uncertainty_meters) as avg_coordinate_uncertainty
FROM {{ref('int_elk_sightings')}}
GROUP BY 1,2,3