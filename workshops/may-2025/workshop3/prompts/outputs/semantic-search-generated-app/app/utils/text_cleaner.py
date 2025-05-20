import re
from typing import Optional

def clean_text(text: str, min_length: Optional[int] = None) -> str:
    """
    Clean and normalize text for embedding.
    
    Args:
        text (str): Input text to clean
        min_length (Optional[int]): Minimum length of text to return, None to skip length check
        
    Returns:
        str: Cleaned text
        
    Raises:
        ValueError: If text is empty or shorter than min_length after cleaning
    """
    if not text:
        raise ValueError("Input text cannot be empty")
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^a-z0-9\s.,!?-]', '', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    # Check minimum length if specified
    if min_length is not None and len(text) < min_length:
        raise ValueError(f"Text is too short after cleaning (min length: {min_length})")
    
    return text 