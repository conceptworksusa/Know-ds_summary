# Import necessary modules
from src.conf.Configurations import logger
from src.utilities.SemanticDataInjestion import SemanticDataInjection
from fastapi import HTTPException
from src.database_utilities.DocumentOcrBlockTable import DocumentOcrBlock


class DataInjectionUsingFileID:
    def __init__(self):
        self.logger = logger

    def inject_data(self, file_id: int, model: str):
        """
        This function injects semantic data into the database using the file_id.
        Args:
            file_id: The ID of the file.
            model: :param model: The model to use for generating embeddings. Default is "minllm_L6_v2".

        Returns: Returns the response of the semantic data injection process.

        """
        try:

            # get text using file_id from DocumentOcrBlock table
            self.logger.info(f"Getting text using file_id: {file_id}")
            text = DocumentOcrBlock().get_document_text_by_id(file_id)
        except Exception as e:
            self.logger.error(f"Error getting text using file_id: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred getting text using file_id: {e}")
        try:
            # Inject semantic data
            self.logger.info("Injecting semantic data...")
            response = SemanticDataInjection().inject_semantic_data(text, file_id, model)

            # Return the response
            return response

        except Exception as e:
            self.logger.error(f"Error injecting semantic data: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred injecting semantic data: {e}")



if __name__ == "__main__":
    # Initialize the data injector
    data_injector = DataInjectionUsingFileID()

    # Inject data using file_id
    res = data_injector.inject_data(99913, "minllm_L6_v2")

    print(res)
