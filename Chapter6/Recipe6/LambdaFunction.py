import boto3
import json
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    invoking_event = json.loads(event['invokingEvent'])
    configuration_item = invoking_event['configurationItem']
    
    # Extract the bucket name from the configurationItem
    bucket_name = configuration_item['configuration']['name']
    s3_client = boto3.client('s3')
    compliance_type = 'NON_COMPLIANT'
    
    try:
        lifecycle_policy = s3_client.get_bucket_lifecycle_configuration(Bucket=bucket_name)
        for rule in lifecycle_policy.get('Rules', []):
            if (
                ('Transitions' in rule and any(
                    'StorageClass' in transition and transition.get('StorageClass', '') in ['GLACIER', 'GLACIER_DEEP_ARCHIVE']
                    for transition in rule['Transitions'])
                ) or 
                ('NoncurrentVersionTransition' in rule and any(
                    'StorageClass' in transition and transition.get('StorageClass', '') in ['GLACIER', 'GLACIER_DEEP_ARCHIVE']
                    for transition in rule.get('NoncurrentVersionTransition', []))
                ) or
                ('Expiration' in rule and 'Days' in rule.get('Expiration', {})) or
                ('NoncurrentVersionExpiration' in rule and 'NoncurrentDays' in rule.get('NoncurrentVersionExpiration', {}))
            ):
                compliance_type = 'COMPLIANT'
                message = 'The bucket has a lifecycle policy with expiration after specified days.'
                break
        else:
            message = 'The bucket lifecycle policy does not archive or delete objects.'
    
    except ClientError as e:
        message = f"Error getting lifecycle configuration for bucket {bucket_name}: {e}"
    
    evaluation_result = {
        'ComplianceResourceType': 'AWS::S3::Bucket',
        'ComplianceResourceId': bucket_name,
        'ComplianceType': compliance_type,
        'OrderingTimestamp': configuration_item['configurationItemCaptureTime'],
        'Annotation': message
    }
    
    config_client = boto3.client('config')
    response = config_client.put_evaluations(
        Evaluations=[evaluation_result],
        ResultToken=event['resultToken']
    )
    
    return response