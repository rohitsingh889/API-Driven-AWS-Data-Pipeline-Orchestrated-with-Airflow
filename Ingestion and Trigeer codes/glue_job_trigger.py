
import boto3

def run_glue_job(job_name):
    glue = boto3.client("glue", region_name="us-east-1")

    response = glue.start_job_run(
        JobName=job_name
    )

    print(f"Started Glue job: {job_name}")
    print(f"Run ID: {response['JobRunId']}")
