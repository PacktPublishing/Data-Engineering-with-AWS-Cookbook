GLUE_ROLE=AWSGlueServiceRole-Recipe

aws iam put-role-policy --role-name $GLUE_ROLE \
--policy-name GlueSessions --policy-document '{"Version":
"2012-10-17", "Statement": [{"Effect": "Allow",
"Action":["glue:*Session", "glue:RunStatement", 
"iam:PassRole"], "Resource":["*"]}]}'
