# Importing required libraries
from fastapi import HTTPException
from src.conf.Configurations import logger, DEFAULT_MODEL
from typing import List, Optional
from src.utilities.EmbeddingUtility import EmbeddingUtility


class EmbeddingsGenerator:
    def __init__(self, model: Optional[str] = DEFAULT_MODEL):
        """
        Initialize the EmbeddingsGenerator class with the logger
        """

        self.logger = logger

        # Get the model
        self.model = EmbeddingUtility(model).get_model()

    def get_embeddings(self, texts:List[str]) -> List[List[float]]:
        """
        Generate embeddings for the given list of texts using the model.


        Args:
            texts: List of texts to generate embeddings for.

        Returns: The generated embeddings.

        """

        try:
            # Generate embeddings for individual tokens
            logger.info("Generating embeddings for individual tokens...")
            token_embeddings = self.model.encode(texts)

            # Return the  embeddings
            return token_embeddings
        except Exception as e:
            logger.error(f"Error during token embedding: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during token embedding: {e}")


if __name__ == "__main__":

    sample_texts = ["Hello, this is a sample text",  "for generating embeddings."]

    # Create an instance of the EmbeddingsGenerator class
    embeddings_generator = EmbeddingsGenerator("all_mpnet_base_v2")

    # Generate embeddings for the sample text
    embeddings = embeddings_generator.get_embeddings(sample_texts)
    print(len(embeddings))
    print(len(embeddings[0]))

    # Print the generated embeddings
    print("Generated Embeddings: \n", embeddings)
