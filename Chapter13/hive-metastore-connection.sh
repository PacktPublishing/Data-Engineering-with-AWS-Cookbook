aws glue create-connection --name hive-metastore-connection \
--connection-input '{
    "Name": "hive-metastore-connection",
    "Description": "JDBC connection to Hive Metastore",
    "ConnectionType": "JDBC",
    "ConnectionProperties": {
        "JDBC_CONNECTION_URL": "jdbc:mysql://<hive-metastore-host>:3306/hive_metastore",
        "USERNAME": "hiveuser",
        "PASSWORD": "hivepassword"
    },
    "PhysicalConnectionRequirements": {
        "AvailabilityZone": "us-east-1a",
        "SubnetId": "subnet-0bb1c79de3EXAMPLE"
    }
}'
