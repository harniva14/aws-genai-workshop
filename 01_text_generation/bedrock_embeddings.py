import boto3
import json
import os
import sys
sys.path.append("..")

from utils import bedrock, print_ww

os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
boto3_bedrock = bedrock.get_bedrock_client()


prompt_data = "Amazon Bedrock supports foundation models from industry-leading providers such as \
AI21 Labs, Anthropic, Stability AI, and Amazon. Choose the model that is best suited to achieving your unique goals."

body = json.dumps({"inputText": prompt_data})
modelId = "amazon.titan-e1t-medium"  # change this to use a different version from the model provider
accept = "application/json"
contentType = "application/json"

response = boto3_bedrock.invoke_model(
    body=body, modelId=modelId, accept=accept, contentType=contentType
)
response_body = json.loads(response.get("body").read())

embedding = response_body.get("embedding")
print(f"The embedding vector has {len(embedding)} values\n{embedding[0:5]+['...']+embedding[-3:]}")