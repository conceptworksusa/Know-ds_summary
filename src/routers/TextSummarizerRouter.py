# Importing necessary libraries
from fastapi import APIRouter
from src.api.TextSummarizer import TextSummarizer
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

@router.post("/summarize/doc_id={doc_id}")
async def get_summary(doc_id: int, llama_model: Options = Options.model_1) -> str:
    """
    Function to get summary of the given text

    :param doc_id: The document id
    :param llama_model: The model to use for summarization
    :return: The summary of the text
    """

    # Get summary of the given text
    summary = TextSummarizer().summarize(doc_id, llama_model=llama_model)

    return summary

