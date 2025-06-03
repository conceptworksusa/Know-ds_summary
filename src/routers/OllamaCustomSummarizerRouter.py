# Importing necessary classes
from fastapi import APIRouter
from src.api.OllamaSummarizer import OllamaSummarizer
from typing import Optional
from src.conf.Prompts import system_prompt
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


@router.post("/ollama/custom-summarization/")
async def summarize_text_custom(text: str, prompt: Optional[str] = system_prompt, llama_model: Optional[Options] = Options.model_1):
    """
    Summarizes the given context using the Ollama model.

    Args:
        text: The text to summarize.
        prompt: Optional prompt to guide the summarization.
        llama_model: The model to use for summarization. Default is "llama3.1".

    Returns:
        str: The generated summary.

    """

    # Check if the prompt is valid
    if prompt and prompt.strip() == "":
        return "Give a valid prompt to summarize the text"

    # Get the summary of the given text
    summary = OllamaSummarizer(llama_model=llama_model, prompt=prompt).summarize_text(text)

    #define the structure of the response
    return summary
