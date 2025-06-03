# Import necessary libraries
from fastapi import APIRouter
from src.injestion.DataInjectionUsingText import DataInjectionUsingText
from typing import Optional
from enum import Enum

# Initialize the router
router = APIRouter(tags=["Ingestion"], prefix="/ingestion")

# Define the available models for summarization
class Options(str, Enum):
    """
    Enum class to define the available options for summarization.
    """
    # Choose which model to use for semantic data injection
    model_1 = "minllm_L6_v2"
    model_2 = "all_mpnet_base_v2"

# Define the route for the root endpoint
@router.post("/text/")
def inject_sematic_info(file_id: int, text: str, model: Optional[Options] = Options.model_1):

    """
    This function injects semantic data into the database using the file_id and text.

    Args:
        file_id: The ID of the file.
        text: The text to be injected into the database.
        model: :param model: The model to use for generating embeddings. Default is "minllm_L6_v2".

    Returns: Response from the DataInjectionUsingText service.
    """

    # Call the DataInjectionUsingText service to inject data
    response = DataInjectionUsingText().inject_data(file_id, text, model)

    return response