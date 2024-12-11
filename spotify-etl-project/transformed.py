import json
import boto3
import datetime

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the source S3 bucket and object key from the event
    source_bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    print(event)
    # Define the destination S3 bucket
    destination_bucket_name = 'spotify-transformed-bucket-asad'
    
    # Fetch the object from the source S3 bucket
    response = s3.get_object(Bucket=source_bucket_name, Key=object_key)
    data = response['Body'].read().decode('utf-8')
    
    # Parse the JSON data
    api_data = json.loads(data)
    
    # Transformation: Add a timestamp to the data
    api_data["timestamp"] = datetime.datetime.now().isoformat()
    
    # Convert the transformed data to JSON
    transformed_data_json = json.dumps(api_data)
    
    # Define the new object key with the prefix for the destination bucket
    transformed_prefix = 'transformed/'
    transformed_object_key = f'{transformed_prefix}{object_key}'
    
    # Upload the transformed data to the destination S3 bucket
    s3.put_object(
        Bucket=destination_bucket_name,
        Key=transformed_object_key,
        Body=transformed_data_json,
        ContentType='application/json'
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Successfully uploaded transformed data to {destination_bucket_name}/{transformed_object_key}')
    }

