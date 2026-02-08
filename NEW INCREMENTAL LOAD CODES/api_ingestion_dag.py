# api_ingestion_dag.py
"""
Airflow DAG to orchestrate an incremental data pipeline:
API → S3 (Raw) → Glue (Silver) → Glue (Gold) → Glue Crawler

Incremental strategy:
- Airflow execution date ({{ ds }}) is used as the incremental watermark
- Each run processes only data for that specific date
- No full reloads or architectural changes required
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import boto3

# Local imports
from api_ingestion import ingest_orders_to_s3
from glue_job_trigger import run_glue_job

# -------------------------------------------------------------------
# Default DAG arguments
# -------------------------------------------------------------------
default_args = {
    "owner": "rohit",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

# -------------------------------------------------------------------
# DAG definition
# -------------------------------------------------------------------
with DAG(
    dag_id="api_to_s3_ingestion",
    default_args=default_args,
    description="Incremental API → S3 → Glue ETL pipeline",
    start_date=datetime(2026, 2, 8),
    schedule_interval="@daily",     # Daily incremental runs
    catchup=False,                  # No historical backfills by default
    tags=["api", "s3", "glue", "incremental"],
) as dag:

    # -------------------------------------------------------------------
    # Task 1: API → S3 (Raw / Bronze layer)
    # -------------------------------------------------------------------
    # Incremental logic:
    # - Airflow passes the execution date ({{ ds }})
    # - Raw data is written to an immutable S3 partition:
    #   raw/orders/ingestion_date=YYYY-MM-DD/
    ingest_task = PythonOperator(
        task_id="ingest_orders_api_to_s3",
        python_callable=ingest_orders_to_s3,
        op_kwargs={
            "run_date": "{{ ds }}"   # Incremental watermark from Airflow
        },
    )

    # -------------------------------------------------------------------
    # Task 2: Raw → Silver (Glue job)
    # -------------------------------------------------------------------
    # Incremental logic:
    # - Glue job reads ONLY the raw partition for run_date
    # - Writes parquet in append mode
    # - Previously processed data is untouched
    raw_to_parquet = PythonOperator(
        task_id="run_glue_raw_to_parquet",
        python_callable=run_glue_job,
        op_args=["Orders_Raw_To_Silver"],  # Exact Glue job name
        op_kwargs={
            "run_date": "{{ ds }}"          # Passed to Glue as --run_date
        },
    )

    # -------------------------------------------------------------------
    # Task 3: Silver → Gold (Glue job)
    # -------------------------------------------------------------------
    # Incremental logic:
    # - Glue job filters Silver data by run_date
    # - Only affected partitions (year/month) are overwritten
    # - Empty incremental batches are safely skipped
    silver_to_gold = PythonOperator(
        task_id="run_glue_silver_to_gold",
        python_callable=run_glue_job,
        op_args=["orders_silver_to_gold"],
        op_kwargs={
            "run_date": "{{ ds }}"          # Controls incremental scope
        },
    )

    # -------------------------------------------------------------------
    # Task 4: Run Glue Crawler on Gold
    # -------------------------------------------------------------------
    # Purpose:
    # - Registers / updates Gold table in Glue Data Catalog
    # - Crawler is triggered only after Gold data is written
    def run_gold_crawler():
        glue = boto3.client("glue", region_name="us-east-1")
        glue.start_crawler(Name="gold_crawler")

    gold_crawler = PythonOperator(
        task_id="run_gold_glue_crawler",
        python_callable=run_gold_crawler,
    )

    # -------------------------------------------------------------------
    # Task dependencies (end-to-end incremental flow)
    # -------------------------------------------------------------------
    ingest_task >> raw_to_parquet >> silver_to_gold >> gold_crawler
