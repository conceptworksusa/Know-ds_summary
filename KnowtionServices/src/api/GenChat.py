# Importing necessary classes
from src.utilities.OllamaPipeline import OllamaPipeline
from src.conf.Configurations import logger
from fastapi import HTTPException
from src.conf.Configurations import DEFAULT_LLAMA_MODEL


class GenChat:
    def __init__(self):
        # Initialize the logger
        self.logger = logger

        try:
            # Initialize the OllamaPipeline model
            self.llm = OllamaPipeline(DEFAULT_LLAMA_MODEL).get_model()
            self.logger.info("Ollama model initialized successfully")

        except Exception as e:
            self.logger.info(f"Error initializing the OllamaPipeline model: {str(e)}")
            raise HTTPException(status_code=500, detail="Error initializing the OllamaPipeline model")

    def chat(self, query):
        # Invoke the model with the chat structure
        try:
            system_prompt = "You are a helpful and knowledgeable assistant. Respond to user questions clearly and concisely."

            # Define prompt structure for the Llama3 model for question answering task
            llama3_prompt_for_qa = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

                {system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

                {query}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

            # Directly invoke the model with the formatted prompt
            self.logger.info("invoking the model with input message")
            response = self.llm.invoke(input=llama3_prompt_for_qa)
            self.logger.info("response received from the model")

            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred during invocation: {e}")


if __name__ == "__main__":

    res = GenChat().chat("what is capital of india?")

    print(res)

