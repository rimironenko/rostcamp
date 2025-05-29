import os
import pytest
from app.config import (
    OPENAI_API_KEY,
    LANGSMITH_API_KEY,
    MODEL_NAME,
    DEFAULT_TEMPERATURE,
    MAX_TOKENS
)

def test_required_environment_variables():
    """Test that required environment variables are set."""
    assert OPENAI_API_KEY is not None
    assert LANGSMITH_API_KEY is not None

def test_optional_environment_variables():
    """Test that optional environment variables have default values."""
    assert MODEL_NAME == "gpt-4o"
    assert DEFAULT_TEMPERATURE == 0.7
    assert MAX_TOKENS == 1000 