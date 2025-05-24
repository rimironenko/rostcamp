import pytest
from unittest.mock import Mock, patch
from app.llm_client import LLMClient

@pytest.fixture
def mock_openai_response():
    """Mock OpenAI response fixture."""
    mock_response = Mock()
    mock_choice = Mock()
    mock_message = Mock()
    mock_message.content = "Test response"
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    return mock_response

def test_llm_client_initialization():
    """Test that LLMClient initializes correctly."""
    client = LLMClient()
    assert client.model == "gpt-3.5-turbo"
    assert client.temperature == 0.7
    assert client.max_tokens == 1000

@patch('app.llm_client.OpenAI')
def test_get_completion(mock_openai, mock_openai_response):
    """Test that get_completion returns the expected response."""
    # Setup mock
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = mock_openai_response
    mock_openai.return_value = mock_client

    # Test
    client = LLMClient()
    response = client.get_completion("Test prompt")
    
    # Verify
    assert response == "Test response"
    mock_client.chat.completions.create.assert_called_once_with(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Test prompt"}],
        temperature=0.7,
        max_tokens=1000
    )
