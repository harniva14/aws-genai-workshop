import boto3
import json
import os
import argparse

session = boto3.Session(profile_name='bedrock')
boto3_bedrock = session.client('bedrock', 'us-east-1', endpoint_url='https://bedrock.us-east-1.amazonaws.com')

parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str, required=True, help="Prompt for text generation")
parser.add_argument("--modelid", type=str, required=True, help="Model ID for generation")
args = parser.parse_args()

modelId = args.modelid  # Using Claude model
accept = 'application/json'
contentType = 'application/json'

# Read the prompt from a text file
with open(args.file, "r") as file:
    prompt_data = "Please provide a summary of the following text in one small paragraph. \n" + file.read().strip()

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