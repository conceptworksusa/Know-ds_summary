# Importing required libraries
from src.conf.Configurations import logger
from src.conf.Configurations import model_paths
from fastapi import HTTPException
from sentence_transformers import SentenceTransformer



class EmbeddingUtility:
    def __init__(self, model: str):
        """
        This function initializes the LateChunking class with the specified model path.
        """

        # Set the model name
        self.model_name = model_paths[model]

        try:
            # Load the model
            logger.info(f"Loading model from {model}...")
            self.model = SentenceTransformer(self.model_name)

        except Exception as e:
            # Log the error
            logger.error(f"Error during model loading: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during model loading: {e}")

    def get_model(self):
        """
        This function returns the model.
        :return: Model
        """

        # Return the model
        return self.model
