# import the necessary libraries
from src.conf.Configurations import logger
from src.retrival.SemanticRetrival import SemanticRetrival
# from src.retrival.Tf_Idf_Retrival import TfIdfRetrival
from fastapi import HTTPException

class Retrival:
    @staticmethod
    def get_similar_documents(query: str, doc_id):
        """
        Get similar documents for the given query using semantic retrival and tf-idf retrival

        :param query: The query for which to find similar documents
        :param doc_id: The document id for which to find similar documents
        :return: The similar documents
        """

        try:
            # Get similar documents using semantic retrival
            logger.info("Retrieving similar documents using semantic retrival")
            semantic_similar_documents = SemanticRetrival().retrieve_relevant_docs(query, doc_id)
            logger.info("similar documents retrieved using semantic retrival")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred during semantic retrival: {e}")


        # try:
        #     # Get similar documents using tf-idf retrival
        #     logger.info("Retrieving similar documents using tf-idf retrival")
        #     tf_idf_similar_documents = TfIdfRetrival().retrieve_relevant_docs(query, doc_id)
        #     logger.info("similar documents retrieved using tf-idf retrival")
        # except Exception as e:
        #     raise HTTPException(status_code=500, detail=f"An error occurred during tf-idf retrival: {e}")
        #
        # # Return the similar documents
        # logger.info("Returning the similar documents")
        # response = {"semantic_similar_documents": semantic_similar_documents, "tf_idf_similar_documents": tf_idf_similar_documents}

        response = {"semantic_similar_documents": semantic_similar_documents}

        return response


if __name__ == "__main__":

    sample_query = " multiple chondral loose bodies were identified in the patellofemoral joint as well.. medial and lateral gutters were notable for several chondral loose bodies."

   # Get similar documents
    similar_documents = Retrival().get_similar_documents(sample_query, 1075)

    print(similar_documents)
