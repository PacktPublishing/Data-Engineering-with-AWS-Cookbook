import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def publish_to_sns(message):
    try:
        sns_client = boto3.client("sns")
        # add any proccessing required on the file or extract certain fields before publishing the message.
        sns_client.publish(
            TopicArn="yourSNSTopicArn", Message=message, Subject="emailSubject"
        )
        logging.info("Published SNS message successfully")
    except ClientError:
        logging.info("Failed to publish SNS due to: {}".format(str(ClientError)))
        return False
    return True


def lambda_handler(event, context):
    # retrieve S3 file name
    s3_event = event["Records"][0]["s3"]
    object_key = s3_event["object"]["key"]
    bucket_name = s3_event["bucket"]["name"]
    s3_client = boto3.client("s3")
    # retrieve file from S3 by its object key
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    file_content = response["Body"].read().decode("utf-8")
    # publish S3 file content to SNS
    publish_to_sns(file_content)
    return {"statusCode": 200}