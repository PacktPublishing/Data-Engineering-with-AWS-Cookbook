import json
import boto3
import logging
from botocore.exceptions import ClientError


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def aws_create_EC2_tag(aws_region, instance_id: str, key_name: str, tag_value: str):
    try:
        client = boto3.client('ec2', region_name=aws_region)
        client.create_tags(Resources=[instance_id, ], Tags=[{'Key': key_name, 'Value': tag_value}, ])
        logging.info(f'Successfuly created tag {key_name} for instance {instance_id}')
    except ClientError:
        logging.info(str(ClientError))
        return False
    return True

def get_user_name(event):
    if 'userIdentity' in event['detail']:
        if event['detail']['userIdentity']['type'] == 'AssumedRole':
            user_name = str('UserName: ' + event['detail']['userIdentity']['principalId'].split(':')[1] + ', Role: ' + event['detail']['userIdentity']['sessionContext']['sessionIssuer']['userName'] + ' (role)')
        elif event['detail']['userIdentity']['type'] == 'IAMUser':
            user_name = event['detail']['userIdentity']['userName']
        elif event['detail']['userIdentity']['type'] == 'Root':
            user_name = 'root'
        else:
            logging.info('Could not determine username, unknown iam userIdentity')
            user_name = ''
    else:
        logging.info('Could not determine username, no userIdentity data in cloudtrail')
        user_name = ''
    return user_name

def lambda_handler(event, context):
    client = boto3.client('cloudtrail')
    
    resource_type = event["detail"]["eventSource"]
    logging.info('resource_type: {}'.format(resource_type))

    user_name = get_user_name(event)
    logging.info('user_name: {}'.format(user_name))

    if resource_type == "lambda.amazonaws.com":
        resource_arn = event["detail"]["responseElements"]["functionArn"]
        resource_name = event["detail"]["responseElements"]["functionName"]
        
        try:
            client = boto3.client('lambda')
            client.tag_resource(
                Resource=resource_arn,
                Tags={'Created_by': user_name}
            )
            logging.info(f"Lambda function {resource_name} tagged with username : {user_name}")
        except ClientError as e:
            logging.error(f"Error tagging Lambda function {resource_name}: {e}")

    
    elif resource_type == "ec2.amazonaws.com":
        try:
            instance_id = [x['instanceId'] for x in event['detail']['responseElements']['instancesSet']['items']]
        except Exception as e:
            instance_id = []

        aws_region = event['detail']['awsRegion']
        client = boto3.client('ec2', region_name=aws_region)
        if instance_id:
            for instance in instance_id:
                # Tagging the instance
                instance_api = client.describe_instances(InstanceIds=[instance])
                # Get all ec2 instance tags
                if 'Tags' in instance_api['Reservations'][0]['Instances'][0]:
                    instance_tags = instance_api['Reservations'][0]['Instances'][0]['Tags']
                else:
                    instance_tags = []
                # Check if 'Name' tag exists for ec2 instance
                if instance_tags:
                    instance_name = [x['Value'] for x in instance_tags if x['Key'] and x['Key'] == 'Name']
                    if instance_name:
                        instance_name = instance_name[0]
                else:
                    instance_name = ''
                # Check if 'Owner' tag exist in instance tags
                if instance_tags:
                    if not any(keys.get('Key') == 'Owner' for keys in instance_tags):
                        logging.info(f'Creating Owner tag for instance: {instance}')
                        aws_create_EC2_tag(aws_region, instance, 'Owner', user_name)
                    else:
                        logging.info(f'Owner tag already exist for instance {instance}')
                else:
                    logging.info(f'Instance {instance} has no tags, we will tag it with Owner tag')
                    aws_create_EC2_tag(aws_region, instance, 'Owner', user_name)
        
                instance_volumes = [x['Ebs']['VolumeId'] for x in instance_api['Reservations'][0]['Instances'][0]['BlockDeviceMappings']]
                # Check if volume already has tags
                for volume in instance_volumes:
                    response = client.describe_volumes(VolumeIds=[volume])
                    volume_tags = [x['Tags'] for x in response['Volumes'] if 'Tags' in x]
                    if volume_tags:
                        if any(keys.get('Key') == 'Owner' and keys.get('Key') == 'AttachedInstance' for keys in
                                   volume_tags[0]):
                            logging.info(f'Volume {volume} of instance: {instance}, is already tagged')
                            continue
                        if not any(keys.get('Key') == 'Owner' for keys in volume_tags[0]):
                            logging.info('Creating Owner tag for volume {volume} of instance: {instance}')
                            aws_create_EC2_tag(aws_region, volume, 'Owner', user_name)
                    else:
                        logging.info(f'Volume {volume} is not tagged, adding Owner tag')
                        aws_create_EC2_tag(aws_region, volume, 'Owner', user_name)

    elif resource_type == "s3.amazonaws.com":
        s3 = boto3.resource('s3')
        bucket_name = event['detail']['requestParameters']['bucketName']
        logging.info('Bucket Name: {}'.format(bucket_name))
        try:
            bucket_tagging = s3.BucketTagging(bucket_name)
            try:
                tags = bucket_tagging.tag_set
            except ClientError as e:
                if e.response['Error']['Code'] == 'NoSuchTagSet':
                    logging.info(f'Bucket {bucket_name} has no tags, creating a new tag set')
                    tags = []
                else:
                    raise
            tags.append({'Key': 'Created_by', 'Value': user_name})
            bucket_tagging.put(Tagging={'TagSet': tags})
        except ClientError as e:
            logging.info(e)
    