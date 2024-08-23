echo placeholder > template_file.csv
gzip template_file.csv
mkdir smallfiles_recipe_input
# Generate the files locally
for i in {1..10000}; do
 cp template_file.csv.gz smallfiles_recipe_input/$i.csv.gz;
 if (($i % 1000 == 0)); then echo -n .; fi
done
echo
# Upload to s3 and cleanup the local files
rm template_file.csv.gz
S3_INPUT_URL=s3://$GLUE_BUCKET/smallfiles_input/
aws s3 sync smallfiles_recipe_input $S3_INPUT_URL
rm smallfiles_recipe_input/*.csv.gz
rmdir smallfiles_recipe_input
S3_OUPUT_URL=s3://$GLUE_BUCKET/smallfiles_output/