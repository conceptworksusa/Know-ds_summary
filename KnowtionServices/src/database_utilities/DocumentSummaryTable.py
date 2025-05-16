# Import necessary libraries
from src.scripts import sql_statements
from src.conf.Configurations import logger
from fastapi import HTTPException
from src.database_utilities.DatabaseConnection import DatabaseConnection

class DocumentSummaryTable:
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

    def  store_doc_summary(self, doc_id, summary):
        """
        Store the document summary for the given doc_id

        Args:
            doc_id: The document ID to store the summary for
            summary: The summary text to be stored

        Returns: None

        """

        try:
            # Check if the file exists in the database
            logger.info(f"Checking if the document with doc_id {doc_id} exists in the database.")

            sql = sql_statements.CHECK_IF_DOC_EXISTS.format(doc_id=doc_id)
            self.cursor.execute(sql)
            count = self.cursor.fetchone()[0]

            if count > 0:
                logger.info(f"Document with doc_id {doc_id} already exists in the database.")
                # Update the summary if it already exists
                logger.info(f"Updating the summary for doc_id: {doc_id}")
                sql = sql_statements.UPDATE_SUMMARY.format(doc_id=doc_id, summary=summary)
                self.cursor.execute(sql)
                self.conn.commit()

            else:

                # Inserting the summary into the database if it doesn't exist
                logger.info(f"Inserting the summary for doc_id: {doc_id}")
                sql = sql_statements.INSERT_SUMMARY.format(doc_id=doc_id, summary=summary)
                self.cursor.execute(sql)
                self.conn.commit()

                # now get the last inserted identity value
                logger.info("Fetching the last inserted summary ID.")
                sql = sql_statements.GET_LAST_INSERTED_SUMMARY_ID
                self.cursor.execute(sql)

                # Retrieve the inserted summary ID
                summary_id = int(self.cursor.fetchone()[0])

                logger.info(f"Updating summarization ID for doc_id: {doc_id}")
                sql = sql_statements.UPDATE_SUMMARY_ID.format(doc_id=doc_id, summary_id=summary_id)
                self.cursor.execute(sql)

                logger.info(f"Summary for doc_id {doc_id} inserted successfully.")

        except Exception as e:
            logger.error(f"Error occurred while inserting summary for doc_id {doc_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Error occurred while inserting summary for doc_id {doc_id}: {e}")

        finally:
            # Commit the changes and close the connection
            logger.info("Committing the changes to the database and closing the connection.")
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
