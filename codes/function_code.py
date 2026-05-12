import json
import base64
import gzip
import boto3
from datetime import datetime

# Initialize AWS Services
sns = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('DetectedAnomalies')

# Replace this with your actual SNS Topic ARN
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:017540984214:LogAlerts"

def lambda_handler(event, context):
    cw_data = event['awslogs']['data']
    compressed_payload = base64.b64decode(cw_data)
    uncompressed_payload = gzip.decompress(compressed_payload)
    payload = json.loads(uncompressed_payload)

    for log_event in payload['logEvents']:
        message = log_event['message']
        
        if "ERROR" in message:
            timestamp = datetime.now().isoformat()
            
            # 1. Send SNS Alert
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="⚠️ LOG ANALYTICS ALERT",
                Message=f"Anomaly detected:\n\n{message}"
            )
            
            # 2. Save to DynamoDB
            table.put_item(
                Item={
                    'Timestamp': timestamp,
                    'LogMessage': message,
                    'Status': 'Critical'
                }
            )
            
    return {"statusCode": 200, "body": "Logged to DynamoDB"}