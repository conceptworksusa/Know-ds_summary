# Import necessary modules
from src.conf.Configurations import logger
from src.utilities.SemanticDataInjestion import SemanticDataInjection
from fastapi import HTTPException


class DataInjectionUsingText:
    """
    This class is responsible for injecting semantic data into the database using text input.
    """
    def __init__(self):

        """
        Initializes the DataInjectionUsingText class with a logger.
        """
        self.logger = logger

    def inject_data(self, file_id: int,text: str,  model: str):
        """
        This function injects semantic data into the database using the file_id.

        Args:
            file_id: The ID of the file.
            text: The text to be injected into the database.
            model: :param model: The model to use for generating embeddings. Default is "minllm_L6_v2".

        Returns: Returns the response of the semantic data injection process.

        """
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
    data_injector = DataInjectionUsingText()


    # Inject data using file_id
    res = data_injector.inject_data(50,"Hello world", "minllm_L6_v2")

    print(res)