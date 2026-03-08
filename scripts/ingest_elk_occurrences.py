import requests
import json
import pandas


offset = 0 
base_url = "https://api.gbif.org/v1/occurrence/search"
payload = {"scientificName":"Cervus canadensis","country":"US","limit":300,'orderBy':'eventDate','order':'desc','offset':offset}
endofRecords = False
cleaned_list = []


while endofRecords is False and offset < 2000:

    ## make API call
    r= requests.get(base_url,params=payload)
    ##print(f"Encoded URL: {r.url}") 
    ##print(f"JSON Response: {r.json()}")
    results = r.json()['results']
    


    ## process results
    for row in results:
        filtered_row = {key: value for key, value in row.items() if key in (('gbifID','occurrenceID','decimalLatitude','decimalLongitude','stateProvince','country','eventDate','year','month','day','coordinateUncertaintyInMeters','recordedBy','institutionCode','gadm'))}
        filtered_row['county'] = filtered_row.get('gadm',{}).get('level2',{}).get('name')
        filtered_row['state'] = filtered_row.get('gadm',{}).get('level1',{}).get('name')
        filtered_row['country'] = filtered_row.get('gadm',{}).get('level0',{}).get('name')
        filtered_row.pop('gadm', None)

        cleaned_list.append(filtered_row)

    ## increment offset
    offset = offset + 300
    payload['offset'] = offset
    
    ## update end of records
    endofRecords = r.json()['endOfRecords']

from google.cloud import bigquery
import os
import pandas as pd

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\lukej\Projects\wildlife-lakehouse\config\wildlife-lakehouse-8025d912066e.json"

client = bigquery.Client(project="wildlife-lakehouse")

job = client.load_table_from_dataframe(df,table,config=job_config)

job.result()

print(f"Loaded {job.output_rows} rows into {table_id}.")

