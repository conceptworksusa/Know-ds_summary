# Importing necessary classes
from fastapi import APIRouter
from src.api.OllamaSummarizer import OllamaSummarizer
from typing import Optional
from enum import Enum

# Initialize the router
router = APIRouter(
    prefix="/llm",
    tags=["core-llm-system"],
)

# Define the available models for summarization
class Options(str, Enum):
    """
    Enum class to define the available options for summarization.
    """
    model_1  = "llama3.1"   # Llama 3.1:latest model
    model_2 = "Mistral"     # Mistral:latest model


@router.post("/ollama/summarization_/")
async def summarize_text_data(text: str, llama_model: Optional[Options] = Options.model_1):
    """
    Summarizes the given context using the Ollama model.

    Args:
        text: The text to summarize.
        llama_model: The model to use for summarization. Default is "llama3.1".

    Returns:
        str: The generated summary.

    """

    # Get the summary of the given text
    summary = OllamaSummarizer(llama_model=llama_model).summarize_text(text)

    #define the structure of the response
    return summary
