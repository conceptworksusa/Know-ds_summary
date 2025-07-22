import logging
import os

# Set up logging configuration(Set the logging level to INFO)
logging.basicConfig(level=logging.INFO)

# Get the logger
logger = logging.getLogger()

# Define base url for invoking the llama3 model through ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://vmdsdev01.knowtionhealth.lan:11434/")

embedding_model_path = r"C:\Surendra\llm\all_mpnet_base_v2"

# Define the default LLM model to be used
DEFAULT_LLAMA_MODEL = os.getenv("DEFAULT_LLAMA_MODEL", "llama3.1")

POSTGRES_DB_CONFIG = {
        "dbname": os.getenv("POSTGRES_DB_NAME", "llm_embeddings"),
        "host": os.getenv("POSTGRES_HOST", "psql-kh-dev-eus2-01.postgres.database.azure.com"),
        "user": os.getenv("POSTGRES_USER", "Azure PostgreSQL Admin Dev"),
        "ssl_mode":os.getenv("POSTGRES_SSL_MODE", 'prefer'),
        "pg_client_id": os.getenv('PG_CLIENT_ID', '587261c4-d766-44a2-adbe-96c8467b7575')
    }

# Define verbose mode
VERBOSE = os.getenv("VERBOSE", False)

# Define the allowed intents for the intent classifier
ALLOWED_INTENTS = ['Greet', 'Status', 'Unknown']
