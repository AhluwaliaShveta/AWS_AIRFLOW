from datetime import datetime, timedelta
from airflow.sdk import dag, task
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.bronze_layer import BronzeLayer
from utils.silver_layer import SilverLayer
from utils.gold_layer import GoldLayer

# -------------------------------- CODE ----------------------------------- #

@dag(
    schedule='@daily',
    is_paused_upon_creation=False
)
def aws_project():

    # Task to extract data from API and load it to S3
    @task.python(retries=3, retry_delay=timedelta(seconds=5))
    def extract_load_s3():
        # Fetching data from API and loading it to S3 using a loop
        urls = [
            "https://raw.githubusercontent.com/AhluwaliaShveta/ApacheAirflow-main/refs/heads/main/bookings.csv",
            "https://raw.githubusercontent.com/AhluwaliaShveta/ApacheAirflow-main/refs/heads/main/passengers.csv",
            "https://raw.githubusercontent.com/AhluwaliaShveta/ApacheAirflow-main/refs/heads/main/airports.csv"
        ]

        obj = BronzeLayer()
        folder_name = datetime.now().strftime("%Y-%m-%d")

        for url in urls:
            fetched_data = obj.ingest_data_api(url)

            if fetched_data is None:
                raise ValueError(f"Failed to fetch data from {url}, skipping upload.")

            obj.put_data_s3(
                "sidhiairflowaws",
                f"raw_bronze/{folder_name}/{url.split('/')[-1]}",
                fetched_data
            )

        return folder_name

    # Task to trigger Spark job in AWS Glue to transform the data and load it to S3
    @task.python(retries=3, retry_delay=timedelta(seconds=5))
    def transform_load_s3(ti):
        last_load_date = ti.xcom_pull(task_ids='extract_load_s3', key='return_value')

        obj = SilverLayer()
        job_run_id = obj.trigger_spark_job("silver_layer", last_load_date)
        print(f"Glue Job triggered with JobRunId: {job_run_id}")

    # Task to trigger Spark job in AWS Glue to transform the data and load it in parquet format to S3
    @task.python(retries=3, retry_delay=timedelta(seconds=5))
    def transform_load_s3_parquet(ti):
        last_load_date = ti.xcom_pull(task_ids='extract_load_s3', key='return_value')

        obj = SilverLayer()
        job_run_id = obj.trigger_spark_job("silverlayer_athena", last_load_date)
        print(f"Glue Job triggered with JobRunId: {job_run_id}")

    # Task to trigger the Glue crawler to update the Glue catalog
    @task.python(retries=3, retry_delay=timedelta(seconds=5))
    def trigger_crawler():
        obj = SilverLayer()
        crawler_response = obj.trigger_crawler("crawler_silver")  # matches actual (typo'd) crawler name in AWS
        print(crawler_response)

    # Task to trigger the Databricks job to transform the data and load it to the gold layer
    @task.python(retries=3, retry_delay=timedelta(seconds=5))
    def trigger_databricks_job():
        obj = GoldLayer()
        response = obj.trigger_databricks_job(job_id=486921513544553)
        print(response)

    # Task Dependency
    extract_load_s3_task = extract_load_s3()
    transform_load_s3_task = transform_load_s3()
    transform_load_s3_parquet_task = transform_load_s3_parquet()
    trigger_crawler_task = trigger_crawler()
    trigger_databricks_job_task = trigger_databricks_job()

    extract_load_s3_task >> [transform_load_s3_task, transform_load_s3_parquet_task] >> trigger_crawler_task >> trigger_databricks_job_task


aws_project_dag = aws_project()