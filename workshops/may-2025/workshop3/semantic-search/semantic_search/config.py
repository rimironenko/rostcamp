# Configuration settings for the semantic search application
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API configurations
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-small"  # Default model

# ChromaDB configurations
CHROMA_PERSIST_DIRECTORY = "./chroma_db"
DEFAULT_COLLECTION_NAME = "documents"
SIMILARITY_METRIC = "cosine"  # Options: cosine, euclidean, dot_product

# Document processing configurations
CHUNK_SIZE = 200  # Reduced size of text chunks in characters (originally 1000)
CHUNK_OVERLAP = 50  # Reduced overlap between chunks to maintain context (originally 200)
MAX_CHUNKS_PER_BATCH = 3  # Maximum number of chunks to process in a single batch

# Search configurations
DEFAULT_SEARCH_RESULTS = 5  # Default number of results to return