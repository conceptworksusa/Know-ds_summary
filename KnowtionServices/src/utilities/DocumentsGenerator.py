from src.conf.Configurations import CHUNK_SIZE_FOR_SUMMARIZATION, CHUNK_OVERlAP_FOR_SUMMARIZATION, MAX_TOKENS_FOR_SUMMARIZATION
from langchain_text_splitters import TokenTextSplitter
from langchain.docstore.document import Document
from fastapi import HTTPException
from src.conf.Configurations import logger


class DocumentsGenerator:
    def __init__(self):
        self.logger = logger


    def create_documents(self, text: str) -> list[Document]:
        """
        This function creates Document objects for each chunk of text.
        Args:
            text: The text to split into chunks and create Document objects.

        Returns: A list of Document objects containing the text chunks

        """

        try:

            # Split the text into chunks for summarization
            self.logger.info("Splitting the text into chunks for summarization")
            splitter = TokenTextSplitter(chunk_size=CHUNK_SIZE_FOR_SUMMARIZATION, chunk_overlap=CHUNK_OVERlAP_FOR_SUMMARIZATION)
            chunks = splitter.split_text(text)

            if len(chunks) * CHUNK_SIZE_FOR_SUMMARIZATION > MAX_TOKENS_FOR_SUMMARIZATION:
                # Create Document objects for the first max_tokens//chunk_size chunks if the document is too large
                documents = [Document(page_content=chunk) for chunk in chunks[:MAX_TOKENS_FOR_SUMMARIZATION // CHUNK_SIZE_FOR_SUMMARIZATION]]
                return documents
            else:
                # Create Document objects for each chunk
                self.logger.info("Creating Document objects for each chunk")
                documents = [Document(page_content=chunk) for chunk in chunks]

                # Return the list of Document objects
                return documents

        except Exception as e:
            # Log the error while processing the text data and raise an HTTPException
            self.logger.info(f"Error while processing the text data: {str(e)}")
            raise HTTPException(status_code=500, detail="Error while processing the text data")
