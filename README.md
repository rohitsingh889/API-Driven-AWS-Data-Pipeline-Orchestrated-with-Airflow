# API-Driven-AWS-Data-Pipeline-Orchestrated-with-Airflow

![Project Overview](https://github.com/rohitsingh889/API-Driven-AWS-Data-Pipeline-Orchestrated-with-Airflow/blob/main/Pics/complete%20pipeline.jpg)

## 📦 API → S3 Data Lake → Glue ETL → Athena Analytics
### End-to-End Data Engineering Project

---

## 📌 Project Description

This project demonstrates a **production-style end-to-end data engineering pipeline** built using **Apache Airflow, Amazon S3, AWS Glue, and Amazon Athena**.

The pipeline ingests **e-commerce order data from a public REST API**, stores it in an **S3-based data lake**, processes it through **Bronze → Silver → Gold layers**, and exposes an **analytics-ready dataset** for SQL-based reporting.

The design follows **real-world cloud data engineering best practices**, including immutable raw storage, distributed ETL, workflow orchestration, and schema-driven analytics.

**Data Source:**  
https://fakestoreapi.com/

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
Preserve raw data exactly as received

**Bronze Layer (Raw Data):**

![Bronze Layer](https://github.com/rohitsingh889/API-Driven-AWS-Data-Pipeline-Orchestrated-with-Airflow/blob/main/Pics/bronzelayer.png)

---

## ⚙️ AWS Glue Job Triggering via boto3

AWS Glue ETL jobs in this project are **programmatically triggered from Apache Airflow** using the **boto3 AWS SDK** instead of manual execution.

### How Glue Jobs Are Triggered

- A lightweight Python utility function is used to start Glue jobs dynamically  
- The function accepts the Glue job name as a parameter  
- Airflow calls this function as part of the DAG execution  
- Glue jobs run asynchronously in AWS while Airflow continues orchestration  

### Purpose of This Approach

- Decouples orchestration logic from ETL logic  
- Allows the same Airflow DAG to trigger multiple Glue jobs  
- Avoids hardcoding Glue execution inside ETL scripts  
- Matches real-world, production-grade orchestration patterns  

### Key Responsibilities of the Glue Trigger Function

- Establishes a connection to AWS Glue using IAM-based authentication  
- Starts a Glue job run using the provided job name  
- Logs the Glue Job Run ID for monitoring and debugging  
- Enables Airflow to orchestrate AWS-native ETL services seamlessly  

### Why Use boto3 for Glue Job Execution

- Native AWS SDK for Python  
- Secure IAM role-based access (no credentials in code)  
- Fully compatible with Airflow PythonOperators  

### End-to-End Flow with Glue Job Triggering

Airflow DAG
    ↓
PythonOperator
    ↓
boto3 Glue Client
    ↓
AWS Glue Job Execution
    ↓
Processed Data Written to S3


This approach ensures **clear separation of concerns**, where:
- **Airflow** handles orchestration and scheduling  
- **AWS Glue** handles distributed data processing  
- **boto3** acts as the integration layer between them  

---

### 2️⃣ Raw → Silver Transformation

- AWS Glue reads raw JSON data from S3  
- Schema is inferred and normalized  
- Data is converted to **Parquet format**  
- Output is written to the **Silver zone**  

**Purpose:**  
Improve performance, enforce structure, and optimize storage.

**Silver Layer:**

![Silver Layer](https://github.com/rohitsingh889/API-Driven-AWS-Data-Pipeline-Orchestrated-with-Airflow/blob/main/Pics/sliver.png)

---

### 3️⃣ Silver → Gold Transformation

- AWS Glue transforms Silver data into an analytics-ready fact table  
- Nested product arrays are exploded  
- Data is normalized to **order-line level**  
- Partition columns (year, month) are added  
- Output is written to the **Gold zone**  

**Purpose:**  
Create business-consumable datasets for reporting and analytics.

**AWS Glue Jobs:**  
![Glue Jobs](https://github.com/rohitsingh889/API-Driven-AWS-Data-Pipeline-Orchestrated-with-Airflow/blob/main/Pics/Glue%20jobs.png)
![Glue Jobs](https://github.com/rohitsingh889/API-Driven-AWS-Data-Pipeline-Orchestrated-with-Airflow/blob/main/Pics/P4.png)

**Gold Layer:**  
![Gold Layer](https://github.com/rohitsingh889/API-Driven-AWS-Data-Pipeline-Orchestrated-with-Airflow/blob/main/Pics/goldlayer.png)

---

### 4️⃣ Metadata Management

- AWS Glue Crawler scans the Gold zone  
- Table schema is registered in the Glue Data Catalog  
- Athena automatically detects the table  

**Purpose:**  
Enable SQL analytics without manual schema management.

**AWS Glue Crawler:**  
![Glue Crawler](https://github.com/rohitsingh889/API-Driven-AWS-Data-Pipeline-Orchestrated-with-Airflow/blob/main/Pics/crawler.png)

---

### 5️⃣ Analytics & Querying

- Amazon Athena queries the Gold table  
- Supports aggregations, trends, and data quality checks  
- Partition pruning improves query performance  
- No infrastructure provisioning required  

**Amazon Athena Queries:**

![Athena Query 1](https://github.com/rohitsingh889/API-Driven-AWS-Data-Pipeline-Orchestrated-with-Airflow/blob/main/Pics/p2.png)  
![Athena Query 2](https://github.com/rohitsingh889/API-Driven-AWS-Data-Pipeline-Orchestrated-with-Airflow/blob/main/Pics/p1.png)

---

## 🧰 Technology Stack

| Layer | Technology |
|------|-----------|
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

**boto3** is used to programmatically interact with AWS services.

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

Apache Airflow is deployed **locally using Docker**, simulating a production orchestration environment.

![Airflow Details](https://github.com/rohitsingh889/API-Driven-AWS-Data-Pipeline-Orchestrated-with-Airflow/blob/main/Pics/airflow%20details.png)  
![Airflow Status](https://github.com/rohitsingh889/API-Driven-AWS-Data-Pipeline-Orchestrated-with-Airflow/blob/main/Pics/airflowstatus.png)

**Airflow Graph View:**  
![Airflow Graph](https://github.com/rohitsingh889/API-Driven-AWS-Data-Pipeline-Orchestrated-with-Airflow/blob/main/Pics/airflow%20graph.png)

**Airflow Gantt Chart:**  
![Airflow Gantt](https://github.com/rohitsingh889/API-Driven-AWS-Data-Pipeline-Orchestrated-with-Airflow/blob/main/Pics/airflow%20gantt%20chart.png)

### Airflow responsibilities
- Schedule the pipeline (daily)  
- Manage task dependencies  
- Retry failed tasks automatically  
- Orchestrate AWS services using boto3  
- Provide monitoring and observability

## ❌ Failure Handling & Reliability

- Airflow retries transient failures automatically
- API failures result in task retries without partial writes
- Raw data ingestion is idempotent and date-partitioned
- Glue jobs are decoupled and can be re-run independently

## 📁 Airflow Code Organization

All Airflow-related Python files are placed within the **same Airflow DAG configuration directory** to ensure proper import resolution and smooth execution inside the Dockerized Airflow environment.

### Files Included

- **`api_ingestion.py`**  
  Contains the core business logic for API ingestion.  
  This module:
  - Fetches raw data from the external REST API  
  - Writes immutable, date-partitioned JSON data to the S3 Bronze layer  
  - Is designed to be reusable and callable by Airflow operators  

- **`glue_job_trigger.py`**  
  Contains utility functions for triggering AWS Glue jobs programmatically using `boto3`.  
  This module:
  - Starts Glue ETL jobs by job name  
  - Enables Airflow to orchestrate Glue without embedding orchestration logic inside ETL scripts  
  - Supports clean separation between orchestration and transformation layers  

- **`api_ingestion_dag.py`**  
  Defines the Apache Airflow DAG.  
  This file:
  - Schedules and orchestrates the end-to-end pipeline  
  - Calls functions from `api_ingestion.py` and `glue_trigger.py` using PythonOperators  
  - Manages task dependencies, retries, and execution order  

### Why All Files Are in the Same Airflow Directory

- Airflow automatically adds the DAG directory to its Python path  
- Keeping related modules in the same location avoids import issues inside Docker containers  


This organization ensures:
- Clean separation of concerns  
- Reusability of ingestion and orchestration logic  
- Reliable DAG parsing and execution in a Dockerized Airflow environment  


### Why local Airflow
- Cost-effective development  
- Easy setup and debugging  
- Alternative of  managed Airflow services (MWAA)  


---

## 🎯 Enhancements Implemented

- Incremental data ingestion and processing using Airflow execution dates  
- Raw data partitioned by ingestion date to avoid full reloads  
- Incremental Glue jobs processing only new data per run  
- Safe re-runs without reprocessing historical data  



## 🔐 Security & Authentication


- IAM-based authentication is used for all AWS access.
- In local development, credentials are injected securely via environment variables, mirroring role-based access used in production environments
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

- Incremental ingestion[Enhanacement Completed]
- Data quality checks 
- Airflow sensors for Glue job monitoring  
- BI dashboards   
- Infrastructure as Code (Terraform)  
- CI/CD for DAG deployments  

---

### Summary

This project showcases a **complete, production-style Airflow-orchestrated data lake pipeline** built on **AWS services**, ingesting e-commerce order data from a public REST API and transforming it into an analytics-ready dataset:

- **Extract:** Fetch raw order data from an external REST API (FakeStore API)  
- **Load (Bronze):** Store raw JSON data immutably in Amazon S3, partitioned by ingestion date  
- **Transform (Silver):** Use AWS Glue to convert raw JSON into optimized Parquet format  
- **Transform (Gold):** Apply business transformations using AWS Glue (PySpark)  
- **Orchestrate:** Apache Airflow manages scheduling, retries, and dependencies  
- **Catalog & Query:** AWS Glue Crawler enables serverless SQL analytics via Athena  
- **Analytics-Ready:** Supports trends, aggregations, and data quality checks  
- **Scalable & Reusable:** Modular and extensible design  


- ![Silver Layer](https://github.com/rohitsingh889/API-Driven-AWS-Data-Pipeline-Orchestrated-with-Airflow/blob/main/Pics/project%20desc.jpg)

---

## 👨‍💻 Author & Project Context

**Rohit Raj Singh**

This project is part of my professional portfolio and demonstrates a **production-grade cloud data engineering pipeline** using **Apache Airflow and AWS**.

Key skills reflected:
- Workflow orchestration with Apache Airflow (local, Dockerized)  
- REST API ingestion and immutable data lake design  
- AWS Glue–based distributed ETL using PySpark  
- Schema inference and partition management with Glue Crawlers  
- Serverless analytics using Amazon Athena  
- Secure, IAM-based AWS integration using boto3 and AWS CLI  
- End-to-end pipeline automation and monitoring  

📬 **LinkedIn:**  
[Connect with me professionally](https://www.linkedin.com/in/rohit-raj-singh-3030172a4?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)
