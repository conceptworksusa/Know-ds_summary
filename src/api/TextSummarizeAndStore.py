# Import the required modules
from src.conf.Configurations import logger, DEFAULT_LLAMA_MODEL
from src.conf.Prompts import system_prompt
from src.api.OllamaSummarizer import OllamaSummarizer
from src.database_utilities.DocumentOcrBlockTable import DocumentOcrBlock
from fastapi import HTTPException
from typing import Optional
from src.database_utilities.DocumentSummaryTable import DocumentSummaryTable


class TextSummarizeAndStore:
    def __init__(self):
        """
        Initialize the TextSummarizeAndStore class.
        """
        self.logger = logger


    def  summarize_and_store(self, doc_id:int, prompt: Optional[str] = system_prompt, llama_model: Optional[str] = DEFAULT_LLAMA_MODEL) -> str:
        """
        Function to get summary of the given text and store it in the database.

        Args:
            doc_id: The document id
            prompt: The prompt to use for summarization. Default is system_prompt.
            llama_model: The model to use for summarization. Default is DEFAULT_LLAMA_MODEL.

        Returns: The summary of the given document.

        """

        # Get the document text by ID
        self.logger.info("Getting the document text by ID.")
        document_text = DocumentOcrBlock().get_document_text_by_id(doc_id)
        if not document_text:
            raise "Empty text found for the given doc_id."

        try:
            # Summarize the text using the OllamaSummarizer class
            self.logger.info("Summarizing the text using the OllamaSummarizer class")
            summary = OllamaSummarizer(llama_model, prompt).summarize_text(document_text)
        except Exception as e:
            self.logger.error(f"Error occurred while summarizing the text: {e}")
            raise HTTPException(status_code=500, detail=f"Error occurred while summarizing the text: {e}")

        # Store the summary in the database
        self.logger.info("Storing the summary in the database.")
        DocumentSummaryTable().store_doc_summary(doc_id, summary)

        # Return the summary
        return summary

if __name__ == "__main__":
    # Run summarization
    res = TextSummarizeAndStore().summarize_and_store(99913)
    print(res)
