
def lambda_handler(event, context):
    # Sample data processing logic
    processed_data = event['message'].upper()
    return {
        "processedMessage": processed_data
    }
