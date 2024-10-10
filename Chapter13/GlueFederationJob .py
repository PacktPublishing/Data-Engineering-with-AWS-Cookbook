aws glue create-job --name GlueFederationJob \
--role arn:aws:iam::<your-account-id>:role/GlueServiceRole \
--command '{"Name": "glueetl", "ScriptLocation": "s3://your-bucket/scripts/hive-metadata-federation.py"}' \
--connections '{"Connections": ["hive-metastore-connection"]}' \
--default-arguments '{
    "--TempDir": "s3://your-bucket/temp/",
    "--enable-glue-datacatalog": "true"
}'
