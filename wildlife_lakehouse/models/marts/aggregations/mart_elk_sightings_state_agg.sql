SELECT 
dd.sighting_date
,fes.season
,ds.state
,sum(case when fes.coordinate_quality = 'low'
    then 1
    else 0
    end) as count_low_quality_sightings,
sum(case when fes.coordinate_quality = 'medium'
    then 1
    else 0
    end) as count_medium_quality_sightings,
sum(case when fes.coordinate_quality = 'high'
    then 1
    else 0
    end) as count_high_quality_sightings,
count(distinct(fes.gbifID)) as sightings_count
FROM {{ref('fct_elk_sightings')}} fes
    LEFT JOIN {{ref('dim_date')}} dd
        ON fes.sighting_date = dd.sighting_date
    LEFT JOIN {{ref('dim_location')}} ds
        ON fes.county = ds.county
            and fes.state = ds.state
GROUP BY 1,2,3