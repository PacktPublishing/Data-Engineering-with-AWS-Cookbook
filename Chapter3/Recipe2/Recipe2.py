import sys
from datetime import datetime
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job 

args = getResolvedOptions(sys.argv, 
             ['JOB_NAME', 'DATE'])
data_date = args["DATE"]
date_format = '%Y-%m-%d'
if data_date == 'TODAY':
  data_date = datetime.today().strftime(date_format)

print(f"Running job for date: '{data_date}'")
