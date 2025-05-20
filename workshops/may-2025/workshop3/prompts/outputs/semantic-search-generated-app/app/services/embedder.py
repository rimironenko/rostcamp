from typing import List
import openai
from app.config import OPENAI_API_KEY, EMBEDDING_MODEL

# Configure OpenAI client
openai.api_key = OPENAI_API_KEY

def get_embedding(text: str) -> List[float]:
    """
    Get embedding vector for the given text using OpenAI's embedding model.
    
    Args:
        text (str): The text to embed
        
    Returns:
        List[float]: The embedding vector
    """
    # Clean and prepare text
    text = text.strip()
    if not text:
        raise ValueError("Text cannot be empty")
    
    # Get embedding from OpenAI
    response = openai.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    
    # Extract embedding vector
    return response.data[0].embedding 