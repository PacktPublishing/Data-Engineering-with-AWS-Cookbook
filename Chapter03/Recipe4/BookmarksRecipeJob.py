import sys
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

dynf = glueContext.create_dynamic_frame_from_options(
    connection_type = "s3", 
    connection_options = {
        "paths": ["s3://glue-recipes-<your account id>/bookmarkrecipe/input/"],
        "boundedFiles": 5
    },
    transformation_ctx="json_source",
    format = "json"
)

glueContext.write_dynamic_frame.from_options(
    frame=dynf.repartition(1),
    connection_type='s3',
    format='json',
    transformation_ctx="csv_dst",
    connection_options={"path": "s3://glue-recipes-<your account id>/bookmarkrecipe/output/"
    }
)

job.commit()
