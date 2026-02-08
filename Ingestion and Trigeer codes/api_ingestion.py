import requests
import json
import boto3
from datetime import datetime, timezone


def ingest_orders_to_s3():
    """
    Fetch orders data from external API and store raw JSON in S3,
    partitioned by ingestion date.
    """

    # -------- CONFIG --------
    API_URL = "https://fakestoreapi.com/carts"
    BUCKET_NAME = "rohit-ecommerce-data-lake"
    S3_RAW_PREFIX = "raw/orders"

    # -------- INGESTION DATE (UTC) --------
    ingestion_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # -------- API CALL --------
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()

    # -------- CONVERT TO JSON STRING --------
    json_data = json.dumps(data)

    # -------- S3 CLIENT --------
    s3 = boto3.client("s3")

    # -------- S3 OBJECT KEY --------
    s3_key = f"{S3_RAW_PREFIX}/ingestion_date={ingestion_date}/orders.json"

    # -------- UPLOAD --------
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=s3_key,
        Body=json_data,
        ContentType="application/json"
    )

    print(f"Uploaded raw data to s3://{BUCKET_NAME}/{s3_key}")

