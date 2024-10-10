aws glue create-crawler --name hive-crawler \
--role arn:aws:iam::<your-account-id>:role/GlueServiceRole \
--database-name hive_database \
--targets '{
    "JdbcTargets": [{
        "ConnectionName": "hive-metastore-connection",
        "Path": "hive_metastore"
    }]
}'
