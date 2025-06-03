# Importing necessary libraries
from fastapi import APIRouter
from src.injestion.DataInjectionUsingFileID import DataInjectionUsingFileID
from typing import Optional
from enum import Enum

# Initialize the router
router = APIRouter(tags=["Ingestion"], prefix="/ingestion")

# Define the available models for summarization
class Options(str, Enum):
    """
    Enum class to define the available options for summarization.
    """
    model_1  = "minllm_L6_v2"   # Llama 3.1:latest model
    model_2 = "all_mpnet_base_v2"     # Mistral:latest model

# Define the route for the root endpoint
@router.post("/file_id/")
def inject_sematic_info(file_id: int, model: Optional[Options] = Options.model_1):
    """
    This function injects semantic data into the database using the file_id.

    Args:
        file_id: The ID of the file.
        model: :param model: The model to use for generating embeddings. Default is "minllm_L6_v2".

    Returns: Response from the DataInjectionUsingFileID service.

    """

    # Call the DataInjectionUsingFileID service to inject data
    response = DataInjectionUsingFileID().inject_data(file_id, model)

    return response
