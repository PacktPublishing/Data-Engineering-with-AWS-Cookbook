from pyspark.context import SparkContext
from awsglue.context import GlueContext
glueContext = GlueContext(SparkContext())
dynf = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={
        "paths": ["s3://glue-recipes-<your account id>-ap-south-1/smallfiles_input/"],
        "useS3ListImplementation": True,
        "groupFiles": "inPartition",
        "groupSize": "100000"
    },
    format="csv"
)
writer=dynf.toDF().write.format("parquet") 
writer.mode("overwrite").save("s3://glue-recipes-<your account id>-ap-south-1/smallfiles_output/")
