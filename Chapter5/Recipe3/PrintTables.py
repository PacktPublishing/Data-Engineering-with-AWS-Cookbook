from pyspark.sql import SparkSession 

spark = SparkSession.builder.enableHiveSupport( 
         ).getOrCreate() 
spark.sql("SHOW TABLES FROM cross_catalog_recipe" 
         ).show() 