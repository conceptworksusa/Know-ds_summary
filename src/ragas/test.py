from datasets import Dataset
from ragas.metrics import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall,
)
from ragas import evaluate
from langchain_ollama.llms import OllamaLLM
from sentence_transformers import SentenceTransformer
import os


class RAGASEvaluator:
    def __init__(self, ollama_url: str, ollama_model: str, embed_model_path_or_name: str):
        # Initialize Ollama LLM
        self.llm = OllamaLLM(
            base_url=ollama_url,
            model=ollama_model
        )

        # # Load sentence transformer embedding model
        # if os.path.exists(embed_model_path_or_name):
        #     pass
        #     # self.embedding_model = SentenceTransformer(embed_model_path_or_name)
        # else:
        #     print(f"⚠️ Model not found at {embed_model_path_or_name}. Downloading from HuggingFace...")
        #     self.embedding_model = SentenceTransformer(embed_model_path_or_name)
        #     self.embedding_model.save(embed_model_path_or_name)

        # Define RAGAS metrics
        self.metrics = [
            Faithfulness(),
        ]

    def evaluate_examples(self, data: dict):
        all_results = []

        for idx in range(len(data["question"])):
            single_example = {k: [v[idx]] for k, v in data.items()}
            eval_dataset = Dataset.from_dict(single_example)

            result = evaluate(
                eval_dataset,
                metrics=self.metrics,
                llm=self.llm
            )
            all_results.append(result)

        return all_results


if __name__ == "__main__":
    # Sample data
    input_data = {
        "question": [
            "What is RAG?",
            "What is RAGAS?"
        ],
        "answer": [
            "RAG is a method to improve the accuracy of language models by providing them with relevant context from external sources.",
            "RAGAS is a framework for evaluating RAG-based LLM systems."
        ],

        "retrieved_contexts": [
            ["RAG stands for Retrieval Augmented Generation. It's a method to improve the accuracy of language models by providing them with relevant context from external sources."],
            ["RAGAS is a framework for evaluating RAG-based LLM systems."]
        ]
    }

    # Initialize evaluator
    evaluator = RAGASEvaluator(
        ollama_url="http://127.0.0.1:11434",
        ollama_model="llama3.2:1b",
        embed_model_path_or_name=r"C:\llm\MiniLM-L6-v2"  # Or "sentence-transformers/all-MiniLM-L6-v2"
    )

    # Run evaluation
    results = evaluator.evaluate_examples(input_data)

    print(results)
