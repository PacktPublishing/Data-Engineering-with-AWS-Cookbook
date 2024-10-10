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

# Reading from the Hive Metastore
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="hive_database_name",
    table_name="hive_table_name"
)
# Writing data to S3 (you can modify the output path or format)
glueContext.write_dynamic_frame.from_options(
    frame=datasource,
    connection_type="s3",
    connection_options={"path": "s3://your-bucket/output-path"},
    format="parquet"
)
job.commit()
