import boto3
import json
import os
import sys
sys.path.append("..")

from utils import bedrock, print_ww

os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
boto3_bedrock = bedrock.get_bedrock_client()

# Extract model IDs and join them with commas
model_data = boto3_bedrock.list_foundation_models()
model_ids = [model['modelId'] for model in model_data['modelSummaries']]
print("Available models:")
print("")
print('\n'.join(model_ids))
