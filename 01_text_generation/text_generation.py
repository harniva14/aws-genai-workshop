import boto3
import json
import os
import sys
sys.path.append("..")

from utils import bedrock, print_ww

os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
boto3_bedrock = bedrock.get_bedrock_client()

modelId = 'anthropic.claude-v2' # change this to use a different version from the model provider
accept = 'application/json'
contentType = 'application/json'

# create the prompt
prompt_data = """
Command: Write an email from Bob, Customer Service Manager, to the customer "Albert E." 
who provided negative feedback on the service provided by our customer support 
engineer"""

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
        "Command:"
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