import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import boto3

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read the data from the Glue catalog
database = "csv_database"
table_name = "csv_table"

# Create a DynamicFrame from the table
dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
    database=database,
    table_name=table_name
)

# Convert DynamicFrame to DataFrame
data_frame = dynamic_frame.toDF()

# Write DataFrame to S3 as partitioned Parquet files by 'city', 'state', and 'country'
output_s3_path = "s3://<Replace with your-S3 bucket Name>/parquet-data/"
data_frame.write.mode("overwrite").partitionBy(
    "city", "state", "country").parquet(output_s3_path)

# Emit success metric to CloudWatch
cloudwatch = boto3.client('cloudwatch')
cloudwatch.put_metric_data(
    Namespace='GluePipelineMetrics',
    MetricData=[
        {
            'MetricName': 'JobSuccess',
            'Dimensions': [
                {
                    'Name': 'JobName',
                    'Value': args['JOB_NAME']
                },
            ],
            'Value': 1,
            'Unit': 'Count'
        },
    ]
)

# Commit job
job.commit()
