aws lambda add-permission \
    --function-name your_function_arn \
    --principal config.amazonaws.com \
    --statement-id AllowConfigInvoke \
    --action lambda:InvokeFunction \
    --source-account your_aws_account_id