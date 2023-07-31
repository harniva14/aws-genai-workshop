import boto3
import json
import os
import argparse

session = boto3.Session(profile_name='bedrock')
boto3_bedrock = session.client('bedrock', 'us-east-1', endpoint_url='https://bedrock.us-east-1.amazonaws.com')

parser = argparse.ArgumentParser()
parser.add_argument("--prompt", type=str, required=True, help="Prompt for text generation")
parser.add_argument("--modelid", type=str, required=True, help="Model ID for generation")
args = parser.parse_args()

modelId = args.modelid
accept = 'application/json'
contentType = 'application/json'

# create the prompt
prompt_data = args.prompt

titan_input = json.dumps({
    "inputText": prompt_data, 
    "textGenerationConfig" : { 
        "maxTokenCount": 512,
        "stopSequences": [],
        "temperature":0.1,  
        "topP":0.9
    }
    })

claude_input = json.dumps({
    "prompt": prompt_data, 
    "max_tokens_to_sample": 500,
    "temperature": 0.5,
    "top_k": 250,
    "top_p": 1,
    "stop_sequences": [
    ]
})

if modelId == "amazon.titan-tg1-large":
    response = boto3_bedrock.invoke_model(body=titan_input, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get("body").read())
    print(response_body.get("results")[0].get("outputText"))
    
if modelId == "anthropic.claude-v2":
    response = boto3_bedrock.invoke_model(body=claude_input, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())
    print(response_body['completion'])