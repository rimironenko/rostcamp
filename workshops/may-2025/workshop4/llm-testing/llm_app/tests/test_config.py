import os
import pytest
from app.config import OPENAI_API_KEY, MODEL_NAME, DEFAULT_TEMPERATURE, MAX_TOKENS

def test_config_variables():
    """Test that configuration variables are properly set."""
    # Test that required variables are present
    assert OPENAI_API_KEY is not None, "OPENAI_API_KEY should be set"
    
    # Test default values
    assert MODEL_NAME == 'gpt-4o', "Default model should be gpt-4o"
    assert DEFAULT_TEMPERATURE == 0.7, "Default temperature should be 0.7"
    assert MAX_TOKENS == 1000, "Max tokens should be 1000" 