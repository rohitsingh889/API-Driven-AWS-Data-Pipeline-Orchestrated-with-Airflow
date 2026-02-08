# API-Driven-AWS-Data-Pipeline-Orchestrated-with-Airflow
📦 API → S3 → AWS Glue → Athena
This project demonstrates a modern, production-style data engineering pipeline built using Apache Airflow, Amazon S3, AWS Glue, and Amazon Athena.

The pipeline ingests e-commerce order data from a public REST API, stores it immutably in an S3-based data lake, processes it through Bronze → Silver → Gold layers, and exposes a query-ready analytics table for downstream consumption.

The design follows industry best practices for scalability, reliability, and cloud-native data processing.

Data Source
Public REST API: https://fakestoreapi.com/carts
