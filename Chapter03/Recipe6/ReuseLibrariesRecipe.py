from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, udf
from my_module import do_some_calculation, get_config_value

spark = SparkSession.builder.getOrCreate()
df = spark.range(1 << 4).toDF("id")
df = df.withColumn("config_val",
         lit(get_config_value()))
calc_udf = udf(do_some_calculation)
df = df.withColumn("calc", calc_udf(df["id"]))
df.repartition(1).write.csv("s3://glue-recipes-<your account id>/reuse_module/out")
