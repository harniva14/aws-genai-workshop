from __future__ import annotations
import boto3
import json
import os
import sys
import time
from urllib.request import urlretrieve
import numpy as np
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain.vectorstores import OpenSearchVectorSearch
from langchain.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

session = boto3.Session(profile_name='bedrock')
boto3_bedrock = session.client('bedrock', 'us-east-1', endpoint_url='https://bedrock.us-east-1.amazonaws.com')

## set up opensearch
host = '<aoss_host>' # OpenSearch Serverless collection endpoint
region = 'us-east-1' 

service = 'aoss'
credentials = boto3.Session().get_credentials() #add access key and secret access key which has data access permissions for the OS collections
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service,
session_token=credentials.token)

# We will be using the Titan Embeddings Model to generate our Embeddings.
titan_llm = Bedrock(model_id= "anthropic.claude-v2", client=boto3_bedrock)
bedrock_embeddings = BedrockEmbeddings(client=boto3_bedrock)

# specify the directory you want to scan for PDF files
directory = './data/'

# load the files from disk
loader = PyPDFDirectoryLoader(directory)

documents = loader.load()
# - in our testing Character split works better with this PDF data set
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 1000,
    chunk_overlap  = 100,
)
docs = text_splitter.split_documents(documents)

avg_doc_length = lambda documents: sum([len(doc.page_content) for doc in documents])//len(documents)
avg_char_count_pre = avg_doc_length(documents)
avg_char_count_post = avg_doc_length(docs)
print(f'Average length among {len(documents)} documents loaded is {avg_char_count_pre} characters.')
print(f'After the split we have {len(docs)} documents more than the original {len(documents)}.')
print(f'Average length among {len(docs)} documents (after split) is {avg_char_count_post} characters.')

docsearch = OpenSearchVectorSearch.from_documents(
    docs, 
    bedrock_embeddings, 
    ids=None,
    opensearch_url="<aoss_host>", 
    http_auth=awsauth,
    timeout = 300,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection,
    index_name = "bedrock-aos-1"
)