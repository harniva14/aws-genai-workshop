import boto3
import json
import os

session = boto3.Session(profile_name='bedrock')
boto3_bedrock = session.client('bedrock', 'us-east-1', endpoint_url='https://bedrock.us-east-1.amazonaws.com')


# Extract model IDs and join them with commas
model_data = boto3_bedrock.list_foundation_models()
model_ids = [model['modelId'] for model in model_data['modelSummaries']]
print("Available models:")
print("")
print('\n'.join(model_ids))
