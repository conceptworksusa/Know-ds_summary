from src.logger.Logger import Logger
import os
from pathlib import Path


# Define the chunk size for embeddings
CHUNK_SIZE_FOR_EMBEDDINGS = os.getenv("CHUNK_SIZE_FOR_EMBEDDINGS", 128)

# Define the chunk overlap size for embeddings
CHUNK_OVERLAP_EMBEDDINGS = os.getenv("CHUNK_OVERLAP_EMBEDDINGS", 0)

# Define the document type for PDF
DOC_TYPE_FOR_PDF  = os.getenv("DOC_TYPE_FOR_PDF", "pdf")

# Define the number of matches toN be retrieved for semantic retrieval
NUMBER_OF_MATCHES_FOR_SEMANTIC_RETRIEVAL = os.getenv("NUMBER_OF_MATCHES_FOR_SEMANTIC_RETRIEVAL", 6)

# Define the number of matches to be retrieved for Tf-Idf
NUMBER_OF_MATCHES_FOR_TF_IDF = os.getenv("NUMBER_OF_MATCHES_FOR_TF_IDF", 3)

# Define the threshold for the LateChunking service
THRESHOLD_FOR_SEMANTIC_RETRIVAL = os.getenv("THRESHOLD_FOR_SEMANTIC_RETRIVAL", 0.2)

# Define the threshold for the Tf-Idf service
THRESHOLD_FOR_TF_IDF = os.getenv("THRESHOLD_FOR_TF_IDF", 0.2)

# set the configuration
SEMANTIC_CONFIGURATION = os.getenv("SEMANTIC_CONFIGURATION", "sematic")

# Define the URL for the ollama service
OLLAMA_QA_URL = os.getenv("OLLAMA_URL", "http://localhost:8000/llm/ollama/")

# Define the URL for the ollama summarization service
OLLAMA_SUMMARIZATION_URL = os.getenv("OLLAMA_SUMMARIZATION_URL", "http://localhost:8000/llm/ollama/summarization")

# Give the model path for MiniLM-L6-v2
model_paths = {"minllm_L6_v2": os.getenv("minllm_L6_v2_path", r"C:\Surendra\llm\minllm_L6_v2"),
               "all_mpnet_base_v2": os.getenv("all_mpnet_base_v2_path", r"C:\Surendra\llm\all_mpnet_base_v2")}

# Define the default model for embeddings
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "minllm_L6_v2")

# Connect with the token and This connection option is defined by microsoft in msodbcsql.h
SQL_COPT_SS_ACCESS_TOKEN = 1256

# Define the database configuration
SQL_DB_CONFIG = {
        "sql_client_id": os.getenv('SQL_CLIENT_ID', '587261c4-d766-44a2-adbe-96c8467b7575'),
        "sql_driver": os.getenv("DRIVER", '{ODBC Driver 17 for SQL Server}'),
        "sql_server": os.getenv("SQL_SERVER", 'sqlmi-kh-dev-eus2-02.bdf8b8e757d5.database.windows.net'),
    }

# # Define the database configuration
# SQL_DB_CONFIG = {
#         "dbname": os.getenv("SQL_DB_NAME", "Management"),
#         "host": os.getenv("SQL_HOST", "sqlmi-kh-dev-eus2-02.bdf8b8e757d5.database.windows.net"),
#         "Authentication": os.getenv("SQL_AUTHENTICATION", "ActiveDirectoryInteractive"),
#         "port": os.getenv("SQL_PORT", 1433),
#     }

# SQL_DB_CONFIG = {
#         "Database": os.getenv("Database", "Management"),
#         "Server": os.getenv("Server", "sqlmi-kh-dev-eus2-02.bdf8b8e757d5.database.windows.net"),
#         "UID": os.getenv("UID", "Azure SQL Admin Dev"),
#         "Authentication": os.getenv("Authentication", "ActiveDirectoryMsi"),
#         "port": os.getenv("SQL_PORT", 1433),
#         "TrustServerCertificate": os.getenv("TrustServerCertificate", "yes"),
#         "Encrypt": os.getenv("Encrypt", "yes")
#     }

# connection_string = f'Driver={driver};Server=tcp:{server};Database={Database};UID={AccountId};Authentication=ActiveDirectoryMsi;TrustServerCertificate=yes;Encrypt=yes'

# Define the database configuration for Postgres SQL

POSTGRES_DB_CONFIG = {
        "dbname": os.getenv("POSTGRES_DB_NAME", "llm_embeddings"),
        "host": os.getenv("POSTGRES_HOST", "psql-kh-dev-eus2-01.postgres.database.azure.com"),
        "user": os.getenv("POSTGRES_USER", "Azure PostgreSQL Admin Dev"),
        #"user": os.getenv("POSTGRES_USER", "id-kh-app-dev-eus2"), # id-kh-app-dev-eus2
        "ssl_mode":os.getenv("POSTGRES_SSL_MODE", 'prefer'),
        "pg_client_id": os.getenv('PG_CLIENT_ID', '587261c4-d766-44a2-adbe-96c8467b7575')
    }

# POSTGRES_DB_CONFIG = {
#         "dbname": os.getenv("POSTGRES_DB_NAME", "llm_embeddings"),
#         "host": os.getenv("POSTGRES_HOST", "psql-kh-dev-eus2-01.postgres.database.azure.com"),
#         "user": os.getenv("POSTGRES_USER", "Azure PostgreSQL Admin Dev"),
#         "password": os.getenv("POSTGRES_PASSWORD", "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkNOdjBPSTNSd3FsSEZFVm5hb01Bc2hDSDJYRSIsImtpZCI6IkNOdjBPSTNSd3FsSEZFVm5hb01Bc2hDSDJYRSJ9.eyJhdWQiOiJodHRwczovL29zc3JkYm1zLWFhZC5kYXRhYmFzZS53aW5kb3dzLm5ldCIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzY1ZjQyNTc0LWNmMzMtNGIxMS1iNjhiLTg4NjVjZGU2MTNkYi8iLCJpYXQiOjE3NDU1MDgxNjIsIm5iZiI6MTc0NTUwODE2MiwiZXhwIjoxNzQ1NTEyMjgxLCJhY3IiOiIxIiwiYWlvIjoiQWFRQVcvOFpBQUFBVlBuaGw4QkZqdnpWTmdSRjJkbkRnRzJaSmhlL1l1VnJhYkVNaDFJKzhBazJTbThVUW16L1ZqRTBmOVpvaGdQaE9JbzFaeFJkZnNkamdFNHVNOTErbzYxdUFyZyszSEdIVWZ3TmI2cU1GYUcyZUR1clQ1WEFUeDhHVi9KRGFCczIzS29zRW1MbVhMK0JycWIzbW1yZlB3MlNHWG0ranBjaStjbGF3TVNTanUraTEwZmdEdGgrQkN4UlAxTWMvYnZ6L2Fnb3dQbWg2TGRuMEpxVXFuZUxTZz09IiwiYW1yIjpbInJzYSIsIm1mYSJdLCJhcHBpZCI6IjA0YjA3Nzk1LThkZGItNDYxYS1iYmVlLTAyZjllMWJmN2I0NiIsImFwcGlkYWNyIjoiMCIsImRldmljZWlkIjoiZjRiZDlmMzctYWFmNy00NWFkLTkyZTQtMzVhNWJlNTgwYjZhIiwiZmFtaWx5X25hbWUiOiJLYXJuYXRhcHUiLCJnaXZlbl9uYW1lIjoiU3VyZW5kcmEiLCJncm91cHMiOlsiMTc2YzI3MTItY2JkYS00MDQ5LTljZjktNjc3ZDY2OWRhNGE3IiwiYWU4YWM3MjAtZDlmZC00MzMwLWFlMTEtZmE0NWMyMDkyMzQ4IiwiY2JjMmU2MjItZGE5Yy00NmYyLTg0ZTYtYjE4ZjMxZTFlOGFmIiwiZGQ4ZGI5MjQtNDAwZS00ZTFkLTg0YTItMGM5MDVlNDY3NDcyIiwiMDRkNjhlMzMtNjJkZC00ZTFiLWIzMzgtMmI1Yzg1MjYwYWY2IiwiMWMwZmQ0MzctMjc5OC00MjU3LThiODEtOWUyNjVjZDg3N2RiIiwiMzEzYmZjM2EtZTk5MC00MTBmLWIyYzAtZWFhZjNmNzM5MTYzIiwiNDU5NWYzNTYtMThlYy00YTljLTk1MDgtNjhmZjViM2ZjNGM2IiwiZWFhZDg2NmEtMzBmMy00MDBiLTkwZmQtYjM1NDVmMTE2NjMzIiwiMTliMTM5NmMtYzQyNS00NDkzLWI3NTYtZTUwYzYxNmRiZTJjIiwiN2RiYjZjNmMtMTA2YS00ZDZhLWE3OTktMGJmMzdjMjFiZDgxIiwiYmEzNjIwNzMtMWE5NS00NzJmLWJhNDQtMmM1NmZhM2FkNWVmIiwiMmU4M2JhN2EtMDZiMi00ZmZjLWEzZWItNmZiNWQ1YzkzODg4IiwiZjIwMDBiODEtNzYwOC00ZDFmLThmYzAtZTk4ZTRhOWU4MTMxIiwiNzA2ZDMwOGUtYmU0ZC00ZWY5LWJmOTQtMjllNDU1ZTNhYmQ5IiwiNjQ4MGVjOGUtOGY0Yi00YjViLThhMGQtYjE0NTNkYmMxMDQxIiwiZDQ5OGU0YTAtMTRmZS00Mzg2LWE1NDItZTJhOGJmNzZhNGIyIiwiZTUyYmY4YWEtYWMyNy00NDFmLTgzZjEtNzFmYTk4MDU3NjQ3IiwiYTAyMjk4YjAtODRmYi00MWVkLWJlYzUtNzRlNDVhZTcwNDk0IiwiN2I3OTIwYzctN2IxMC00ZGFkLThiYTctZGQ4NTdkOGZmMDQ2IiwiZTA1MjFkZTAtOTQ3My00YjkwLWJiZjAtOGQxYzQxYWFhNjgwIiwiYmY1ZjQ1ZjYtYjhiMi00YmU0LTlmODAtZGJlYjVlNWM2ODMyIl0sImlkdHlwIjoidXNlciIsImlwYWRkciI6IjE4NC45OC4yMjEuMTY2IiwibmFtZSI6IlN1cmVuZHJhIEthcm5hdGFwdSIsIm9pZCI6Ijg3M2FjNDFiLThmMTUtNGVkNy05NmU5LTA3YmU4N2JlZDQ5YiIsIm9ucHJlbV9zaWQiOiJTLTEtNS0yMS0xOTI1MTkzNzIwLTg2Mzc3MzEzLTkzNjExMzU0My03Njg5IiwicHVpZCI6IjEwMDMyMDA0Mzk5RTNEMTMiLCJwd2RfdXJsIjoiaHR0cHM6Ly9wb3J0YWwubWljcm9zb2Z0b25saW5lLmNvbS9DaGFuZ2VQYXNzd29yZC5hc3B4IiwicmgiOiIxLkFYMEFkQ1gwWlRQUEVVdTJpNGhsemVZVDIxRFlQQkxmMmIxQWxOWEo4SHRfb2dPMUFQVjlBQS4iLCJzY3AiOiJ1c2VyX2ltcGVyc29uYXRpb24iLCJzaWQiOiIwMDEzOGZlOS1iNDgwLTRjYmEtOTYxNS0zZjY2OGZkYTFhNmEiLCJzdWIiOiJadHJfVUU5QTBpMHRIMmk1aFN3cGU5MmlseWxqOTAyOWJhN2VLVmkwbEVvIiwidGlkIjoiNjVmNDI1NzQtY2YzMy00YjExLWI2OGItODg2NWNkZTYxM2RiIiwidW5pcXVlX25hbWUiOiJza2FybmF0YXB1QGtub3d0aW9uaGVhbHRoLmNvbSIsInVwbiI6InNrYXJuYXRhcHVAa25vd3Rpb25oZWFsdGguY29tIiwidXRpIjoicWJFdkk5TGk2a2UwMUtzUWdtTWFBQSIsInZlciI6IjEuMCIsInhtc19pZHJlbCI6IjEwIDEifQ.HTbvxQpKt4_Cfu7aRvNZUe4FPJ2UOBZ2SB3AeL7tFZKabVpPHrRgD0BXjPtRqSRpdZQ5p8jI-oTzajCFUOb6_hsUxehTpvUwSz4OAVZNTj9PFFgTMJLZpqohu0aiiTMhdvBDg8BZ7TpIflraB0WP79h0OVNHMiVZJWWS6Hg0MWXsRRwLWnc9c5gjSkOOOwfBv84ozpPCdHlshnfixFIlvGXw3YbFQ1NJZnfawPgu639zS5EU_jqQ4kHpprC4ay0d_gH6IvKUk5-lU7_s7BxkTu5aiqxCw8kTJTKDfWwlIyxRbhyZFGGdD19fi6zFnkIrK10uKqlYooqRx1Ycv4Jqyw"),
#         "port":os.getenv("POSTGRES_PORT", 5432)
#     }

# Define the chunk size and overlap for text splitting
CHUNK_SIZE_FOR_SUMMARIZATION = os.getenv("CHUNK_SIZE_FOR_SUMMARIZATION", 2000)
CHUNK_OVERlAP_FOR_SUMMARIZATION = os.getenv("CHUNK_OVERlAP_FOR_SUMMARIZATION", 10)

# Define the maximum number of tokens for summarization depends on the machine
MAX_TOKENS_FOR_SUMMARIZATION = os.getenv("MAX_TOKENS_FOR_SUMMARIZATION", 10000)

# Define base url for invoking the llama3 model through ollama
#OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://vmdsdev01.knowtionhealth.lan:11434/")


# Define the default LLM model to be used
DEFAULT_LLAMA_MODEL = os.getenv("DEFAULT_LLAMA_MODEL", "llama3.1")

# Define verbose mode
VERBOSE = os.getenv("VERBOSE", False)

LOG_PATH = os.getenv("LOG_PATH", os.path.join(Path(__file__).parent.parent.parent, "logs"))
__log_kh_services = Logger("Knowtion-Services", LOG_PATH)

__log_kh_services.start()

logger = __log_kh_services
