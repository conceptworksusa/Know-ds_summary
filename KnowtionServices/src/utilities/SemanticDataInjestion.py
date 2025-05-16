# Import required libraries
from src.conf.Configurations import logger, CHUNK_SIZE_FOR_EMBEDDINGS
from src.database_utilities.DocumentEmbeddingsTable import DocumentEmbeddingsTable
from src.api.EmbeddingsGenerator import EmbeddingsGenerator


class SemanticDataInjection :
    def __init__(self):
        """
        This function initializes the SemanticDataInjection class with the specified logger.
        """
        self.logger = logger

    def inject_semantic_data(self, text, file_id: int, model: str):
        """"
        This function tokenizes and embeds the text, performs late chunking, and stores the chunks in the database.

        Args:
            text: The text to be processed.
            file_id: The ID of the file.
            model: :param model: The model to use for generating embeddings. Default is "minllm_L6_v2".

        """

        # check the document_exits in the database
        # if SemanticTable().document_exists(file_id):
        #     self.logger.info(f"Document with file_id {file_id} already exists in the database. Skipping...")
        #     return "Document already exists"

        tokens = text.split()

        # Creating chunks by splitting the text into chunks with a specified size
        logger.info(f"Tokenizing text...  With chunk size: {CHUNK_SIZE_FOR_EMBEDDINGS}")
        chunks = [" ".join(tokens[i:i + CHUNK_SIZE_FOR_EMBEDDINGS]) for i in
                  range(0, len(tokens), CHUNK_SIZE_FOR_EMBEDDINGS)]

        # Generate embeddings for individual chunks
        embeddings = EmbeddingsGenerator(model).get_embeddings(chunks)


        # Store chunks in database
        self.logger.info("Storing chunks in the database...")
        DocumentEmbeddingsTable().store_chunks_in_db(chunks, embeddings, file_id)

        return "Semantic data injected successfully"


if __name__ == "__main__":
    sample_text = "This is a sample text for semantic data injection. It will be tokenized and embedded."
    sample_file_id = 12345
    # Initialize the semantic data injector
    semantic_data_injector = SemanticDataInjection()
    # Inject semantic data
    result = semantic_data_injector.inject_semantic_data(sample_text, sample_file_id, "minllm_L6_v2")
