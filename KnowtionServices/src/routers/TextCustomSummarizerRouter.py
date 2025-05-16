# Importing necessary libraries
from fastapi import APIRouter
from src.api.TextSummarizer import TextSummarizer
from typing import Optional
from src.conf.Prompts import system_prompt
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


@router.post("/summarize/custom/doc_id={doc_id}")
async def get_custom_summary(doc_id: int, prompt: Optional[str] = system_prompt, llama_model: Optional[Options] = Options.model_1 ) -> str:
    """
    Function to get summary of the given text

    Args:
        doc_id: The document id
        prompt: The prompt to be used for summarization
        llama_model: The model to use for summarization

    Returns: The summary of the given document.

    """

    # Check if the prompt is valid
    if prompt and prompt.strip() == "":
        return "Give a valid prompt to summarize the text"


    # Get summary of the given text
    summary = TextSummarizer().summarize(doc_id, prompt=prompt, llama_model=llama_model)

    return summary

