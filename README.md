# AWS GenAI Workshop

## Agenda
- **00 Pre-requisites**
    - Storage expansion
    - Upgrading python to 3.9.9
    - Setting up environment to interact with Amazon Bedrock
    - Installing required dependencies
    - Creating RDS postgres DB
- **01 - Text generation**
    - Listing all available models
    - With Titan and Claude models
    - Embeddings with Titan
- **02 - Text summarization**
    - Text summarization with pre-downloaded file
    - Large text summarization with chunking
- **03 - Image generation**
    - Using the Stable Diffusion model
- **04 - Private Chatbot**
    - Chat with your private documents (streamlit and pgvector)
- **05 - CodeWhisperer**
  - In C9 environment

## 00. Pre-requisites
1. Create a Cloud9 environment
    - Within the AWS Management Console navigate to the [Cloud9 console](https://us-east-1.console.aws.amazon.com/cloud9control/home?region=us-east-1)
    - Select **Create environment**.
    - Enter `genai-workshop` in the Name
    - Select `m5.large` instance type
    - Click **Create**

2. Open Cloud9 IDE. In Cloud9, click (+) sign and select **New Terminal**. Then clone the repository using the below command.

    ```
    git clone https://github.com/harniva14/aws-genai-workshop.git
    ```

3. Extend the file system storage to 50 GB so we have enough storage space to install all the required dependencies

    ```
    cd /home/ec2-user/environment/aws-genai-workshop/00_setup/
    ```

    ```
    bash expand_storage.sh
    ```

4. Upgrade to python3.9 which is compatible with the dependencies. This may take a few minutes. Continue with 5 and 6 below while you wait for this to finish.

    ```
    bash update_python.sh
    ```

    Check the python version and make sure it is 3.9.9

    ```
    python --version
    ```

5. Turn off AWS Managed temporary credentials and Git Auto refresh
    - In Cloud9 environment click the gear icon on top right
    - Go to **AWS Settings** option
    - Toggle to turn off **AWS managed temporary credentials**
    - Next, go to **Project settings** > **Git**
    - Toggle off **Git: Autorefresh**

6. Update IAM role so we can deploy some resources in this account
    - Go to [IAM console](https://us-east-1.console.aws.amazon.com/iamv2/home?region=us-east-1#)
    - Click on **Roles** on left navigation menu
    - Search for **AWSCloud9SSMAccessRole**
    - Click on **Add Permission**. Then click **Attach policies**
    - Search for **AdministratorAccess** in the search bar select the role name 
    - Click **Add Permissions**


7. Install required AWS and external dependencies to access Amazon Bedrock APIs.
    
    Run the script below

    ```
    bash install_aws_dependencies.sh
    ```
    Next, run the script below to install external dependencies
    
    ```
    pip install pydantic fpdf langchain transformers pillow==9.5.0
    ```

8. Open **`00_setup/creds_setup.sh`** file. Then, update the file with the information provided. Then go back to the terminal window and run the below script.

    ```
    bash creds_setup.sh
    ```

9. In the terminal window, execute the below command to deploy the CloudFormation stack in your account. This stack deploys a VPC, VPC resources and a PostgreSQL database that you will need for later exercise.

    ```
    aws cloudformation create-stack --region us-east-1 \
    --stack-name PostgresDBStack \ 
    --template-body file://deploy_db_stack.yaml
    ```


## 01. Text generation with Amazon Bedrock

1. Go to the appropriate folder

    ```
    cd /home/ec2-user/environment/aws-genai-workshop/01_text_generation/
    ```

2. List all the available Amazon Bedrock foundational models

    ```
    python print_bedrock_models.py
    ```

    You would see the following output

    ```
    amazon.titan-tg1-large
    amazon.titan-e1t-medium
    stability.stable-diffusion-xl
    ai21.j2-grande-instruct
    ai21.j2-jumbo-instruct
    anthropic.claude-instant-v1
    anthropic.claude-v1
    anthropic.claude-v2
    ```


3. Use the below command to invoke the Bedtock API and generate a text from the input prompt. In this example, we use the Amazon's Titan text model

    ```
    python text_generation.py \
    --prompt "Explain quantum computing like I am 5 years old" \
    --modelid "amazon.titan-tg1-large"
    ```


4. Now we will run the same script with a different text model. We will use Anthropic's Claude2 model.

    ```
    python text_generation.py \
    --prompt "Explain quantum computing like I am 5 years old" \
    --modelid "anthropic.claude-v2"
    ```


5. Vector Embeddings

Word Embeddings or Word vectorization is a methodology in NLP to map words or phrases from vocabulary to a corresponding vector of real numbers which used to find word predictions, word similarities/semantics.

In simple terms, vector embeddings are like a secret language that computers use to represent and understand complex data, like words or images, in a simpler and more compact form. Think of it as turning a big, detailed painting into a small doodle that still captures the main idea. This makes it easier for the computer to work with and generate new content.

Run the embeddings script to convert text in to vector embeddings.

```
python bedrock_embeddings.py \
--modelid "amazon.titan-e1t-medium" \
--text "Amazon Bedrock supports foundation models from \
industry-leading providers such as \
AI21 Labs, Anthropic, Stability AI, and Amazon. \ 
Choose the model that is best suited to achieving your unique goals."
```


## 02. Text Summarization with Amazon Bedrock

1. Go to the appropriate folder

    ```
    cd /home/ec2-user/environment/aws-genai-workshop/02_text_summarization/
    ```


2. In the folder `02_text_summarization`, there is a file `letter.txt`. Open the file in IDE and review it. Next, run the below script to summarize the text from the file.

    ```
    python text_summarization.py \
    --modelid "anthropic.claude-v1" \
    --file "letter.txt"
    ```


3. We will now perform a summarization for large text present in **hipaa.txt** file. Observe the content of the file hipaa.txt in the IDE. Then run the large text summarization script and review the output.

    ```
    python large_text_summarization.py
    ```


## 03 - Image generation

1. Go to the appropriate folder

    ```
    cd /home/ec2-user/environment/aws-genai-workshop/03_image_generation/
    ```

    Run the script to generate image

    ```
    python image_generation.py
    ```


## 04 - Chat with your private documents


1. Go to the appropriate folder

    ```
    cd /home/ec2-user/environment/aws-genai-workshop/04_chatbot_private_documents/
    ```


2. Download required dependencies

    ```
    pip install -r requirements.txt
    ```

3. Update the DB host in environment file
    - Go to [CloudFormation console](console.aws.amazon.com/cloudformation/home?region=us-east-1)
    - Click on the stack names **PostgresDBStack**
    - Click **Outputs**
    - Copy the value of **RDSInstanceEndpoint**
    - Open **env.example** file in **04_chatbot_private_documents** folder
    - Paste the value in **PGVECTOR_HOST**


4. Update the Huggingface API key in environment file
    - Open **env.example** file in **04_chatbot_private_documents** folder
    - Update the value of **HUGGINGFACEHUB_API_TOKEN**


5. Update the Cloud9 instance security group to allow a port 8501 to the world. This is the port on which our application runs.
    - Go to the [EC2 console](console.aws.amazon.com/ec2/home?region=us-east-1)
    - Under **Instances**, select the instance with name **aws-cloud9-genai-workshop-*** 
    - Click on **Security**. Then under **Security groups** click on the security group link
    - Under inbound rules, click **Edit inbound rules**
    - Click **Add rule** with following information: **All TCP**, from **Anywhere-IPv4**


6. Run the applcation

    ```
    streamlit run app.py
    ```

Open the endpoint URL with Public IP address. Upload the document and chat with your PDF file.


## 05 - CodeWhisperer - AI Coding assistant

1. Go to the appropriate folder

    ```
    cd /home/ec2-user/environment/aws-genai-workshop/05_codewhisperer/
    ```

2. Open python script 01_csv.py and start coding with CodeWhisperer

3. Open python script 02_upliad_to_s3.py and start coding with CodeWhisperer

4. Open python script 03_query_ddb.py and start coding with CodeWhisperer

