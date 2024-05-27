# The Technical requirements section instructs you do define several variables
# that some recipes use.
# Replace the sample values with your own and then you can run this script 
# whenever you are going to do a recipe, to make sure they are set in the shell

SUBNET=subnet-XXXXXXX 

# Don’t use a trailing / in the S3 urls
S3_SCRIPTS_URL=s3://mybucket/recipes/scripts
S3_LOGS_URL=s3://mybucket/recipes/logs

KEYNAME=mykey

