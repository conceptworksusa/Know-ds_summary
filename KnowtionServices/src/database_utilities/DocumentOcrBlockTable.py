# Import necessary libraries
from src.scripts import sql_statements
from src.conf.Configurations import logger
from fastapi import HTTPException
import re
from src.database_utilities.DatabaseConnection import DatabaseConnection

class DocumentOcrBlock:
    def __init__(self):
        try:

            # Getting the database connection
            logger.info("Getting the database connection...")
            self.conn = DatabaseConnection().get_sql_conn()

            # Create a cursor object
            logger.info("Creating a cursor object...")
            self.cursor = self.conn.cursor()

        except Exception as e:
            logger.error(f"Error during initialization of the database connection: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during database connection: {e}")

    def  get_document_text_by_id(self, doc_id):
        """
        Get the document text for the given doc_id

        Args:
            doc_id: The document ID to fetch the text for

        Returns: The document text

        """

        try:
            # Fetch complete document text for the given doc_id
            logger.info(f"Extracting document text for doc_id: {doc_id}")

            sql = sql_statements.GET_DOCUMENT_TEXT_BY_ID.format(doc_id = doc_id)
            self.cursor.execute(sql)

            # List of tuples like [(text1,), (text2,), ...]
            texts = self.cursor.fetchall()

            if not texts:
                logger.warning(f"Empty text found for doc_id: {doc_id}")
                return ""

            # Convert list of tuples to a single string
            document_text = " ".join(chunk[0] for chunk in texts)

            document_text = re.sub(r'\n\s*\n', '\n', document_text)


        except Exception as e:
            logger.error(f"Error fetching document chunks: {e}")
            raise HTTPException(status_code=500, detail=f"Error fetching document chunks: {e}")

        finally:
            # Commit the changes and close the connection
            logger.info("Committing the changes to the database and closing the connection.")
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

        return document_text
