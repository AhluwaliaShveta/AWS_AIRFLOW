AWS Data Engineering Project

<img width="2037" height="772" alt="image" src="https://github.com/user-attachments/assets/2ee4a7e9-47fd-49dd-8669-3e49a99b31d9" />


An end-to-end AWS data engineering pipeline orchestrated with Apache Airflow, following a Medallion Architecture (Bronze → Silver → Gold) to transform raw data into analytics-ready datasets.

🔄 Data Flow
Source Data
    ↓
Bronze Layer — Raw Data / S3
    ↓
Silver Layer — Clean & Transform / Spark
    ↓
Gold Layer — Analytics-Ready Data
    ↓
Athena / Data Warehouse
    ↓
Power BI & Analytics
📁 Project Structure
aws_project/
├── dags/
│   └── aws_project.py          # Airflow DAG & orchestration
├── utils/
│   ├── bronze_layer.py         # Raw data ingestion
│   ├── silver_layer.py         # Data cleaning & transformation
│   └── gold_layer.py           # Business-ready datasets
├── config/
│   └── airflow.cfg
├── Dockerfile
├── docker-compose.yaml
└── requirements.txt
🛠️ Tech Stack

AWS S3 · Apache Airflow · Python · Apache Spark · AWS Glue · Athena · Redshift · Snowflake · Docker · Power BI

✨ Key Features
Medallion-based Bronze, Silver, and Gold data layers
Airflow DAGs for workflow orchestration and scheduling
Modular Python transformation logic
Cloud-based data lake and warehouse integration
Dockerized Airflow environment
Analytics-ready datasets for BI and reporting

🚀 Run Locally
docker compose up -d

Open Airflow at:

http://localhost:8080

Trigger the aws_project DAG to execute the pipeline.
aws_project/
├── dags/
│   └── aws_project.py
├── utils/
│   ├── bronze_layer.py
│   ├── silver_layer.py
│   └── gold_layer.py
├── config/
│   └── airflow.cfg
├── Dockerfile
├── docker-compose.yaml
└── requirements.txt
Tech Stack

AWS S3 · Apache Airflow · Python · Spark · AWS Glue · Athena · Redshift · Snowflake · Docker · Power BI

Run Locally
docker compose up -d

Open Airflow:

http://localhost:8080

Trigger the aws_project DAG to run the pipeline.
