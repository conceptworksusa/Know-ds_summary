# Importing the required libraries
from psycopg2.extras import execute_values
from src.conf.Configurations import logger
from src.conf.Configurations import NUMBER_OF_MATCHES_FOR_SEMANTIC_RETRIEVAL
from fastapi import HTTPException
from src.database_utilities.DatabaseConnection import DatabaseConnection


class DocumentEmbeddingsTable:
    def __init__(self):
        """
        This function initializes the DataBaseUtility class with the specified database configuration.
        """
        try:

            # Connect to the database
            logger.info("Getting the database connection...")
            self.conn =DatabaseConnection().get_postgres_conn()

            # Create a cursor object
            self.cursor = self.conn.cursor()
        except Exception as e:
            logger.error(f"Error during initialization of the database connection: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during database connection: {e}")


    # Function to store chunks in the database
    def store_chunks_in_db(self,start_pages, end_pages, chunks, embeddings, doc_id: int):
        """
        This function stores the chunks in the database with a unique doc_id.
        :param chunks: The list of chunks.
        :param embeddings: The list of embeddings.
        :param doc_id: The document ID.
        :return: None
        """

        # # Drop the table if it exists
        # logger.info("Dropping the table if it exists...")
        # self.cursor.execute("DROP TABLE IF EXISTS document_embeddings;")
        try:
            # Create the table if it doesn't exist
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS document_embeddings (
                    doc_id int,
                    start_page int,  -- Start page number
                    end_page int,    -- End page number
                    chunk_id int,  -- Auto-incrementing chunk ID
                    chunk TEXT,
                    embeddings vector
                );
            """)

        except Exception as e:
            logger.error(f"Error during table creation: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during table creation: {e}")

        try:

            chunk_ids = range(1,len(chunks)+1)

            # Creating the values to be inserted
            values = [(doc_id, start_page, end_page, chunk_id, chunk, chunk_embedding.astype(float).tolist()) for start_page, end_page, chunk_id, chunk, chunk_embedding in zip(start_pages, end_pages, chunk_ids, chunks, embeddings)]

            # Creating the insert query
            query = "INSERT INTO document_embeddings (doc_id, start_page, end_page, chunk_id, chunk, embeddings) VALUES %s"

            # Using execute_values to insert the data in bulk
            execute_values(self.cursor, query, values)

            # Commit the changes
            logger.info(f"Committing the changes for document id :  {doc_id}")
            self.conn.commit()


        except Exception as e:
            logger.error(f"Error during insertion of chunks: {e}")
            raise HTTPException(status_code=422, detail=f"An error occurred during insertion of chunks: {e}")
        finally:
            self.cursor.close()
            self.conn.close()


    def fetch_similar_text(self, query_embedding, doc_id):
        """
        This function retrieves all matches for the query sorted by similarity in descending order.
        :param query_embedding: The embedding of the query.
        :param doc_id: The document ID to exclude from the search.
        :return: The results sorted by similarity in descending order.
        """

        try:
            # Retrieve all matches sorted by similarity in descending order
            logger.info("Retrieving all matches for the query...")
            self.cursor.execute(
                """
                SELECT chunk, 1 - (embeddings <=> %s::vector) AS similarity
                FROM claimbrain.document_embeddings Where doc_id = %s
                ORDER BY similarity DESC
                LIMIT %s;
                """,
                (query_embedding.tolist(), doc_id, NUMBER_OF_MATCHES_FOR_SEMANTIC_RETRIEVAL)
            )

            # Fetch the results
            logger.info("Fetching the results...")
            results = self.cursor.fetchall()

            # Return the results
            return results

        except Exception as e:
            logger.error(f"Error during retrieval of similar text: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during retrieval of similar text: {e}")

        finally:
            # Close the cursor and connection
            logger.info("Closing the cursor and connection...")
            self.cursor.close()
            self.conn.close()

    def document_exists(self, doc_id):
        """
        Checks if a document with the given name already exists in the database.
        :param doc_id: The document ID to check.
        :return: True if document exists, otherwise False.
        """
        try:
            self.cursor.execute("SELECT COUNT(*) FROM document_embeddings WHERE doc_id = %s", (doc_id,))
            count = self.cursor.fetchone()[0]
            return count > 0
        except Exception as e:
            if "does not exist" in str(e):
                return False
        finally:
            # Close the cursor and connection
            logger.info("Closing the cursor and connection...")
            self.cursor.close()
            self.conn.close()

    def get_all_document_ids(self):
        """
        Fetches all document IDs from the database in the order they are stored.
        :return: List of document IDs.
        """
        try:
            # Fetch all document IDs in order
            logger.info("Fetching all document IDs in order...")
            self.cursor.execute("SELECT DISTINCT doc_id FROM claimbrain.document_embeddings ORDER BY doc_id;")
            doc_ids = [row[0] for row in self.cursor.fetchall()]  # Extracting IDs from tuples

            # Return the document IDs
            return doc_ids

        except Exception as e:
            logger.error(f"Error during retrieval of document IDs: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during retrieval of document IDs: {e}")

        finally:
            # Close the cursor and connection
            logger.info("Closing the cursor and connection...")
            self.cursor.close()
            self.conn.close()
