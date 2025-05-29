import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# OpenAI configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-3.5-turbo')

# Application configuration
DEFAULT_TEMPERATURE = 0.7
MAX_TOKENS = 1000
