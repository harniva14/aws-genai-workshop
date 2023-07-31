import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.llms import HuggingFaceHub
from langchain.vectorstores.pgvector import PGVector
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms.bedrock import Bedrock
import os
import psycopg2
import boto3

# Load environment variables from the env.example file
load_dotenv('env.example')

session = boto3.Session(profile_name='bedrock')
boto3_bedrock = session.client('bedrock', 'us-east-1', endpoint_url='https://bedrock.us-east-1.amazonaws.com')

# Access the environment variables
huggingface_api_token = os.getenv('HUGGINGFACEHUB_API_TOKEN')
hub_instance = HuggingFaceHub(huggingfacehub_api_token=huggingface_api_token)

pgvector_host = os.getenv('PGVECTOR_HOST')
CONNECTION_STRING = PGVector.connection_string_from_db_params(                                                  
    driver = '',
    user = 'Someuser',                                      
    password = 'SomePassword',                                  
    host = pgvector_host,                                            
    port = '5432',                                          
    database = 'new_dbname'                                       
)
CONNECTION_STRING = CONNECTION_STRING.replace("postgresql+://", "postgresql://")
print(CONNECTION_STRING)   


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
     )

    chunks = text_splitter.split_text(text)
    return chunks

def ensure_database_exists():
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='Someuser',
            password='SomePassword',
            host=pgvector_host,
            port='5432'
        )
        print("conn created")
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS new_dbname;")
        cur.execute(f"CREATE DATABASE new_dbname;")
        print("Database created successfully")
        cur.close()
        conn.close()
        conn = psycopg2.connect(
            dbname='new_dbname',
            user = 'Someuser',                                      
            password = 'SomePassword',   
            host=pgvector_host,
            port='5432'
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"CREATE EXTENSION vector;")
    except Exception as e:
        print(f"Error: Harniva {e}")

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    vectorstore = PGVector.from_texts(texts=text_chunks, embedding=embeddings,connection_string=CONNECTION_STRING)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = Bedrock(model_id="anthropic.claude-v2", 
              model_kwargs ={
                "max_tokens_to_sample": 1000,
                "temperature": 0.5,
                "top_k": 250,
                "top_p": 1
              },
              client=boto3_bedrock)
    #llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":1024}, huggingfacehub_api_token=huggingface_api_token)

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()
    ensure_database_exists()
    st.set_page_config(page_title="Streamlit Question Answering App",
                       page_icon=":books::parrot:")
    st.write(css, unsafe_allow_html=True)

    st.sidebar.markdown(
    """
    ### Instructions:
    1. Browse and upload PDF files
    2. Click Process
    3. Type your question in the search bar to get more insights
    """
)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("GenAI Q&A with pgvector and Amazon Aurora PostgreSQL :books::parrot:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)


if __name__ == '__main__':
    main()
