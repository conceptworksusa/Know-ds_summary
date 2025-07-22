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


# Set Ollama LLM
ollama_llm = OllamaLLM(base_url="http://127.0.0.1:11434", model="llama3.2:1b")
model = SentenceTransformer(r"C:\llm\MiniLM-L6-v2")

data = {
    "question": ["What is RAG?", "What is RAGAS?"],
    "reference": [
        "RAG stands for Retrieval Augmented Generation. It's a method to improve the accuracy of language models by providing them with relevant context from external sources.",
        "RAGAS is a framework for evaluating RAG-based LLM systems."
    ],
    "answer": [
        "RAG is a method to improve the accuracy of language models by providing them with relevant context from external sources.",
        "RAGAS is a framework for evaluating RAG-based LLM systems."
    ],
    "ground_truths": [
        ["RAG is a method to improve the accuracy of language models by providing them with relevant context from external sources."],
        ["RAGAS is a framework for evaluating RAG-based LLM systems."]
    ],
    "retrieved_contexts": [
        ["RAG stands for Retrieval Augmented Generation. It's a method to improve the accuracy of language models by providing them with relevant context from external sources."],
        ["RAGAS is a framework for evaluating RAG-based LLM systems."]
    ]
}

eval_dataset = Dataset.from_dict(data)

# Define metrics
faithfulness = Faithfulness()
answer_relevancy = AnswerRelevancy()
context_precision = ContextPrecision()
context_recall = ContextRecall()

# Evaluate
results = evaluate(
    eval_dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    ], llm=ollama_llm, embeddings=model
)

# Print results
print(results)
