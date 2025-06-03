# Importing the required libraries and modules
from langchain.chains import load_summarize_chain
from src.utilities.OllamaPipeline import OllamaPipeline
from src.utilities.DocumentsGenerator import DocumentsGenerator
from langchain import PromptTemplate
from src.conf.Configurations import VERBOSE
from fastapi import HTTPException
from src.conf.Prompts import final_combine_prompt, system_prompt, additional_prompt
from src.conf.Configurations import logger, DEFAULT_LLAMA_MODEL
from typing import Optional


class OllamaSummarizer:
    def __init__(self, llama_model: Optional[str] = DEFAULT_LLAMA_MODEL,  prompt: Optional[str] = system_prompt ):
        """
        Initialize the OllamaSummarizer class with the specified model and prompt.

        Args:
            llama_model: The model to use for summarization. Default is "llama3.1".
            prompt: The system prompt to use for the summarization model. Default is system_prompt.
        """

        # Initialize the logger
        self.logger = logger

        # Set the system prompt for the summarization model
        self.system_prompt = prompt + additional_prompt

        try:
            # Initialize the OllamaPipeline model
            self.llm = OllamaPipeline(llama_model).get_model()
            self.logger.info(f"Initialized the OllamaPipeline model")

        except Exception as e:
            self.logger.info(f"Error initializing the OllamaPipeline model: {str(e)}")
            raise HTTPException(status_code=500, detail="Error initializing the OllamaPipeline model")

    def get_stuff_summary_chain(self):
        """
        Get the summarization chain for summarizing small documents using the stuff technique

        Returns: Returns the summarization chain for summarizing small documents using the stuff technique
        """
        # If there is only one chunk, summarize it using the stuff chain
        logger.info("Summarizing the single chunk using the stuff chain")
        prompt = PromptTemplate(
            input_variables=['text'],
            template=self.system_prompt
        )

        # Load the summarize chain with the stuff technique
        logger.info("Loading the summarize chain with the stuff technique")

        # Load the summarize chain with the stuff technique
        stuff_chain = load_summarize_chain(
            self.llm,
            chain_type='stuff',
            prompt=prompt,
            verbose=VERBOSE
        )

        return stuff_chain

    def get_map_reduce_summary_chain(self):
        """
        Get the summarization chain for summarizing large documents using the map-reduce technique

        Returns: The summarization chain for summarizing large documents using the map-reduce technique

        """

        # Creating a map prompt template for summarizing the chunks
        map_prompt_template = PromptTemplate(input_variables=['text'],
                                             template=self.system_prompt)

        # Creating a combine prompt template for combining the intermediate summaries
        final_combine_prompt_template = PromptTemplate(input_variables=['text'],
                                                       template=final_combine_prompt)
        # Load the summarize chain with the map-reduce technique
        logger.info("Loading the summarize chain with the map-reduce technique")
        map_reduce_chain = load_summarize_chain(
            llm=self.llm,
            chain_type='map_reduce',
            map_prompt=map_prompt_template,
            combine_prompt=final_combine_prompt_template,
            verbose=VERBOSE
        )

        return map_reduce_chain

    def summarize_text(self, text: str) -> str:
        """
        Get the summary of the document using the map-reduce summarization technique

        Args:
            text: The text to summarize

        Returns: The final summary of the document
        """

        # Get the data from the CSV file based on the document ID
        logger.info("getting Langchain document format from text")
        documents = DocumentsGenerator().create_documents(text)

        try:

            if len(documents) == 1:
                # Get the summarization chain for summarizing small documents using the stuff technique
                logger.info("Getting the summarization chain for summarizing small documents using the stuff technique")
                summary_chain = self.get_stuff_summary_chain()

            else:
                # Get the summarization chain for summarizing large documents using the map-reduce technique
                logger.info("Getting the summarization chain for summarizing large documents using the map-reduce technique")
                summary_chain = self.get_map_reduce_summary_chain()

            # Run the summarization chain on the documents
            logger.info("Running the summarization chain on the documents")
            output = summary_chain.invoke(documents)

            return output['output_text']

        except Exception as e:
            # Log the error while summarizing the documents and raise an HTTPException
            self.logger.info(f"Error summarizing the documents: {str(e)}")
            raise HTTPException(status_code=500, detail="Error summarizing the documents")


if __name__ == "__main__":

    summarizer = OllamaSummarizer()
    # sample_text = "This is a test document. It is a test document for summarization. It is a test document for summarization using the map-reduce technique."
    sample_text = """
    {
  "DemographicsInfo": {
    "PatientDateOfBirth": "2000-07-09T00:00:00",
    "PatientGender": "M",
    "PatientAddress": "25096 150TH ST",
    "PatientCity": "DIKE",
    "PatientState": "IA",
    "PatientZip": "50624",
    "PatientControlNumber": "40126829607",
    "ServiceDateFrom": "2023-07-05T00:00:00",
    "ServiceDateThrough": "2023-07-10T00:00:00",
    "Facility": "ALLEN HOSPITAL",
    "FacilityAddress": "1825 LOGAN AVE",
    "NPI": "1336231091",
    "TaxID": "420698265",
    "RepresentativeName": null,
    "RepresentativeTitle": null,
    "RepresentativeEmail": null,
    "AccountNumber": "401268296",
    "MedicalRecordNumber": null,
    "PatientFirstName": "Matthew",
    "PatientLastName": "Wagner",
    "PatientNameFirstLast": "Matthew Wagner",
    "PatientNameLastFirst": "Wagner, Matthew",
    "BillDate": "2024-12-05",
    "ClaimControlNumber": null,
    "FacilityCity": "WATERLOO",
    "FacilityState": "IA",
    "FacilityZip": "507031916",
    "FacilityCityStateZip": "WATERLOO, IA 507031916",
    "FacilityPhone": null,
    "GuarantorFirstName": null,
    "GuarantorLastName": null,
    "GuarantorAddress": null,
    "GuarantorCity": null,
    "GuarantorState": null,
    "GuarantorZip": null,
    "AttentionTo": null,
    "PayerName": "IOWA TOTAL CARE",
    "PayerAddress1": "PO BOX 843151",
    "PayerAddress2": null,
    "PayerCity": "KANSAS CITY",
    "PayerState": "MO",
    "PayerZip": "641843151",
    "PayerPhone": null,
    "PayerFax": null,
    "SubscriberFirstName": "MATTHEW",
    "SubscriberLastName": "WAGNER",
    "SubscriberId": "2142439I",
    "SubscriberDateOfBirth": "2000-07-09T00:00:00",
    "SubscriberGroupName": "IOWA TOTAL CARE",
    "SubscriberGroupNumber": null
  }
}"""

    print(summarizer.summarize_text(sample_text))
