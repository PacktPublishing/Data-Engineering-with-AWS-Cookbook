# Hbase to Dynamodb
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

glueContext = GlueContext(SparkContext.getOrCreate())
dynamic_frame = glueContext.create_dynamic_frame.from_catalog(database = "your-database-name", table_name = "your-table-name")

# Transformation logic here

glueContext.write_dynamic_frame.from_options(frame = dynamic_frame, connection_type = "dynamodb", connection_options = {"dynamodb.output.tableName": "your-dynamodb-table-name"})
