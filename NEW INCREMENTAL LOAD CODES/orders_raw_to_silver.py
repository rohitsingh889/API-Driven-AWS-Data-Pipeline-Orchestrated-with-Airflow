import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'run_date'])  # ✅ NEW

run_date = args['run_date']

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# ✅ READ ONLY CURRENT PARTITION
raw_df = spark.read.json(
    f"s3://rohit-ecommerce-data-lake/raw/orders/ingestion_date={run_date}/"
)

print(f"Raw records for {run_date}: {raw_df.count()}")

raw_df.write \
    .mode("append") \                # ✅ APPEND
    .parquet("s3://rohit-ecommerce-data-lake/processed/orders/parquet/")

job.commit()
