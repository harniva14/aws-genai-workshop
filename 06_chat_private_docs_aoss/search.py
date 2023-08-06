from langchain.vectorstores import OpenSearchVectorSearch
from langchain.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3

session = boto3.Session(profile_name='bedrock')
boto3_bedrock = session.client('bedrock', 'us-east-1', endpoint_url='https://bedrock.us-east-1.amazonaws.com')

host = '<aoss_host>' # OpenSearch Serverless collection endpoint
region = 'us-east-1'

service = 'aoss'
credentials = boto3.Session().get_credentials() #add access key and secret access key which has data access permissions for the OS collections
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service,
session_token=credentials.token)

# We will be using the Titan Embeddings Model to generate our Embeddings.

titan_llm = Bedrock(model_id= "anthropic.claude-v1", client=boto3_bedrock)
bedrock_embeddings = BedrockEmbeddings(client=boto3_bedrock)

docsearch = OpenSearchVectorSearch(
    "<aoss_host>", 
    "bedrock-aos-1", 
    bedrock_embeddings, 
    http_auth=awsauth,
    timeout = 300,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

query = "Can you briefly explain what Formula 1 is?"
query_docs = docsearch.similarity_search(query, k=3)

context = ""
for i, rel_doc in enumerate(query_docs):
    context += query_docs[i].page_content
#print(context)

parameters = {
    "maxTokenCount":3000,
    "stopSequences":["."],
    "temperature":1,
    "topP":0.999
    }

prompt_data = f"""Human:Answer the question based only on the information provided in full sentences only.
<context>
{context}
</context>
<question>
{query}
</question>
Assistant:"""

output_titan_text = titan_llm(prompt_data)
print(output_titan_text)
