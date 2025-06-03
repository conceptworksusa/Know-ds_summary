from src.conf.Configurations import logger, db_config
import psycopg2


class DatabaseConnection:
    def __init__(self):
        self.logger = logger

    def get_postgres_conn(self):

        # Connect to the database
        logger.info("Connecting to the database...")
        postgres_conn = psycopg2.connect(**db_config)


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
