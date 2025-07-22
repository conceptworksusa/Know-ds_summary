from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_ollama.llms import OllamaLLM

from ragas.evaluation import evaluate
from ragas.metrics import context_precision, context_recall
from datasets import Dataset


# 1. Load sample documents
def load_documents():
    docs = [
        Document(page_content="India won its independence in 1947."),
        Document(page_content="The capital of India is New Delhi."),
        Document(page_content="Python is a popular programming language."),
    ]
    return docs


# 2. Split and embed the documents into FAISS
def embed_and_store(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(chunks, embedding=embeddings)
    return db


# 3. Get answer from local LLM using LangChain's RetrievalQA
def get_answer(llm, vectordb, question):
    retriever = vectordb.as_retriever()
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa.run(question)


# 4. Prepare RAGAS dataset with required columns
def prepare_ragas_dataset(question, answer, contexts, reference):
    dataset = Dataset.from_dict({
        "question": [question],
        "answer": [answer],
        "contexts": [[ctx.page_content for ctx in contexts]],
        "reference": [reference],  # Required for context_precision
    })
    return dataset


# 5. Run RAGAS evaluation
def run_evaluation(llm, dataset):
    result = evaluate(
        dataset,
        metrics=[context_precision, context_recall],
        llm=llm,
    )
    print(result)


# 6. Main
if __name__ == "__main__":
    documents = load_documents()
    vectordb = embed_and_store(documents)

    # Use your local Ollama model (llama3.2:1b should be pulled via Ollama CLI)
    local_llm = OllamaLLM(model="llama3.2:1b", base_url="http://localhost:11434")

    question = "When did India become independent?"
    reference = "India won its independence in 1947."

    answer = get_answer(local_llm, vectordb, question)
    context = vectordb.similarity_search(question, k=2)

    dataset = prepare_ragas_dataset(question, answer, context, reference)
    run_evaluation(local_llm, dataset)
