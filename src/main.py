# Importing necessary classes
from fastapi import FastAPI
from src.routers.ChatBotRouter import router as chatbot_router
from src.routers.TextSummarizerRouter import router as text_summarizer_router
from src.routers.TextCustomSummarizerRouter import router as text_custom_summarizer_router
from src.routers.OllamaQuestionAnsRouter import router as ollama_qa_router
from src.routers.OllamaSummarizerRouter import router as ollama_summarizer_router
from src.routers.EmbeddingsGeneratorRouter import router as embeddings_generator_router
from src.routers.OllamaCustomSummarizerRouter import router as ollama_custom_summarizer_router
from src.routers.DataInjectionUsingFileIDRouter import router as data_injection_using_file_id_router
from src.routers.TextSummarizeAndStoreRouter import router as text_summarize_and_store_router

from fastapi.middleware.cors import CORSMiddleware
# Initialize the FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Include the chatbot router
app.include_router(chatbot_router)

# Include the text summarizer router
app.include_router(text_summarizer_router)

# Include the text custom summarizer router
app.include_router(text_custom_summarizer_router)

# Include the ollama router
app.include_router(ollama_qa_router)

# Include the ollama summarizer router
app.include_router(ollama_summarizer_router)

# Include the custom summarizer router
app.include_router(ollama_custom_summarizer_router)

# Include the embeddings generator router
app.include_router(embeddings_generator_router)

# Include the data injection using file ID router
app.include_router(data_injection_using_file_id_router)

# Include the text summarize and store router
app.include_router(text_summarize_and_store_router)
