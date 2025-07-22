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
ollama_llm = OllamaLLM(
    base_url="http://127.0.0.1:11434",
    model="llama3.2:1b"
)

# Sentence transformer for embeddings
model = SentenceTransformer(r"C:\llm\MiniLM-L6-v2")

# Your input data
data = {
    "question": [
        "What is RAG?",
        "What is RAGAS?"
    ],
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

# Define metrics
faithfulness = Faithfulness()
answer_relevancy = AnswerRelevancy()
context_precision = ContextPrecision()
context_recall = ContextRecall()

# Evaluate each example serially to avoid timeouts
all_results = []
for idx in range(len(data["question"])):
    single_example = {
        k: [v[idx]] for k, v in data.items()
    }
    eval_dataset = Dataset.from_dict(single_example)

    result = evaluate(
        eval_dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ],
        llm=ollama_llm,
        embeddings=model
    )

    all_results.append(result)

# Print all results
for i, res in enumerate(all_results, 1):
    print(f"\n✅ Result for Example {i}:")
    for metric, value in res.items():
        print(f"  {metric}: {value:.4f}")
