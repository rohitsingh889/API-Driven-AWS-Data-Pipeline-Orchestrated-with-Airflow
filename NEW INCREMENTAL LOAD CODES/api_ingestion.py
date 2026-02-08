import requests
import json
import boto3
from datetime import timezone

def ingest_orders_to_s3(run_date: str):
    """
    Incremental raw ingestion:
    - Fetches data from API
    - Writes immutable raw JSON to S3
    - Partitioned by Airflow execution date
    """

    # API endpoint
    API_URL = "https://fakestoreapi.com/carts"

    # S3 raw zone configuration
    BUCKET_NAME = "rohit-ecommerce-data-lake"
    S3_RAW_PREFIX = "raw/orders"

    # Incremental partition (controlled by Airflow)
    ingestion_date = run_date

    # Fetch data from external API
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()

    # Convert API response to JSON string
    json_data = json.dumps(data)

    # Initialize S3 client (IAM-based auth)
    s3 = boto3.client("s3")

    # Immutable raw data path (date-partitioned)
    s3_key = f"{S3_RAW_PREFIX}/ingestion_date={ingestion_date}/orders.json"

    # Upload raw data to S3
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=s3_key,
        Body=json_data,
        ContentType="application/json"
    )

    print(f"Uploaded raw data for ingestion_date={ingestion_date}")
