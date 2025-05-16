Knowtion Services
Overview
Knowtion Services is a collection of services that provide various functionalities to the Knowtion platform. These services are designed to be modular and can be used independently or in conjunction with each other.

Prerequisites
Create and activate a virtual environment
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
Install dependencies
# Install the required packages
pip install -r requirements.txt
Run the services
# Run the services
uvicorn src.main:app
Database Connection Guide
This module provides complete Guide to connect to databases using either Azure SQL and PostgreSQL.

It uses pyodbc for SQL connections and psycopg2 for PostgreSQL connections. Azure-based connections are authenticated using DefaultAzureCredential from the Azure Identity SDK.

📦 Prerequisites
Install the required dependencies:

pip install pyodbc psycopg2 azure-identity fastapi
🔌 SQL Server Connection
This section provides examples for connecting to sql server using pyodbc and DefaultAzureCredential.
✅ SQL Server Connection for Azure Service
Below example demonstrates how to connect to an Azure SQL Database using a managed identity.
credential = DefaultAzureCredential(managed_identity_client_id=SQL_DB_CONFIG["sql_client_id"])  # example for dev: "587261c4-d766-44a2-adbe-96c8467b7575"ee
token = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
token_struct = struct.pack(f"<I{len(token)}s", len(token), token)

conn_string = (
    f"Driver={SQL_DB_CONFIG['sql_driver']};"  # example: "{ODBC Driver 17 for SQL Server}"
    f"Server={SQL_DB_CONFIG['sql_server']},1433;"  # example: "sqlmi-kh-dev-eus2-02.bdf8b8e757d5.database.windows.net"
    f"Database=YourDatabase;" # example: "Management"
    f"UID={SQL_DB_CONFIG['sql_client_id']};" # example: "587261c4-d766-44a2-adbe-96c8467b7575"
    f"Authentication=ActiveDirectoryMsi;" 
    f"Encrypt=yes;"
)

sql_conn = pyodbc.connect(conn_string, attrs_before={sql_copt_ss_access_token: token_struct})
✅ SQL Server Connection for Local Service
Below example demonstrates how to connect to SQL Server using a from local machine.

credential = DefaultAzureCredential(managed_identity_client_id=SQL_DB_CONFIG["sql_client_id"]) # example for dev: "587261c4-d766-44a2-adbe-96c8467b7575"
token = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
token_struct = struct.pack(f"<I{len(token)}s", len(token), token)

conn_string = (
    f"Driver={SQL_DB_CONFIG['sql_driver']};" # example: "{ODBC Driver 17 for SQL Server}"
    f"Server={SQL_DB_CONFIG['sql_server']};" # example: "sqlmi-kh-dev-eus2-02.bdf8b8e757d5.database.windows.net"
    f"TrustServerCertificate=yes;"
    f"Encrypt=yes;"
)

sql_conn = pyodbc.connect(conn_string, attrs_before={sql_copt_ss_access_token: token_struct})
🔌 PostgreSQL Connection
PostgreSQL is connected using psycopg2 and the connection string is formed as:

db_user = urllib.parse.quote(POSTGRES_DB_CONFIG['user']) # example: "Azure PostgreSQL Admin Dev"
password = DefaultAzureCredential().get_token("https://ossrdbms-aad.database.windows.net/.default").token

db_uri = (
    f"postgresql://{db_user}:{password}"
    f"@{POSTGRES_DB_CONFIG['host']}/{POSTGRES_DB_CONFIG['dbname']}" # example: "Your Database" (llm_embeddings)
    f"?sslmode={POSTGRES_DB_CONFIG['ssl_mode']}" # example: "prefer" 
)

postgres_conn = psycopg2.connect(db_uri)
Useful Links
https://knowtionhealth.atlassian.net/browse/CIE-207
https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/how-to-configure-sign-in-azure-ad-authentication
https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/how-to-connect-with-managed-identity
https://knowtionhealth.atlassian.net/wiki/spaces/Azure/pages/1026621466/Connect+to+Azure+Database+for+PostgreSQL
Services
1. Data Ingestion Service
The Data Ingestion Service is responsible for collecting and processing data from specified database. It takes a file id as input, collects data from the database, and stores it in a specified vector database.

Steps
Data Collection: Collects data from the specified database using given file id and credentials of that database.
Data preparation: Prepares the data for further processing by cleaning and transforming it a manageable chunks of given chunk size.
Embeddings Generation: Generates embeddings for the list of chunks using the specified embedding model.
Data Storage: Stores the file_id, chunks and their corresponding embeddings in the specified vector database.
Example
curl -X POST "http://KH_DNS_HOST:8000/ingestion/file_id/"
Endpoint
POST /ingestion/file_id/
2. Embedding Generation Service
The Embedding Generation Service is responsible for generating embeddings for a given text.

It takes a text and model(Optional) as input and returns the generated embeddings.

Steps
Text Input: Accepts a text input from the user.
Model Selection: Allows the user to select a specific embedding model (optional). Default is minllm_L6_v2.
Embeddings Generation: Generates embeddings for the input text at token level using the specified embedding model.
Response: Returns the generated embeddings .
Example
curl -X POST "http://KH_DNS_HOST:8000/generate_embeddings/" -H "Content-Type: application/json" -d '{"text": "Hello, world!", "model": "minllm_L6_v2"}'
Endpoint
POST /generate_embeddings/
3. Ollama Question and Answer Service
The Ollama Question and Answer Service is responsible for generating answers to questions based on a given context. It takes a question and context as input and returns the generated answer.

Steps
Question Input: Accepts a question input from the user.
Context Input: Accepts a context input from the user.
Answer Generation: Generates an answer for the input question based on the given context.
Response: Returns the generated answer.
Example
curl -X POST "http://KH_DNS_HOST:8000/llm/ollama/question-answering/" -H "Content-Type: application/json" -d '{"question": "What is the capital of France?", "context": "France is a country in Europe and paris is its capital."}'
Endpoint
POST /llm/ollama/question-answering/
4. Ollama summarization Service
The Ollama Summarization Service is responsible for summarizing a given text. It takes a text and llama model(Optional) as input and returns the generated summary.

Steps
Text Input: Accepts a text input from the user.
Model Selection: Allows the user to select a specific summarization model (optional). Default is llama3.1.
Summary Generation:
For summarizing the text, it creates documents for the text using the TokenTextSplitter and Document from langchain library(map-reduce and stuff chain summarization approaches accepts text in the form of documents).
The TokenTextSplitter is used to split the text into smaller chunks based on the chunk size and chunk overlap.
The Document is used to create a document object from the text.
The map_reduce and stuff chain summarization approaches are used to summarize the text.
The map_reduce chain approach is used to summarize big documents.
The stuff chain approach is used to summarize small documents.
Generates a summary for the input text using the specified summarization model.
Response: Returns the generated summary.
Example
curl -X POST "http://KH_DNS_HOST:8000/llm/ollama/summarization/" -H "Content-Type: application/json" -d '{"text": "The quick brown fox jumps over the lazy dog.", "llama_model": "llama3.1"}'
Endpoint
POST /llm/ollama/summarization/
5. Ollama Custom Summarization Service
The Ollama Custom Summarization Service is responsible for summarizing a given text and model using a custom prompt. It takes a text, model and custom prompt as input and returns the generated summary. In this service, the user can provide a custom prompt to the model to generate a summary. It is useful when the user wants to generate a summary in a specific format or style.

Steps
Text Input: Accepts a text input from the user.
Model Selection: Allows the user to select a specific summarization model (optional). Default is llama3.1.
Custom Prompt Input: Accepts a custom prompt input from the user(optional). Default prompt taken from the prompts file.
Summary Generation:
For summarizing the text, it creates documents for the text using the TokenTextSplitter and Document from langchain library(map-reduce and stuff chain summarization approaches accepts text in the form of documents).
The TokenTextSplitter is used to split the text into smaller chunks based on the chunk size and chunk overlap.
The Document is used to create a document object from the text.
The map_reduce and stuff chain summarization approaches are used to summarize the text.
The map_reduce chain approach is used to summarize big documents.
The stuff chain approach is used to summarize small documents.
Generates a summary for the input text using the specified summarization model.
Response: Returns the generated summary.
Example
curl -X POST "http://KH_DNS_HOST:8000/llm/ollama/custom-summarization/" -H "Content-Type: application/json" -d '{"text": "The quick brown fox jumps over the lazy dog.", "llama_model": "llama3.1", "prompt": "Summarize the text in a single sentence."}'
Endpoint
POST /llm/ollama/custom-summarization/
6. Text summarization Service
The Text Summarization Service is responsible for summarizing the given document. This service is useful when the user wants to summarize a document in a specific format or style. It takes a document id and model as input and returns the generated summary. The amount of text to be summarized is determined by the maximum number of tokens allowed by the model(Environment variable MAX_TOKENS_FOR_SUMMARIZATION).

Steps
Document ID Input: Accepts a document id input from the user.
Model Selection: Allows the user to select a specific summarization model (optional). Default is llama3.1.
Extract Text: Extracts the text from the database using the document id.
Summary Generation:
For summarizing the text, it creates documents for the text using the TokenTextSplitter and Document from langchain library(map-reduce and stuff chain summarization approaches accepts text in the form of documents).
The TokenTextSplitter is used to split the text into smaller chunks based on the chunk size and chunk overlap.
The Document is used to create a document object from the text.
The map_reduce and stuff chain summarization approaches are used to summarize the text.
The map_reduce chain approach is used to summarize big documents.
The stuff chain approach is used to summarize small documents.
Generates a summary for the input text using the specified summarization model.
Response: Returns the generated summary.
Example
curl -X POST "http://KH_DNS_HOST:8000/summarize/doc_id={doc_id}" -H "Content-Type: application/json" -d '{"doc_id": "12345", "llama_model": "llama3.1"}'
Endpoint
POST /summarize/doc_id={doc_id}
7. Custom Text Summarization Service
The Custom Text Summarization Service is responsible for summarizing the given document using a custom prompt. This service is useful when the user wants to summarize a document in a specific format or style. It takes a document id, model and custom prompt as input and returns the generated summary. The amount of text to be summarized is determined by the maximum number of tokens allowed by the model(Environment variable MAX_TOKENS_FOR_SUMMARIZATION).

Steps
Document ID Input: Accepts a document id input from the user.
Model Selection: Allows the user to select a specific summarization model (optional). Default is llama3.1.
Custom Prompt Input: Accepts a custom prompt input from the user(optional). Default prompt taken from the prompts file.
Extract Text: Extracts the text from the database using the document id.
Summary Generation:
For summarizing the text, it creates documents for the text using the TokenTextSplitter and Document from langchain library(map-reduce and stuff chain summarization approaches accepts text in the form of documents).
The TokenTextSplitter is used to split the text into smaller chunks based on the chunk size and chunk overlap.
The Document is used to create a document object from the text.
The map_reduce and stuff chain summarization approaches are used to summarize the text.
The map_reduce chain approach is used to summarize big documents.
The stuff chain approach is used to summarize small documents.
Generates a summary for the input text using the specified summarization model.
Response: Returns the generated summary.
Example
curl -X POST "http://KH_DNS_HOST:8000/summarize/custom/doc_id={doc_id}" -H "Content-Type: application/json" -d '{"doc_id": "12345", "llama_model": "llama3.1", "prompt": "Summarize the text in a single sentence."}'
Endpoint
POST /summarize/custom/doc_id={doc_id}
Limitations
The services are designed to work with specific embedding models and summarization models.
The embedding models are minllm_L6_v2 and all_mpnet_base_v2
The llama models are llama3.1 and Mistral
If the user wants to use a different model or a custom model then developer needs to modify the code to add support for that model.
Note
The services are designed to be modular and can be used independently or in conjunction with each other.
The services are built using FastAPI and can be easily extended to add more functionalities.
The services are designed to be scalable and can handle large amounts of data.
The services are designed to be secure and can be easily integrated with authentication and authorization mechanisms.
The services are designed to be easily deployable and can be deployed on any cloud platform or on-premises.
The services are designed to be easily maintainable and can be easily updated to add new features or fix bugs.
The services are designed to be easily monitored and can be easily monitored using logging and monitoring tools.
