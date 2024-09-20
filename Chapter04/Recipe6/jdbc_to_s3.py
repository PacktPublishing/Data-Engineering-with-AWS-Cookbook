import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import boto3
import time

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

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

database = "relational_data"
table_name = "your_table_name"
output_s3_path = "s3://your-glue-data-bucket/ingested-data/"

max_retries = 3
retries = 0
success = False

while retries < max_retries and not success:
    try:
        dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
            database=database,
            table_name=table_name,
            transformation_ctx="dynamic_frame"
        )

        data_frame = dynamic_frame.toDF()
        data_frame.write.mode("overwrite").parquet(output_s3_path)
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
