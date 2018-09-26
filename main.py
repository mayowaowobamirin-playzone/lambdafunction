import boto3
import os

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    sns = boto3.client('sns')
    sns.publish(
        TopicArn = os.environ['TOPICARN'],
        Subject = 'File uploaded: ' + key,
        Message = 'File was uploaded to bucket: ' + bucket
    )
