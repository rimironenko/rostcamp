from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# ChromaDB configuration
CHROMA_PATH = os.getenv("CHROMA_PATH", "./data/chroma")
CHROMA_PATH = Path(CHROMA_PATH)
CHROMA_PATH.mkdir(parents=True, exist_ok=True)

# Model configuration
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002") 