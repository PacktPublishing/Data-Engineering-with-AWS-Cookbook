from pyspark.context import SparkContext
from pyspark.sql.functions import *
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame

glueContext = GlueContext(SparkContext())
spark = glueContext.spark_session

s3_output_path = "s3://glue-recipes-<your account id>/retry_recipe"
# The first attempt is just an hexadecimal number
# the retries have a suffix with the retry number 
is_retry = "_attempt_" in   spark.conf.get("spark.glue.JOB_RUN_ID")

df = spark.range(1 << 10, numPartitions=4)
# Simulate the retry works ok
if is_retry:
    df = df.withColumn("fail", lit(False))
else:    
    df = df.withColumn("fail", expr( 
        f"case when id=10 then true else false end"))

# Introduce a failure when flagged
fail_udf = udf(lambda fail: 1/0 if fail else fail)
df = df.withColumn("fail", fail_udf(df.fail))
failDf = DynamicFrame.fromDF(df, glueContext, "")
glueContext.write_dynamic_frame.from_options(
    frame=failDf,
    connection_type='s3',
    format='csv',
    connection_options={"path": s3_output_path}
) 
