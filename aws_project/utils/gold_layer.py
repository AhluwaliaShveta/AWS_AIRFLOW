from databricks.sdk import WorkspaceClient
import os
from dotenv import load_dotenv
 
load_dotenv()
 
 
class GoldLayer:
 
    def __init__(self):
        pass
 
    def trigger_databricks_job(self, job_id: int):
 
        databricks_pat = os.getenv("DATABRICKS_PAT")
        databricks_host = os.getenv("DATABRICKS_HOST")
 
        client = WorkspaceClient(
            host=databricks_host,
            token=databricks_pat
        )
 
        # Trigger the Databricks job
        run = client.jobs.run_now(job_id=job_id)
        return f"Triggered Databricks job with ID: {run.run_id}"
    

if __name__ == "__main__":
    gold_layer = GoldLayer()
    response = gold_layer.trigger_databricks_job(job_id=486921513544553)  # Replace with your actual job ID
    print(response)