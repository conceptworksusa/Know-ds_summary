# Importing required libraries
from src.conf.Configurations import logger, CHUNK_SIZE_FOR_EMBEDDINGS
from src.api.EmbeddingsGenerator import EmbeddingsGenerator
from src.database_utilities.DocumentEmbeddingsTable import DocumentEmbeddingsTable
from fastapi import HTTPException
import numpy as np


class SemanticRetrival:
    def __init__(self):
        # Initialize the logger
        self.logger = logger

    def retrieve_relevant_docs(self, query, doc_id):
        """
        This function retrieves relevant text based on the query.
        :param query: The query to search for.
        :param doc_id: The document id to exclude from the search.
        :return: List of tuples containing the text chunk and similarity score.
        """

        # Get the tokens by splitting the text into chunks
        tokens = query.split()

        # Creating chunks by splitting the text into chunks with a specified size
        self.logger.info(f"Tokenizing text...  With chunk size: {CHUNK_SIZE_FOR_EMBEDDINGS}")
        chunks = [" ".join(tokens[i:i + CHUNK_SIZE_FOR_EMBEDDINGS]) for i in
                  range(0, len(tokens), CHUNK_SIZE_FOR_EMBEDDINGS)]

        # Generate embeddings for individual chunks
        embeddings = EmbeddingsGenerator().get_embeddings(chunks)

        try:
            # Get the mean of the embeddings
            self.logger.info("Getting the mean of the embeddings...")
            query_embedding = np.mean(embeddings, axis=0)
        except Exception as e:
            self.logger.error(f"Error in getting the mean of the embeddings: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during mean embedding: {e}")

        # Fetch similar text from the database
        self.logger.info("Fetching similar text from the database...")
        result = DocumentEmbeddingsTable().fetch_similar_text(query_embedding, doc_id)

        return result

if __name__ == "__main__":
    # Sample query
    sample_query = "What is the name of Patient?"

    # Retrieve relevant text
    results = SemanticRetrival().retrieve_relevant_docs(sample_query, 99913)

    for chunk, similarity in results:
        print(f"Chunk: {chunk}\nSimilarity: {similarity}\n")
