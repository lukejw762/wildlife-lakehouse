import sys
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.ingest_elk_occurrences import ingest_sightings

with DAG(
    dag_id="elk_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@weekly",
    catchup=False,
) as dag:
    
    ingest_task = PythonOperator(
        task_id="ingest_elk_sightings",
        python_callable=ingest_sightings,
        op_kwargs={
            "species":"Cervus canadensis",
            "country":"US",
            "max_records":2000,
            "table_id":"wildlife-lakehouse.wildlife_raw.elk_sighting_raw",
            "write_disposition":"WRITE_TRUNCATE"
    }
    )
    
    dbt_run_task = BashOperator(
        task_id ="dbt_run",
        bash_command ="dbt run --project-dir /opt/airflow/wildlife_lakehouse --profiles-dir /opt/airflow"
    )
    dbt_test_task = BashOperator(
        task_id="dbt_test",
        bash_command="dbt test --project-dir /opt/airflow/wildlife_lakehouse --profiles-dir /opt/airflow"
    )

    ingest_task >> dbt_run_task >> dbt_test_task