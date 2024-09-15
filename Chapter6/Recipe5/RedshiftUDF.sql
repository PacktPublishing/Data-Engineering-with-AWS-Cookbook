CREATE OR REPLACE
EXTERNAL FUNCTION PII_tokenize_str (value VARCHAR)
RETURNS VARCHAR
STABLE
LAMBDA 'your_lambda_function_name'
IAM_ROLE 'your_redshift_role_arn';

CREATE OR REPLACE
EXTERNAL FUNCTION PII_tokenize_int (value INT)
RETURNS VARCHAR
STABLE
LAMBDA 'your_lambda_function_name'
IAM_ROLE 'your_redshift_role_arn';