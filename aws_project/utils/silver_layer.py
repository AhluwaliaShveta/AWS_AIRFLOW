import time
import boto3
import os
from dotenv import load_dotenv

load_dotenv()


class SilverLayer:

    def __init__(self):
        pass

    def trigger_spark_job(self, job_name, job_parameter):
        aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

        # Create a glue client
        glue_client = boto3.client(
            'glue',
            region_name='us-west-2',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        # Start the Glue job
        response = glue_client.start_job_run(
            JobName=job_name,
            Arguments={
                '--load_date': job_parameter
            }
        )

        job_run_id = response['JobRunId']

        # Polling mechanism to check the status of the job until it finishes
        while True:
            status = glue_client.get_job_run(
                JobName=job_name,
                RunId=job_run_id
            )['JobRun']['JobRunState']

            print(f"Job '{job_name}' status: {status}")

            if status in ('SUCCEEDED',):
                break
            elif status in ('FAILED', 'STOPPED', 'TIMEOUT', 'ERROR'):
                raise Exception(f"Glue job '{job_name}' ended with status: {status}")

            time.sleep(15)  # wait before polling again

        return job_run_id

    def trigger_crawler(self, crawler_name):
        aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

        # Create a glue client
        glue_client = boto3.client(
            'glue',
            region_name='us-west-2',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        # Start the Glue crawler
        response = glue_client.start_crawler(Name=crawler_name)
        return response


if __name__ == "__main__":
    obj = SilverLayer()
    job_run_id = obj.trigger_spark_job("silverlayer_athena", "2026-09-08")
    print(f"Glue Job triggered with JobRunID: {job_run_id}")