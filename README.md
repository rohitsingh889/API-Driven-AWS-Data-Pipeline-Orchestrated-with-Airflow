# API-Driven-AWS-Data-Pipeline-Orchestrated-with-Airflow
![Logo](https://github.com/rohitsingh889/API-Driven-AWS-Data-Pipeline-Orchestrated-with-Airflow/blob/main/Pics/project%20desc.jpg)
# 📦 API → S3 → AWS Glue → Athena  
## End-to-End Data Engineering Project

---

## 📌 Project Description

This project demonstrates a **production-style end-to-end data engineering pipeline** built using **Apache Airflow, Amazon S3, AWS Glue, and Amazon Athena**.

The pipeline ingests **e-commerce order data from a public REST API**, stores it in an **S3-based data lake**, processes it through **Bronze → Silver → Gold layers**, and exposes an **analytics-ready dataset** for SQL-based reporting.

The design closely follows **real-world cloud data engineering best practices**, including immutable raw storage, distributed ETL, workflow orchestration, and schema-driven analytics.

**Data Source:**  
https://fakestoreapi.com/carts

---

## 🏗️ High-Level Architecture

- Apache Airflow (Local, Dockerized) orchestrates the pipeline
- REST API provides raw JSON order data
- Amazon S3 serves as the data lake (Bronze, Silver, Gold)
- AWS Glue performs distributed ETL using PySpark
- AWS Glue Crawler manages metadata
- Amazon Athena enables serverless analytics

---

## 🔁 End-to-End Workflow

### 1️⃣ API Ingestion – Bronze Layer
- Airflow triggers a Python ingestion task
- Raw JSON data is fetched from the external API
- Data is stored **immutably** in Amazon S3
- Files are partitioned by **ingestion date**
- No transformations are applied at this stage

**Purpose:**  
Preserve raw data exactly as received for replayability and auditing.

---

### 2️⃣ Raw → Silver Transformation
- AWS Glue reads raw JSON data from S3
- Schema is inferred and normalized
- Data is converted to **Parquet format**
- Output is written to the **Silver zone**

**Purpose:**  
Improve performance, enforce structure, and optimize storage.

---

### 3️⃣ Silver → Gold Transformation
- AWS Glue transforms Silver data into an analytics-ready fact table
- Nested product arrays are exploded
- Data is normalized to **order-line level**
- Partition columns (year, month) are added
- Output is written to the **Gold zone**

**Purpose:**  
Create business-consumable datasets for reporting and analytics.

---

### 4️⃣ Metadata Management
- AWS Glue Crawler scans the Gold zone
- Table schema is registered in the Glue Data Catalog
- Athena automatically detects the table

**Purpose:**  
Enable SQL analytics without manual schema management.

---

### 5️⃣ Analytics & Querying
- Amazon Athena is used to query the Gold table
- Supports aggregations, trends, and data quality checks
- Partition pruning improves query performance
- No infrastructure provisioning required

---

## 🧰 Technology Stack

| Layer | Technology |
|-----|-----------|
| Orchestration | Apache Airflow (Local, Docker) |
| Storage | Amazon S3 |
| ETL | AWS Glue (PySpark) |
| Metadata | AWS Glue Crawler |
| Query Engine | Amazon Athena |
| SDK | boto3 |
| CLI | AWS CLI |
| Authentication | IAM Roles |

---

## 🐍 boto3 Usage (AWS SDK for Python)

**boto3** is used to programmatically interact with AWS services within the pipeline.

### Where boto3 is used
- Upload raw API data to Amazon S3
- Trigger AWS Glue ETL jobs
- Start AWS Glue Crawlers
- Authenticate securely using IAM roles

### Why boto3
- Native AWS SDK for Python
- Secure, role-based authentication
- Enables full automation from Airflow
- Industry standard for AWS-backed pipelines

---

## 💻 AWS CLI Usage (Local Development)

The **AWS Command Line Interface (CLI)** is used during development and operations.

### AWS CLI is used for
- Verifying data in S3 buckets
- Running and debugging Glue jobs
- Managing Glue Crawlers
- Validating IAM permissions
- Troubleshooting access and connectivity

### Benefits
- Fast local validation
- No dependency on AWS Console
- Matches real-world production workflows

---

## ⏱️ Apache Airflow (Local, Dockerized)

Apache Airflow is deployed **locally using Docker containers**, simulating a production orchestration environment.

### Airflow responsibilities
- Schedule the pipeline (daily)
- Manage task dependencies
- Retry failed tasks automatically
- Orchestrate AWS services using boto3
- Provide monitoring and observability

### Why local Airflow
- Cost-effective development
- Easy setup and debugging
- Mirrors managed Airflow services (MWAA)
- Ideal for portfolio and interview projects

---

## 🔐 Security & Authentication

- IAM roles are used for all AWS access
- No AWS credentials are hardcoded
- boto3 and AWS CLI rely on role-based authentication
- Follows AWS security best practices

---

## 📊 Analytics Capabilities

The Gold table supports:
- Order and sales trends
- User behavior analysis
- Product performance metrics
- Repeat customer analysis
- Data quality validation
- Partition-optimized queries

---

## 🚀 Key Data Engineering Concepts Demonstrated

- REST API ingestion
- Cloud-native data lake architecture
- Bronze / Silver / Gold layers
- Distributed ETL with Spark
- Workflow orchestration
- Partitioned analytics tables
- Metadata-driven querying
- Production-style SQL analytics

---

## 🎯 Future Enhancements

- Incremental ingestion
- Data quality checks (Great Expectations)
- Airflow sensors for Glue job monitoring
- BI dashboards (Amazon QuickSight)
- Infrastructure as Code (Terraform)
- CI/CD for DAG deployments

---

## 👤 Author

**Rohit**  
Data Engineer

