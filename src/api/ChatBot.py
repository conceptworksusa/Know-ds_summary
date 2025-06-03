# import necessary libraries and modules
from src.conf.Configurations import logger, SEMANTIC_CONFIGURATION
from src.utilities.ChatBotUtilities import ChatBotUtilities
from src.retrival.Retrival import Retrival
from typing import Union
from src.api.OllamaQuestionAnswer import OllamaQuestionAnswer


class ChatBot:
    def __init__(self):
        """
        This function initializes the ChatBot class.
        """
        self.logger = logger


    def get_response(self, query: str, doc_id: Union[str, int]) -> str:
        """
        This function is used to get the response for the given query and document id.

        Args:
            query: The query for which the response is to be generated.
            doc_id: The document id for which the response is to be generated.

        Returns: The response for the given query and document id.

        """

        # Get the similar documents
        self.logger.info("Getting the similar documents...")
        similar_documents  = Retrival().get_similar_documents(query, doc_id)

        if similar_documents:

            if SEMANTIC_CONFIGURATION == "BOTH":

                # Get the text from the semantically similar documents and the Tf-Idf similar documents
                self.logger.info("Getting the text from the semantically similar documents and the Tf-Idf similar documents...")
                context = ChatBotUtilities().get_sematic_similar_documents_text(similar_documents) + ChatBotUtilities().get_tf_idf_similar_documents_text(similar_documents)

            elif SEMANTIC_CONFIGURATION == "Tf_Idf":

                # Get the text from the Tf-Idf similar documents
                self.logger.info("Getting the text from the Tf-Idf similar documents...")
                context = ChatBotUtilities().get_tf_idf_similar_documents_text(similar_documents)

            else:

                # Get the text from the semantically similar documents
                self.logger.info("Getting the text from the semantically similar documents...")
                context = ChatBotUtilities().get_sematic_similar_documents_text(similar_documents)

            if context:
                # Call the Ollama service to get the response
                self.logger.info("Calling the Ollama service to get the response...")
                response = OllamaQuestionAnswer().qa_with_ollama(context, [query])
            else:
                response = "No relevant information found in the database."

            return response

        else:
            return "Error occurred while processing the request "


if __name__ == "__main__":

    res = ChatBot().get_response("What is date of birth of Shawn P Plouffe?", 99913)

    print(res)
