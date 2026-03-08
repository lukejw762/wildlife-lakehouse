SELECT 
gbifID,
occurrenceID,
COALESCE(DATE(year,month,day),cast(eventDate as Date)) as sighting_date,
decimalLatitude as latitude,
decimalLongitude as longitude,
coordinateUncertaintyInMeters as coordinate_uncertainty_meters,
county,
COALESCE(stateProvince,state)as state,
country,
institutionCode as institution_code
FROM {{ source('wildlife_raw', 'elk_sighting_raw') }}
WHERE 
(decimalLatitude IS NOT NULL 
and decimalLongitude IS NOT NULL)