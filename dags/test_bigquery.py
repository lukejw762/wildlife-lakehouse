from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from datetime import datetime

with DAG(
    dag_id="test_bigquery_connection",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    create_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id="create_wildlife_dataset",
        dataset_id="wildlife_raw",
        project_id="wildlife-lakehouse",
        location="US",
    )