import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read the data from the Glue catalog
database = "glue-workshop"
table_name = "tbl_data"

# Create a DynamicFrame from the table
dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
    database=database,
    table_name=table_name
)

# Convert DynamicFrame to DataFrame
data_frame = dynamic_frame.toDF()

# Write DataFrame to S3 as partitioned Parquet files
output_s3_path = "s3://<Replace with Your S3 Bucket Name>/parquet-data/"
data_frame.write.mode("overwrite").partitionBy( "country", "state","city").parquet(output_s3_path)

# Commit job
job.commit()
