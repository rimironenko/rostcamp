# Embedding handling module
import openai
from typing import List

from semantic_search.config import OPENAI_API_KEY, EMBEDDING_MODEL

class EmbeddingGenerator:
    """Class to handle embedding generation from OpenAI API."""
    
    def __init__(self, api_key: str = None):
        """Initialize the embedding generator."""
        self.api_key = api_key or OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set it in .env file or pass it directly.")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = EMBEDDING_MODEL
    
    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        response = self.client.embeddings.create(
            input=text,
            model=self.model
        )
        return response.data[0].embedding
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts in batch."""
        response = self.client.embeddings.create(
            input=texts,
            model=self.model
        )
        return [item.embedding for item in response.data]
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embeddings from the current model."""
        # Generate a test embedding to find out the dimension
        test_embedding = self.get_embedding("test")
        return len(test_embedding)