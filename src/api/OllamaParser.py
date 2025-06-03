from fastapi import HTTPException
from src.conf.Configurations import logger, DEFAULT_LLAMA_MODEL
from src.utilities.OllamaPipeline import OllamaPipeline
from src.conf.Prompts import system_prompt_for_json
import json
from src.conf.FilesManager import file_paths


class OllamaParser:
    def __init__(self):
        """
        Initializes the OllamaSummarizer class.
        """

        try:
            # Initialize the Ollama model
            self.model = OllamaPipeline(DEFAULT_LLAMA_MODEL).get_model()
            logger.info("Model initialized.")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while initializing the model: {e}")

    def parsing_with_ollama(self, text: str):
        """
        parsing the given json using the Ollama model.

        Args:
            text (str): The input json to parse.

        Returns:
            str: The generated text.

        Raises:
            HTTPException: If an error occurs during model invocation.
        """

        # Construct the user prompt
        user_prompt = f"json: {text}"

        # Format the complete prompt for model invocation
        prompt = (
            "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
            f"{system_prompt_for_json}<|eot_id|><|start_header_id|>user<|end_header_id|>\n"
            f"{user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
        )

        try:
            logger.info("Invoking the model with the input prompt.")
            response = self.model.invoke(input=prompt, options={"num_ctx": 20000})
            logger.info("Response received from the model.")

            return response
        except Exception as e:
            logger.error(f"Error during model invocation: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during invocation: {e}")

    def get_story(self, file_name: str):
        """
        Parses the JSON file and generates a summary using the Ollama model.

        Args:
            file_name (str): The path to the JSON file.

        Returns:
            str: The generated summary.
        """

        # Open the JSON file and load its content
        with open(file_paths[file_name], 'r') as file:
            d = json.load(file)


        # Convert each item in the dictionary to a JSON string with key-value pairs
        final_summary = ""
        for key, value in d.items():
            json_string = f'"{key}" : {json.dumps(value)}'

            # Generate the summary using the Ollama model
            summary = self.parsing_with_ollama(json_string)

            # Append the summary to the final summary string
            final_summary += f"{summary}\n"

        return final_summary


if __name__ == "__main__":

    # Initialize the OllamaParser
    parser = OllamaParser()
    # Get the story
    fin_summary = parser.get_story('BillingStory.json')

    print(fin_summary)
