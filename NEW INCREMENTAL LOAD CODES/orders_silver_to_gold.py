import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

from pyspark.sql.functions import (
    explode,
    col,
    to_date,
    year,
    month
)

# --------------------------------------------------
# Get job arguments
# --------------------------------------------------
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'run_date'])
run_date = args['run_date']

# --------------------------------------------------
# Initialize Spark & Glue
# --------------------------------------------------
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args['JOB_NAME'], args)

print(f"Starting Gold job for run_date = {run_date}")

# --------------------------------------------------
# Read Silver data
# --------------------------------------------------
silver_df = spark.read.parquet(
    "s3://rohit-ecommerce-data-lake/processed/orders/parquet/"
)

print(f"Total silver records: {silver_df.count()}")

# --------------------------------------------------
# Incremental filter
# --------------------------------------------------
incremental_df = silver_df.filter(col("ingestion_date") == run_date)

incremental_count = incremental_df.count()
print(f"Incremental records for {run_date}: {incremental_count}")

# --------------------------------------------------
# SAFETY: skip empty incremental batch
# --------------------------------------------------
if incremental_count == 0:
    print("No new data for this run. Skipping Gold write.")
    job.commit()
    sys.exit(0)

# --------------------------------------------------
# Transform (Gold logic)
# --------------------------------------------------
exploded_df = (
    incremental_df
    .withColumn("product", explode(col("products")))
    .select(
        col("id").alias("order_id"),
        col("userid").alias("user_id"),
        col("product.productid").alias("product_id"),
        col("product.quantity").alias("quantity"),
        to_date(col("date")).alias("order_date"),
        col("ingestion_date")
    )
)

final_df = (
    exploded_df
    .withColumn("order_year", year(col("order_date")))
    .withColumn("order_month", month(col("order_date")))
)

print(f"Final Gold records to write: {final_df.count()}")

# --------------------------------------------------
# Write Gold data (partitioned)
# --------------------------------------------------
final_df.write \
    .mode("overwrite") \
    .partitionBy("order_year", "order_month") \
    .parquet("s3://rohit-ecommerce-data-lake/gold/orders/")

print("Gold write completed successfully")

# --------------------------------------------------
# Commit job
# --------------------------------------------------
job.commit()
