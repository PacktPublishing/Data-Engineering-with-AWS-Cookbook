import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.{col,lit,rand}

object GlueApp {
  def main(sysArgs: Array[String]) {
    val spark = (SparkSession.builder 
       .config("spark.sql.extensions", 
             "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
       .config("spark.sql.catalog.iceberg", 
             "org.apache.iceberg.spark.SparkCatalog")
       .config("spark.sql.catalog.iceberg.warehouse", 
             "s3://glue-recipes-<your account id>/iceberg")
       .config("spark.sql.catalog.iceberg.catalog-impl", "org.apache.iceberg.aws.glue.GlueCatalog")
       .config("spark.sql.catalog.iceberg.io-impl", 
             "org.apache.iceberg.aws.s3.S3FileIO")
        .getOrCreate())
 
    val db = "iceberg_recipe_db"
    spark.sql("CREATE DATABASE IF NOT EXISTS iceberg." + db)
    val df = (spark.range(1 << 10).toDF("id") 
               .withColumn("value1", rand()) 
               .withColumn("region", lit("region1"))
             )
    df.writeTo("iceberg." + db + ".icetable").
       partitionedBy(col("region")).createOrReplace()
  }
}
