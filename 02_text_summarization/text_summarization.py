import boto3
import json
import os
import sys

sys.path.append("..")
from utils import bedrock, print_ww

os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
boto3_bedrock = bedrock.get_bedrock_client()

modelId = 'anthropic.claude-v2'  # Using Claude model
accept = 'application/json'
contentType = 'application/json'

# Read the prompt from a text file
with open("letter.txt", "r") as file:
    prompt_data = "Please provide a summary of the following text. \n" + file.read().strip()

claude_input = json.dumps({
    "prompt": prompt_data,
    "max_tokens_to_sample": 500,
    "temperature": 0.5,
    "top_k": 250,
    "top_p": 1,
    "stop_sequences": [
        "Command:"
    ]
})

response = boto3_bedrock.invoke_model(body=claude_input, modelId=modelId, accept=accept, contentType=contentType)
response_body = json.loads(response.get('body').read())
print(response_body['completion'])