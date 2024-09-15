import boto3
import json
import numbers
import pyffx
from botocore.exceptions import ClientError, BotoCoreError

def get_secret():
    try:
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(SecretId='RedshiftTokenizationSecretKey')
        secret = json.loads(response['SecretString'])
        return secret['secret_key']
    except (ClientError, BotoCoreError) as e:
        return {
            'success': False,
            'message': f'Failed to retrieve secret key: {e}'
        }

def encrypt_data(data, secret_key):
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
    try:
        if isinstance(data, numbers.Number):
            e = pyffx.Integer(secret_key.encode(), length=len(str(data)))
        else:
            e = pyffx.String(secret_key.encode(), alphabet=alphabet, length=len(data))
        encrypted_text = e.encrypt(data)
        return encrypted_text
    except Exception as e:
        return json.dumps({'success': False, 'message': f'Failed to encrypt text: {e}'})

def lambda_handler(event, context):
    secret_key = get_secret()
    return_value = dict()
    response = []
    for argument in event['arguments']:
        msg = argument[0]
        encrypted_text = encrypt_data(msg, secret_key)
        response.append(json.dumps(encrypted_text))
    
    return_value['success'] = True
    return_value['results'] = response
    
    return json.dumps(return_value)
