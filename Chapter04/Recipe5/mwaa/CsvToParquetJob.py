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
database_name = "glue-workshop"
table_name = "data"
output_s3_path = "s3://mwaa-env-data-bucket-vk/parquet-data/"


def put_metric_data(metric_name, value):
    cloudwatch = boto3.client('cloudwatch')
    cloudwatch.put_metric_data(
        Namespace='GlueIngestion',
        MetricData=[
            {
                'MetricName': metric_name,
                'Value': value,
                'Unit': 'Count'
            },
        ]
    )


# Create a DynamicFrame from the table
dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
    database=database_name,
    table_name=table_name
)

# Convert DynamicFrame to DataFrame
data_frame = dynamic_frame.toDF()

# Write DataFrame to S3 as partitioned Parquet files
data_frame.write.mode("overwrite").partitionBy(
    "country", "state", "city").parquet(output_s3_path)

# Maximum number of retries
max_retries = 3
retries = 0
success = False

while retries < max_retries and not success:
    try:
        # Create a DynamicFrame from the table
        dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
            database=database_name,
            table_name=table_name
        )
        # Convert DynamicFrame to DataFrame
        data_frame = dynamic_frame.toDF()

        # Write DataFrame to S3 as partitioned Parquet files
        data_frame.write.mode("overwrite").partitionBy(
            "country", "state", "city").parquet(output_s3_path)

        success = True
        put_metric_data('JobSuccess', 1)
    except Exception as e:
        retries += 1
        if retries < max_retries:
            time.sleep(30)  # Wait for 30 seconds before retrying
        else:
            put_metric_data('JobFailure', 1)
            raise e

job.commit()
