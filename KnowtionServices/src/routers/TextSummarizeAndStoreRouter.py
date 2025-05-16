# Importing necessary libraries
from fastapi import APIRouter
from src.api.TextSummarizeAndStore import TextSummarizeAndStore
from enum import Enum

# Initialize the router
router = APIRouter(tags=["text-summarizer"])

# Define the available models for summarization
class Options(str, Enum):
    """
    Enum class to define the available options for summarization.
    """
    model_1  = "llama3.1"   # Llama 3.1:latest model
    model_2 = "Mistral"     # Mistral:latest model

@router.post("/summarize/store/doc_id={doc_id}")
async def get_and_store_summary(doc_id: int, llama_model: Options = Options.model_1) -> str:
    """
    Service to get summary of the given text and store it in the database.

    Args:
        doc_id: The document id
        llama_model: The model to use for summarization. Default is llama3.1.

    Returns: The summary of the given document.

    """

    # Get summary of the given text
    summary = TextSummarizeAndStore().summarize_and_store(doc_id, llama_model=llama_model)

    return summary

