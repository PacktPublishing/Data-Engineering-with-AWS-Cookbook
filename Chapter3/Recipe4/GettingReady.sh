RECIPE_S3_SRC=s3://$GLUE_BUCKET/bookmarkrecipe/input/
RECIPE_S3_DST=s3://$GLUE_BUCKET/bookmarkrecipe/output/

mkdir ./bookmark_recipe_data/
for i in 1 2 3 4 5 6 7 8 9 10;do
 echo '{"file_number": '$i'}' > \
 ./bookmark_recipe_data/$i.json
done
aws s3 sync ./bookmark_recipe_data/ $RECIPE_S3_SRC
rm ./bookmark_recipe_data/*.json
rmdir ./bookmark_recipe_data/