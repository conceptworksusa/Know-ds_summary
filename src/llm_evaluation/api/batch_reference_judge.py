from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import Optional
from fastapi import HTTPException
from KnowtionPOC.intent_classification.utilities.OllamaPipeline import OllamaPipeline
from KnowtionPOC.intent_classification.conf.Configurations import DEFAULT_LLAMA_MODEL , logger
from KnowtionPOC.intent_classification.conf.Prompts import BATCH_CONTEXT_RELEVANCE_PROMPT


class EvalBatchContextRelevance(BaseModel):
    questions: list  = Field(..., description="List of questions or prompts that were used to evaluate the context relevance.")
    contexts: list = Field(..., description="List of contexts or reference texts against which the questions are evaluated.")
    Response: list = Field(..., description="List of answers to the questions which are either Relevant or Not Relevant.")

class RagBasedJudge:


    def __init__(self, llama_model: Optional[str] = DEFAULT_LLAMA_MODEL):
         # Initialize the logger
         self.logger = logger

         try:
             # Initialize the OllamaPipeline model
             self.llm = OllamaPipeline(llama_model).get_model()
             self.logger.info("Ollama model initialized successfully")

         except Exception as e:
             self.logger.info(f"Error initializing the OllamaPipeline model: {str(e)}")
             raise HTTPException(status_code=500, detail="Error initializing the OllamaPipeline model")

    def batch_context_relevance(self, questions: list, contexts: list, system_prompt: Optional[str] = BATCH_CONTEXT_RELEVANCE_PROMPT):
        """
        Evaluate the relevance of a batch of contexts to their corresponding questions.
        Args:
            questions: List of questions or prompts that were used to evaluate the context relevance.
            contexts: List of contexts or reference texts against which the questions are evaluated.
            system_prompt: The system prompt to guide the evaluation process.

        Returns: Returns an EvalBatchContextRelevance object containing the evaluation results for each question-context pair.

        """
        # Check if the lengths of questions and contexts match
        if len(questions) != len(contexts):
            raise HTTPException(status_code=400, detail="Questions and contexts must have the same length.")

        parser = PydanticOutputParser(pydantic_object=EvalBatchContextRelevance)

        prompt = PromptTemplate(
            template=system_prompt + "\n {format_instructions}\n",
            input_variables=["questions", "contexts"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )

        try:
            self.logger.info("Evaluating context relevance...")
            response = self.llm.invoke(
                input=prompt.format(questions=questions, contexts=contexts)
            )
            self.logger.info("Response received from the model.")

            # Parse the response
            parsed_response = parser.invoke(response)
            return parsed_response

        except Exception as e:
            self.logger.error(f"Error evaluating context relevance: {e}")
            raise HTTPException(status_code=500, detail="Error evaluating context relevance")


if __name__ == "__main__":
    # Example usage
    judge = RagBasedJudge()

    questions1 = ["What is the capital of France?", "Who maintains SpaceX?"]
    contexts1 = ["The capital of France is Paris.", "Elon Musk is the CEO of SpaceX and Tesla."]
    try:
        batch_result = judge.batch_context_relevance(questions1, contexts1)
        print(f"Batch Relevance Evaluation Result: {batch_result.Response}")
    except HTTPException as e:
        print(f"Error: {e}")
