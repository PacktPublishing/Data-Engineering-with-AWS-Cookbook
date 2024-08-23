CREATE DATABASE consumer_database_name
FROM DATASHARE datashare_name OF ACCOUNT 'producer_account_ID'
NAMESPACE 'producer_cluster_namespace';

CREATE EXTERNAL SCHEMA consumer_schema_name 
FROM redshift DATABASE consumer_database_name
SCHEMA producer_schema_name;

SELECT * FROM
consumer_database_name.consumer_schema_name.table_name;