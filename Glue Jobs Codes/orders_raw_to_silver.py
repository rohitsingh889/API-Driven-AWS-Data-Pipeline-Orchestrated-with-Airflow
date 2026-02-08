import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# -----------------------------
# Get job arguments
# -----------------------------
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# -----------------------------
# Initialize Spark & Glue
# -----------------------------
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# -----------------------------
# READ raw JSON from S3
# -----------------------------
raw_df = spark.read.json(
    "s3://rohit-ecommerce-data-lake/raw/orders/"
)

print(f"Raw record count: {raw_df.count()}")

# -----------------------------
# WRITE as Parquet to S3
# -----------------------------
raw_df.write.mode("overwrite").parquet(
    "s3://rohit-ecommerce-data-lake/processed/orders/parquet/"
)

# -----------------------------
# Commit job
# -----------------------------
job.commit()
