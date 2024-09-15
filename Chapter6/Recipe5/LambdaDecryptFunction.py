import boto3
import pyffx
import json
import numbers
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

def decrypt_data(token, is_number, secret_key):
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
    try:
        if is_number:
            d = pyffx.Integer(secret_key.encode(), length=len(str(token)))
        else:
            d = pyffx.String(secret_key.encode(), alphabet=alphabet, length=len(token))
        
        decrypted_text = d.decrypt(token)
        return decrypted_text
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

    
def lambda_handler(event, context):
    secret_key = get_secret()

    return_value = dict()
    response = []
    for argument in event['arguments']:
        token = argument[0]
        is_number = argument[1]
        try:
            result = decrypt_data(token, is_number, secret_key)
            response.append(json.dumps(result))
        except Exception as e:
            return {
            'success': False,
            'error': str(e)
        }
        
    return_value['success'] = True
    return_value['results'] = response
    
    return json.dumps(return_value)