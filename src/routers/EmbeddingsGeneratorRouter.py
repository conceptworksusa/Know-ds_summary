# Importing necessary libraries
from fastapi import APIRouter
from src.api.EmbeddingsGenerator import EmbeddingsGenerator
from typing import List, Optional
from enum import Enum

# Initialize the router
router = APIRouter(tags=["embeddings"])

# Define the available models for summarization
class Options(str, Enum):
    """
    Enum class to define the available options for summarization.
    """
    model_1  = "minllm_L6_v2"   # Llama 3.1:latest model
    model_2 = "all_mpnet_base_v2"     # Mistral:latest model


@router.get("/generate_embeddings/")
async def generate_embeddings(text: str, model: Optional[Options] = Options.model_1) -> List[List[float]]:
    """
        Tokenizes the text and generates embeddings for each token, handling long texts by splitting them.

        Args:
            text: :param text: The text to tokenize.
            model: :param model: The model to use for generating embeddings. Default is "minllm_L6_v2".

        Returns: The embeddings.

        """

    # Tokenize the text
    texts = text.split()

    # Get summary of the given text
    embeddings = EmbeddingsGenerator(model).get_embeddings(texts)

    return embeddings

