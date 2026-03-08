SELECT *
FROM {{ ref('stg_elk_sightings') }}
WHERE latitude NOT BETWEEN -90 and 90
    or longitude NOT BETWEEN -180 and 180