import json
import boto3
glue=boto3.client('glue');

def lambda_handler(event, context):
    #TODO implement
    response = glue.start_crawler(
    Name='spotift-transformed-crawler'
    #print(f"{Name} sucessfully run")
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }