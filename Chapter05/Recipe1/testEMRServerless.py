from pyspark.sql import SparkSession
spark = (SparkSession.builder.config(
         "hive.metastore.client.factory.class",
         "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory")
    .enableHiveSupport()
    .getOrCreate())
spark.sql("SHOW TABLES").show() 
