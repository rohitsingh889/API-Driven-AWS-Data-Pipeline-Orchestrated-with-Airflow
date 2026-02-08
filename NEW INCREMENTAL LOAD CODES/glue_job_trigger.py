import boto3

def run_glue_job(job_name, run_date):  # ✅ NEW PARAM
    glue = boto3.client("glue", region_name="us-east-1")

    response = glue.start_job_run(
        JobName=job_name,
        Arguments={                 #  NEW 
            "--run_date": run_date
        }
    )

    print(f"Started Glue job: {job_name} for {run_date}")
