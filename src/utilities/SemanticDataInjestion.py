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

    def inject_semantic_data(self, page_nums, texts, file_id: int, model: str):
        """"
        This function tokenizes and embeds the text, performs late chunking, and stores the chunks in the database.

        Args:
            text: The text to be processed.
            file_id: The ID of the file.
            model: :param model: The model to use for generating embeddings. Default is "minllm_L6_v2".

        """

        # check the document_exits in the database
        if DocumentEmbeddingsTable().document_exists(file_id):
            self.logger.info(f"Document with file_id {file_id} already exists in the database. Skipping...")
            return "Document already exists"

        # Check if the input is valid
        all_sentences = list(zip(page_nums, texts))

        # Flatten tokens while keeping page numbers
        flat_tokens = [
            (pg, token)
            for pg, txt in all_sentences
            for token in txt.split()  # simple whitespace split
        ]

        # Chunk into 128-token blocks
        chunk_size = 20
        start_pages = []
        end_pages = []
        text_chunks = []

        # Iterate through the flat tokens and create chunks
        for i in range(0, len(flat_tokens), chunk_size):
            chunk_tokens = flat_tokens[i:i + chunk_size]
            start_page = chunk_tokens[0][0]
            end_page = chunk_tokens[-1][0]
            text_chunk = " ".join(token for _, token in chunk_tokens)
            start_pages.append(start_page)
            end_pages.append(end_page)
            text_chunks.append(text_chunk)

        # Generate embeddings for individual chunks
        embeddings = EmbeddingsGenerator(model).get_embeddings(text_chunks)


        # Store chunks in database
        self.logger.info("Storing chunks in the database...")
        DocumentEmbeddingsTable().store_chunks_in_db(start_pages, end_pages, text_chunks, embeddings, file_id)

        return "Semantic data injected successfully"


if __name__ == "__main__":
    sample_text = "This is a sample text for semantic data injection. It will be tokenized and embedded."
    sample_file_id = 12345
    # Initialize the semantic data injector
    semantic_data_injector = SemanticDataInjection()
    # Inject semantic data
    result = semantic_data_injector.inject_semantic_data(sample_text, sample_file_id, "minllm_L6_v2")
