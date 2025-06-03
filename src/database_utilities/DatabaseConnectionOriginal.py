# Importing necessary libraries
import pyodbc, struct
from src.conf.Configurations import logger, SQL_DB_CONFIG, POSTGRES_DB_CONFIG
import psycopg2
from fastapi import HTTPException
import urllib.parse
from azure.identity import DefaultAzureCredential

class DatabaseConnection:
    def __init__(self):
        self.logger = logger

    def get_sql_conn(self):
        try:
            # Create a credential object using DefaultAzureCredential.
            self.logger.info("Creating a credential object using DefaultAzureCredential.")
            credential = DefaultAzureCredential(
                managed_identity_client_id=SQL_DB_CONFIG["sql_client_id"])

            # Get token for Azure SQL Database and convert to UTF-16-LE for SQL Server driver
            self.logger.info("Getting token for Azure SQL Database.")

            # Get the token using the DefaultAzureCredential
            token = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")

            # Pack the token into a structure for pyodbc
            self.logger.info("Token obtained successfully")
            token_struct = struct.pack(f'<I{len(token)}s', len(token), token)


            # Connect with the token and This connection option is defined by microsoft in msodbcsql.h
            sql_copt_ss_access_token = 1256

            # Define the connection string for local
            conn_string = f"Driver={SQL_DB_CONFIG['sql_driver']};Server=tcp:{SQL_DB_CONFIG['sql_server']};TrustServerCertificate=yes;Encrypt=yes;"

            # Define the connection string for Azure
            # conn_string = f"Driver={SQL_DB_CONFIG['sql_driver']};Server={SQL_DB_CONFIG['sql_server']},1433;Database=Management;UID={SQL_DB_CONFIG['sql_client_id']};Authentication=ActiveDirectoryMsi;Encrypt=yes;"

            # Connect to the database using pyodbc
            self.logger.info("Connecting to the database...")
            sql_conn = pyodbc.connect(conn_string, attrs_before={sql_copt_ss_access_token: token_struct})
            self.logger.info("Connection established successfully.")

            # return the connection object
            return sql_conn

        except Exception as e:
            # Log the error and raise an HTTPException
            logger.info(f"Error connecting to SQL database: {e}")
            raise HTTPException(status_code=500, detail=f"Error connecting to SQL database: {e}")

    def get_postgres_conn(self):

        # Parse the PostgreSQL user
        db_user = urllib.parse.quote(POSTGRES_DB_CONFIG['user'])

        # Create a credential object using DefaultAzureCredential.
        self.logger.info("Creating a credential object using DefaultAzureCredential.")
        password = DefaultAzureCredential().get_token("https://ossrdbms-aad.database.windows.net/.default").token
        self.logger.info("Token obtained successfully")

        # Create the database URI
        db_uri = f"postgresql://{db_user}:{password}@{POSTGRES_DB_CONFIG['host']}/{POSTGRES_DB_CONFIG['dbname']}?sslmode={POSTGRES_DB_CONFIG['ssl_mode']}"

        # Connect to the database
        self.logger.info("Connecting to the database...")
        postgres_conn = psycopg2.connect(db_uri)
        self.logger.info("PostgreSQL connection established successfully.")
        return postgres_conn


if __name__ == "__main__":
    # Initialize the database connection
    db_connection = DatabaseConnection()

    # Get SQL connection
    # sql_con = db_connection.get_sql_conn()
    # print("SQL Connection established.")

    # Get PostgreSQL connection
    postgres_con = db_connection.get_postgres_conn()
    print("PostgreSQL Connection established.")