## DevOps for GenAI Workshop

This workshop explores the integration and impact of Generative AI (GAI) tools in DevOps and DevSecOps. We aim to comprehensively understand RAGs, Orchestration, and Observalbility solutions related (LLMs) that can be effectively utilized in modern software delivery and security practices.

In this workshop we will focus on what we are calling the LAM stack in order to learn the basics of data operations and engenering realted to Large Language Models (LLMs.)

LORM Stack for this workshop

- L - Langchain or LlamaIndex (Orchestration)
- O - Arize Pheonix (Observability) 
- R - MongoDB Atlas Vector Serach (RAG)
- M - GPT4 (Model)

## Code of Conduct
[https://devopsdays.org/conduct/](https://devopsdays.org/conduct/)

## GenAI Workshop Preparation Sheet Overview

| Overview  |
|:----------|
| Signup for a free OpenAI account    |
| Create a Free MongoDB Atlas Account |
| Run the first example |
| Chunking Strategy Example |
| Embedding Strategy Example |
| Setup another Atlas Vector Database (Langchain Example) |
| Setup Google Colab environment id using GCP |
| Setup Amazon Sagemaker environment id using AWS|
| Chunking and Embedding Labs |
| Evaluation Labs |
| Optional Labs |
| Setting S3 Buckets for large files (optional) |

### 1) Signup for a free OpenAI account
- Create an OpenAI account
- Select API keys in the left panel
- Verify by phone
- Create a secret key, save and copy it.

### 2) Create a Free MongoDB Atlas Account
- Register a new account at: [https://www.mongodb.com/cloud/atlas/register](https://www.mongodb.com/cloud/atlas/register)

#### Create an account
- Select Product from top down menu
- Select Try for Free Signup for a free account
- Great, now verify your email
- Fill in the little questionnaire
- Takes you into the Deploy Database

#### Deploy Database Cluster
- Select the free m0
- Use the defaultname Cluster0
- Default to N.Virginia (US-East-1) 
- Keep Automate security setup enabled
- Keep Add sample dataset enabled
- Provide AWS
- Now create the deployment (button below/right)

#### Configure the database cluster
- There is an automatic user created.
- (if copy and paste doesn't work, consider reloading the page)
- Fill out user and password & create the user
- Change the IP address that have access: (by clicking IP Access List)
- by default it will fill in your current IP address
- but for the hackathon we don't exactly what that IP will be
- Therefore we allow all IPs
- Use 0.0.0.0/0 for IP
- do this for hackathon only , for production restrict this
- Now Create the Database and Cluster.

#### Get database cluster connection string
- After the Database is created select the Connect button for Cluster0
- Select Drivers
- Select Python (3.12 or later is fine)
- Copy the connect string: it Should look like something like this:

 ```
  mongodb+srv://<userid>:<password>@cluster0.ozciyn7.mongodb.net/?retryWrites=true&w=majority
 ```
- Replace the &lt; and &gt; characters with the user and password you created (don't include the &lt; and &gt; characters)
- Congratulations, you're all done and the mongodb database setup is completed

### 3) Setup and run the first example code  

In this example we are going to load a HuggingFace dataset provided by MongoDB.

>>##### For more details see:
>> [https://huggingface.co/datasets/AIatMongoDB/embedded_movies](https://huggingface.co/datasets/AIatMongoDB/embedded_movies)
>>
>>#### Here are some examples applications by MongoDB
>> [https://huggingface.co/MongoDB](https://huggingface.co/MongoDB)


#### Setup the Database Collection 
- select Database button on the left
- select the Browse Collections tab
- select create databases
- select add my own data
	- Database sample_mflix
 	- Collection embedded_movies

Note: this same code can be used to load another MongoDB supplied HF dataset called "whatscooking"

Code example from the AIatMongoDB/embedded_movies (loading the collection)
Use:

In the clone's repo run the following notebook:

**GenAI-Workshop-Demon1a.ipyn**

**Note:** You can choose your own notebook interface to run your code. For the purposes of this workshop we have setup examples fro both AWS Sagemaker and Google Colab ( Section #5 for Sagemaker and Section #6 for Colab)

```
!pip install pymongo
!pip install dataset
```
```
import os
os.environ['MONGODB_ATLAS_URI'] = <your atlas connection string>

from pymongo import MongoClient
import datasets
from datasets import load_dataset
from bson import json_util

uri = os.environ.get('MONGODB_ATLAS_URI')
client = MongoClient(uri)
db_name = 'sample_mflix'
collection_name = 'embedded_movies'

embedded_movies_collection = client[db_name][collection_name]

dataset = load_dataset("AIatMongoDB/embedded_movies")

insert_data = []

for movie in dataset['train']:
    doc_movie = json_util.loads(json_util.dumps(movie))
    insert_data.append(doc_movie)

    if len(insert_data) == 1000:
        embedded_movies_collection.insert_many(insert_data)
        print("1000 records ingested")
        insert_data = []

if len(insert_data) > 0:
    embedded_movies_collection.insert_many(insert_data)
    insert_data = []

print("Data Ingested")
```
>See Using **Using Amazon Sagemaker** from Google Colab - MDB_embedded_movies.ipynb
>
>or
>
>See **Using Google Colab** from Amazon Sagemaker - MDB_embedded_movies.ipynb 

#### Browse the embedded_movies collection

![Figure 0](/images/image0.png)

Add a filter to see only one movie

```
{ "title": "Scarface" }
```
#### Deleting a Collection (Optional)

If you need to reload a collection.

- Select Database
- Select Brose Collections
- In the left window highlight the collection name
- Select the trash can icon and delete

### 4) Managing Chunking  

In this example we are going to load a HuggingFace dataset based on a Deming Book and demo chunking stratgies.

Using Gradio to demonstrate chunking/ebeddings for Deming’s Journey to Profound Knowledge. 

In the clone's repo run the following notebook:

**GenAI-Workshop-Demo1b.ipynb**

### 5) Testing Embeddings  

In this example we are going to load a HuggingFace dataset based on a Deming Book and demo embedding stratgies.

Using Embeddings to test Cosine Similarities

Try testing out some differnt embeddings and see what kind of results you get with your query

```
# Constants for default values
DEFAULT_CHUNK_SIZE = 400
DEFAULT_CHUNK_OVERLAP = 50
DEFAULT_NUM_CHUNKS = 10

# nomic-ai/nomic-embed-text-v1',trust_remote_code=True

# Initialize the sentence transformer model for embeddings
#model = SentenceTransformer('all-MiniLM-L6-v2')
model = SentenceTransformer('BAAI/bge-small-en-v1.5')
#model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
#model = SentenceTransformer('nomic-ai/nomic-embed-text-v1',trust_remote_code=True)
```
In the clone's repo run the following notebook:

**GenAI-Workshop-Demon1c.ipyn**

### 6) Setup another Atlas Vector Database (Langchain Example)

This example is based on the following code:

[https://python.langchain.com/docs/integrations/vectorstores/mongodb_atlas](https://python.langchain.com/docs/integrations/vectorstores/mongodb_atlas)

- set up Atlas database:
- select Deployments > Database on the left side
- Select Browse Collections tab
- Select Create Database button on the left
- database langchain_db
- collection_name test 

#### Setup Atlas search vector index
- After the Database is created and set up, we'll set up an Atlas search vector index.
- select Atlas Search on the left navigation side
- select your database source: Cluster0	
- Click on “Create Search Index”
- Select Atlas Vector Search (Json editor)
- Select Database langchain_db and collection_name test 
- IndexName vector_index
- Use the following json to configure:					

```
{
  "fields": [
    {
      "numDimensions": 1536,
      "path": "embedding",
      "similarity": "cosine",
      "type": "vector"
    }
  ]
}
```
 
Here’s what it should look like when you're done:
![Figure 1](/images/image1.png)
Figure 1

>>##### For more details see:
>>[https://www.mongodb.com/docs/atlas/atlas-vector-search/create-index/](https://www.mongodb.com/docs/atlas/atlas-vector-search/create-index/)

In the clone's repo run the following notebook:
**GenAI-Workshop-Demo5.ipynb**

Note: The code assumes you have setup Google Secrets Manager. If your using a differnt platform you will need to change the code accordingly. 

Retrieve the vector database example:

In the clone's repo run the following notebook:
**GenAI-Workshop-Demo6.ipynb**

### 7) Setting up Google Colab 
- Create a free account on Google Colab
- Goto ( https://colab.research.google.com/ )
- Clone the workshop repo
  	- open up a terminal window
  	- git clone https://github.com/OperationalizingAI/DevOpsGAIWorkshop.git
- Load the same note books for Colab
	- MDBLoad-GC.ipynb
	- MDBRetrieve-GC.ipynb
- Setup Google Secrets Manager (secrets)
- For certain labs you may need to copy the requirements,txt, OpenAICLient.py, AltasClient.py from the repo directory to the root directory.
- Run your code.
   
### 8) Using Amazon Sagemaker 
From the AWS Console navigate the Amazon Sagemaker (note you can use the search bar.)

#### Setup a Notebook Instance
- After the Atlas Vector Database (Cluster0) is created and set up, we'll set up a Notebook Instance:
- select Notebook > Notebook Instances on the left side
- Select the “Create notebook Instance” button on top right
- In Notebook Instance Settings
- Add a Notebook Instance name (e.g., MDB-test1)
- Use the defaults for the other setting fields
- See Figure 2.
- In Permissions and encryption
- Select “Create a new role” from dropdown (take the defaults)
- See Figure 3

#### Configure a Git Repository 
- Select Git repository from the left window
- Select the Default repository arrow
- Select Clone a public Git repository to this notebook instance only
- Paste the repo
- Create notebook

Use this link to clone...

[https://github.com/OperationalizingAI/DevOpsGAIWorkshop.git](https://github.com/OperationalizingAI/DevOpsGAIWorkshop.git)

(See Figure 4 for an example)

![Figure 2](/images/image2.png)
Figure 2

![Figure 3](/images/image3.png)
Figure 3

![Figure 4](/images/image4.png)
Figure 4 
### Note: Use github.com/OperationalizingAI/DevOpsGAIWorkshop.git for the cloned repo.

#### Create the Notebook
- After the instance is running (inService) create the Python notebook. 
- Select the Open JupyterLabs action for the instance
- Under Notebook select the conda_python3 box
- Rename your notebook (e.g., MDB-example1.ipynb)
- Import the sample notebook provided with the workshop
- Load the same note books for Colab
- For the Langchain Example
	- **MDBLoad-SM.ipynb**
	- **MDBRetrieve-SM.ipynb**
- Run your code.

>Note: The examples use a secrets manager. For Sagemaker we used Amazon Secrets Manager.
> Setup the following:
>> OPENAPI_API_KEY
>> 
>> MONGODB_ATLAS_CLUSTER_URI
>
> Alternativly you can setup your keys in the notebook "getpass" or some other tool.

#### Using Amazon Secrets Manager
- Setup your secrets in Amazon Secrets Manager
- Remove all of the Google code from the norebook (installs and secrets management code)
- Add the following code to your notebook
> Note:
>> I had to comment out llama-cpp-python in requirements.txt (figure out later)

```
import os
import json
import boto3
from botocore.exceptions import ClientError

def get_secret():

    secret_name = "hackathon"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = json.loads(get_secret_value_response['SecretString'])
    #print(secret)
    return secret
```
```
secret = get_secret()

openai_api_key = secret["OPENAI_API_KEY"]
os.environ['OPENAI_API_KEY'] = openai_api_key

MONGODB_ATLAS_CLUSTER_URI = secret["MONGODB_ATLAS_CLUSTER_URI"]
os.environ['MONGODB_ATLAS_CLUSTER_URI'] = MONGODB_ATLAS_CLUSTER_URI

langsmith_api_key = secret["LANGSMITH_API_KEY"]
os.environ['LANGSMITH_API_KEY'] = langsmith_api_key
```

### 8) Evaluation Labs
Using Pheonix Arize andLangsmith, we will look at different thinking strategies to analyze optimal relevance and similarity queries.

Arize Phoenix is an opensource tool for evaluating, troubleshoot, and fine tune your LLMs.

[https://github.com/Arize-ai/phoenix](https://github.com/Arize-ai/phoenix)

Lab Demo Example:

- **GenAI-Workshop-Demo7.ipynb** - Evaluation of OpenContext Documentaion with Arize
 - For Sagemaker change install - pip install arize-phoenix>=3.14.0

This is what we are calling the LAM Stack Example...

[https://colab.research.google.com/drive/1LXJW0YS-N8_5f6E6p1hGGLsZ2k4ZD5P3?usp=sharing](https://colab.research.google.com/drive/1LXJW0YS-N8_5f6E6p1hGGLsZ2k4ZD5P3?usp=sharing)

The following is a code that will work with Langhcain.

Install Arize-Phoenix
```
!pip install arize-phoenix
```

Import and setup the enviornment
```
from urllib.request import urlopen

import nest_asyncio
import numpy as np
import pandas as pd
import phoenix as px
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.retrievers import KNNRetriever
from phoenix.experimental.evals import (
    HallucinationEvaluator,
    OpenAIModel,
    QAEvaluator,
    RelevanceEvaluator,
    run_evals,
)
from phoenix.session.evaluation import get_qa_with_reference, get_retrieved_documents
from phoenix.trace import DocumentEvaluations, SpanEvaluations
from phoenix.trace.langchain import LangChainInstrumentor
from tqdm import tqdm

nest_asyncio.apply()  # needed for concurrent evals in notebook environments
```
Before you run your quey
```
session = px.launch_app()
LangChainInstrumentor().instrument(
```
If you want to run evaluations for hallucinations, correctness, and relevance
```
queries_df = get_qa_with_reference(px.Client())
retrieved_documents_df = get_retrieved_documents(px.Client()

eval_model = OpenAIModel(
    model_name="gpt-4-turbo-preview",
)
hallucination_evaluator = HallucinationEvaluator(eval_model)
qa_correctness_evaluator = QAEvaluator(eval_model)
relevance_evaluator = RelevanceEvaluator(eval_model)

hallucination_eval_df, qa_correctness_eval_df = run_evals(
    dataframe=queries_df,
    evaluators=[hallucination_evaluator, qa_correctness_evaluator],
    provide_explanation=True,
)
relevance_eval_df = run_evals(
    dataframe=retrieved_documents_df,
    evaluators=[relevance_evaluator],
    provide_explanation=True,
)[0]

px.Client().log_evaluations(
    SpanEvaluations(eval_name="Hallucination", dataframe=hallucination_eval_df),
    SpanEvaluations(eval_name="QA Correctness", dataframe=qa_correctness_eval_df),
    DocumentEvaluations(eval_name="Relevance", dataframe=relevance_eval_df),
)
```

### 8) Optional Labs
We created a number of lab exerciese based on the work of Sujee Maniyam. He did an amazing job researching and putting together a number of examples. However, they are all designed to run locally on your machine. We have created a number of his labs in this repository under the directory "labs/" that work with Google Colab and Amazon's Sagemaker. You can find his orignal work here:

[https://github.com/sujee/mongodb-atlas-vector-search](https://github.com/sujee/mongodb-atlas-vector-search)]

There also some great examples in Prakul Argarwal's (from MongoDB) repository here:

[https://github.com/prakul/MongoDB-AI-Resources](https://github.com/prakul/MongoDB-AI-Resources)

Here's a list of the labs:

- MDB-lab1 - Connects to the client connection to the Atlas database. Assumes the sample_mflix databse exists.
- MDB-Lab1-2 - Simple program to generate images using OpenAI Dall-e-3. 
- MDB-Lab2-1 - Simple OpenAI client connection test.
- MDB-Lab2-2 - Run simple quries against the sample_mflux (Netflix Movies) dataset. Setup a vector search index to quest embeddings.
- MDB-Lab2-3 - Run cosine similarity against chunked PDF files. 
- MDB-Lab2-4 - Query embeddings from text-embedding-ada-002 to use to search Atlas vector database. The langchain_db must exist already.
- MDB-Lab3-1 - Querying with different embedding models.
- MDB-Lab3-2 - Adding multiple embeddings to a collection.
- MDB-Lab3-3 - Compare performance of different embeddings.
- MDB-Lab4-1 - Load Uber and Lyft 10k PDFs into Atlas Vector Search.
- MDB-Lab4-2 - DAL-E-3 Image generator.

### 9) Setting S3 Buckets for large files (optional) 

- Additional Notes for Processing Large Files
- Setup a shared S3 blob
- Bucket 
- Large-blobs
- Upload the file(s) 
- Uncheck - Block all public access
- Take all the default
```
Create Bucket
	Configure Bucket policy
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::large-blobs/*"
        }
    ]
}
```

From the Notebook console open the termial of the Instance…
```
	aws s3 cp s3://large-blobs/void.tar.gz ~/void.tar.gz
```
