import json
import boto3


def lambda_handler(event, context):
    glue = boto3.client('glue')

    # Start the Glue workflow
    workflow_name = 'CsvToParquetWorkflow'
    response = glue.start_workflow_run(Name=workflow_name)

    return {
        'statusCode': 200,
        'body': json.dumps('Workflow started: {}'.format(response['RunId']))
    }
