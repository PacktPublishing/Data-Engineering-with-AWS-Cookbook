CREATE DATASHARE datashare_name;
ALTER DATASHARE datashare_name ADD SCHEMA schema_name;
ALTER DATASHARE datashare_name ADD TABLE schema_name.table_name;
ALTER DATASHARE datashare_name SET INCLUDENEW = TRUE FOR ALL TABLES IN SCHEMA schema_name; -- Remove "SET INCLUDENEW = TRUE" if you don't need new tables to be included
GRANT USAGE ON DATASHARE datashare_name TO ACCOUNT 'account_ID';