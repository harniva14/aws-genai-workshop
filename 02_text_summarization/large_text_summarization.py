import boto3
import json
import os

session = boto3.Session(profile_name='bedrock')
boto3_bedrock = session.client('bedrock', 'us-east-1', endpoint_url='https://bedrock.us-east-1.amazonaws.com')

from langchain.llms.bedrock import Bedrock

#prompt_data = "Summarize Title I"

llm = Bedrock(model_id="anthropic.claude-v2", 
              model_kwargs ={
                "max_tokens_to_sample": 5000,
                "temperature": 0.5,
                "top_p": 1,
                "stop_sequences": [
                    "Here is a concise summary"
                ]},
              client=boto3_bedrock)

text_file = "hipaa.txt"

with open(text_file, "r") as file:
    letter = file.read()
    
llm.get_num_tokens(letter)

from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n"], chunk_size=6000, chunk_overlap=50
)

docs = text_splitter.create_documents([letter])

num_docs = len(docs)

num_tokens_first_doc = llm.get_num_tokens(docs[0].page_content)

print(
    f"Now we have {num_docs} documents and the first one has {num_tokens_first_doc} tokens"
)

# Set verbose=True if you want to see the prompts being used
from langchain.chains.summarize import load_summarize_chain
summary_chain = load_summarize_chain(llm=llm, chain_type="map_reduce", verbose=False)

output = summary_chain.run(docs)

print(output.strip())
