# Import the required modules
from src.conf.Configurations import logger, DEFAULT_LLAMA_MODEL
from src.conf.Prompts import system_prompt
from src.api.OllamaSummarizer import OllamaSummarizer
from src.database_utilities.DocumentOcrBlockTable import DocumentOcrBlock
from fastapi import HTTPException
from typing import Optional


class TextSummarizer:
    def __init__(self):
        """
        This function initializes the TextSummarizer class.
        """
        self.logger = logger


    def summarize(self, doc_id:int, prompt: Optional[str] = system_prompt, llama_model: Optional[str] = DEFAULT_LLAMA_MODEL) -> str:
        """
        Function to get summary of the given text

        Args:
            doc_id: The document id
            prompt: The prompt to be used for summarization
            llama_model: The model to use for summarization

        Returns: The summary of the text

        """
        # Get the document text by ID
        self.logger.info("Getting the document text by ID.")
        document_text = DocumentOcrBlock().get_document_text_by_id(doc_id)
        if not document_text:
            raise "Empty text found for the given doc_id."

        try:
            # Summarize the text using the OllamaSummarizer class
            logger.info("Summarizing the text using the OllamaSummarizer class")
            summary = OllamaSummarizer(llama_model, prompt).summarize_text(document_text)

            return summary
        except Exception as e:
            logger.error(f"Error occurred while summarizing the text: {e}")
            raise HTTPException(status_code=500, detail=f"Error occurred while summarizing the text: {e}")


if __name__ == "__main__":
    # Run summarization
    res = TextSummarizer().summarize(99913)
    print(res)
