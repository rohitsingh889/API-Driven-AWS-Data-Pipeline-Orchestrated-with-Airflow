import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

from pyspark.sql.functions import explode, col, to_date, year, month

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
# READ SILVER data (Parquet)
# -----------------------------
df = spark.read.parquet(
    "s3://rohit-ecommerce-data-lake/processed/orders/parquet/"
)

print(f"Silver record count: {df.count()}")

# -----------------------------
# TRANSFORM (REAL ETL)
# -----------------------------

# Explode products array
exploded_df = df \
    .withColumn("product", explode(col("products"))) \
    .select(
        col("id").alias("order_id"),
        col("userid").alias("user_id"),
        col("product.productid").alias("product_id"),
        col("product.quantity").alias("quantity"),
        to_date(col("date")).alias("order_date"),
        col("ingestion_date")
    )

# Add partition columns
final_df = exploded_df \
    .withColumn("order_year", year(col("order_date"))) \
    .withColumn("order_month", month(col("order_date")))

# -----------------------------
# WRITE GOLD table
# -----------------------------
final_df.write \
    .mode("overwrite") \
    .partitionBy("order_year", "order_month") \
    .parquet(
        "s3://rohit-ecommerce-data-lake/gold/orders/"
    )

# -----------------------------
# Commit job
# -----------------------------
job.commit()
