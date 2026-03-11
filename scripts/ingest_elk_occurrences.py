## Imports
import requests
import pandas as pd
from google.cloud import bigquery


## pull data with API call
def fetch_sightings(species,country,max_records,limit=300):
    offset = 0 
    base_url = "https://api.gbif.org/v1/occurrence/search"
    payload = {"scientificName":species,"country":country,"limit":limit,'orderBy':'eventDate','order':'desc','offset':offset}
    endofRecords = False
    records =[]

    while endofRecords is False and offset < max_records:

        
        r= requests.get(base_url,params=payload)
        result = r.json()
        
        for row in result['results']:
            records.append(row)
        
        offset = offset + limit
        payload['offset'] = offset
        endofRecords = result['endOfRecords']
    
    return records

## process JSON objects in records list
def parse_sightings(records):
    cleaned_list = []
    
    for row in records:
        filtered_row = {key: value for key, value in row.items() if key in (('gbifID','occurrenceID','decimalLatitude','decimalLongitude','stateProvince','country','eventDate','year','month','day','coordinateUncertaintyInMeters','institutionCode','gadm'))}
        filtered_row['county'] = filtered_row.get('gadm',{}).get('level2',{}).get('name')
        filtered_row['state'] = filtered_row.get('gadm',{}).get('level1',{}).get('name')
        filtered_row['country'] = filtered_row.get('gadm',{}).get('level0',{}).get('name')
        filtered_row.pop('gadm', None)

        cleaned_list.append(filtered_row)

    df = pd.DataFrame(cleaned_list)
    df['eventDate'] = pd.to_datetime(df['eventDate'], utc=True, errors='coerce')

    return df


def load_to_bigquery(df,table_id,write_disposition):
## Create Client
    
    client = bigquery.Client(project=table_id.split(".")[0])
## Define Schema
    schema = [
        bigquery.SchemaField("gbifID", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("eventDate", "TIMESTAMP", mode="NULLABLE"),
        bigquery.SchemaField("year", "INT64", mode="NULLABLE"),
        bigquery.SchemaField("month", "INT64", mode="NULLABLE"),
        bigquery.SchemaField("day", "INT64", mode="NULLABLE"),
        bigquery.SchemaField("county", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("state", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("stateProvince", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("country", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("decimalLatitude", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("decimalLongitude", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("occurrenceID", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("institutionCode", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("coordinateUncertaintyInMeters", "FLOAT64", mode="NULLABLE")
    ]
## Create Job Config
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition=write_disposition
    )
## Create Job
    job = client.load_table_from_dataframe(df,table_id,job_config=job_config)

    job.result()

    print(f"Loaded {job.output_rows} rows into {table_id}.")

def ingest_sightings(species,country,max_records,table_id,write_disposition):
    records = fetch_sightings(species,country,max_records)
    df = parse_sightings(records)
    load_to_bigquery(df,table_id,write_disposition)

if __name__ == "__main__":
    ingest_sightings(  species="Cervus canadensis",
        country="US",
        max_records=2000,
        table_id="wildlife-lakehouse.wildlife_raw.elk_sighting_raw",
        write_disposition="WRITE_TRUNCATE"
        )