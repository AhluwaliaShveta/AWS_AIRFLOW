import os
from dotenv import load_dotenv
import boto3
import pandas as pd
import requests
from io import StringIO
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

# Loading environment variables from .env file
load_dotenv()


class BronzeLayer:

    def __init__(self):
        pass

    def ingest_data_api(self, url):
        # GitHub token needed since the repo is private
        token = os.environ.get("GITHUB_TOKEN")
        headers = {"Authorization": f"token {token}"} if token else {}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.text
            df = pd.read_csv(StringIO(data))

            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index=False)

            return csv_buffer.getvalue()
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None

    def put_data_s3(self, bucket_name, object_key, data):
        aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

        s3_client = boto3.client(
            's3',
            region_name='us-west-2',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=data
        )

        return f"Data uploaded to S3 bucket '{bucket_name}' with object key '{object_key}'"


# This block now runs OUTSIDE the class, at module level
if __name__ == "__main__":
    obj = BronzeLayer()
    data = obj.ingest_data_api("https://raw.githubusercontent.com/AhluwaliaShveta/ApacheAirflow-main/refs/heads/main/bookings.csv")

    if data is not None:
        result = obj.put_data_s3("sidhiairflowaws", "raw_bronze/bookings.csv", data)
        print(result)