CREATE DATABASE consumer_database_name
FROM DATASHARE datashare_name OF ACCOUNT 'producer_account_ID'
NAMESPACE 'producer_cluster_namespace';


SELECT * FROM
consumer_database_name.consumer_schema_name.table_name;