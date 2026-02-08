from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import boto3

# local imports
from api_ingestion import ingest_orders_to_s3
from glue_job_trigger import run_glue_job


default_args = {
    "owner": "rohit",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="api_to_s3_ingestion",
    default_args=default_args,
    description="API → S3 → Glue ETL pipeline",
    start_date=datetime(2026, 2, 8),
    schedule_interval="@daily",
    catchup=False,
    tags=["api", "s3", "glue", "ingestion"],
) as dag:

    # -----------------------------
    # Task 1: API → S3 (raw zone)
    # -----------------------------
    ingest_task = PythonOperator(
        task_id="ingest_orders_api_to_s3",
        python_callable=ingest_orders_to_s3,
    )

    # -----------------------------
    # Task 2: Glue raw → parquet (silver)
    # -----------------------------
    raw_to_parquet = PythonOperator(
        task_id="run_glue_raw_to_parquet",
        python_callable=run_glue_job,
        op_args=["orders_raw_to_parquet"],  # ✅ matches Glue job
    )

    # -----------------------------
    # Task 3: Glue parquet → gold
    # -----------------------------
    silver_to_gold = PythonOperator(
        task_id="run_glue_silver_to_gold",
        python_callable=run_glue_job,
        op_args=["orders_silver_to_gold"],
    )

    # -----------------------------
    # Task 4: Run Glue crawler on gold
    # -----------------------------
    def run_gold_crawler():
        glue = boto3.client("glue", region_name="us-east-1")
        glue.start_crawler(Name="gold_crawler")

    gold_crawler = PythonOperator(
        task_id="run_gold_glue_crawler",
        python_callable=run_gold_crawler,
    )

    # -----------------------------
    # Dependencies
    # -----------------------------
    ingest_task >> raw_to_parquet >> silver_to_gold >> gold_crawler
