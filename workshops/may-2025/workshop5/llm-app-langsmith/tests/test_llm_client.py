import pytest
from unittest.mock import Mock, patch
from app.llm_client import LLMClient
from app.config import LANGSMITH_PROJECT

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

@pytest.fixture
def mock_langsmith_client():
    """Mock LangSmith client fixture."""
    return Mock()

def test_llm_client_initialization():
    """Test that LLMClient initializes correctly."""
    client = LLMClient()
    assert client.model == "gpt-4o"
    assert client.temperature == 0.7
    assert client.max_tokens == 1000
    assert client.session_id is not None
    assert client.user_id is None

def test_llm_client_with_session_and_user():
    """Test LLMClient initialization with session and user IDs."""
    session_id = "test-session"
    user_id = "test-user"
    client = LLMClient(session_id=session_id, user_id=user_id)
    assert client.session_id == session_id
    assert client.user_id == user_id

@patch('app.llm_client.OpenAI')
@patch('app.llm_client.Client')
@patch('app.llm_client.ChatOpenAI')
def test_get_completion_with_langsmith(mock_chat_openai, mock_langsmith, mock_openai, mock_openai_response):
    """Test that get_completion works with LangSmith tracing."""
    # Setup mocks
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = mock_openai_response
    mock_openai.return_value = mock_client
    
    mock_langsmith_client = Mock()
    mock_langsmith.return_value = mock_langsmith_client

    mock_chat = Mock()
    mock_chat.invoke.return_value.content = "Test response"
    mock_chat_openai.return_value = mock_chat

    # Test
    client = LLMClient()
    response = client.get_completion("Test prompt")
    
    # Verify
    assert response == "Test response"
    mock_chat.invoke.assert_called_once()
    mock_langsmith.assert_called_once()

@patch('app.llm_client.OpenAI')
@patch('app.llm_client.Client')
@patch('app.llm_client.ChatOpenAI')
def test_get_completion_error_with_fallback(mock_chat_openai, mock_langsmith, mock_openai, mock_openai_response):
    """Test that get_completion falls back to OpenAI on LangSmith error."""
    # Setup mocks
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = mock_openai_response
    mock_openai.return_value = mock_client
    
    mock_langsmith_client = Mock()
    mock_langsmith_client.invoke.side_effect = Exception("LangSmith error")
    mock_langsmith.return_value = mock_langsmith_client

    mock_chat = Mock()
    mock_chat.invoke.side_effect = Exception("LangChain error")
    mock_chat_openai.return_value = mock_chat

    # Test
    client = LLMClient()
    response = client.get_completion("Test prompt")
    
    # Verify fallback to OpenAI
    assert response == "Test response"
    mock_client.chat.completions.create.assert_called_once()

def test_collect_feedback():
    """Test feedback collection functionality."""
    client = LLMClient()
    prompt = "Test prompt"
    response = "Test response"
    rating = 4
    feedback_text = "Good response"
    
    client.collect_feedback(prompt, response, rating, feedback_text)
    
    # Verify feedback was stored
    feedback_summary = client.get_feedback_summary()
    assert feedback_summary["last_rating"] == rating
    assert feedback_summary["last_feedback"] == feedback_text

def test_evaluate_response():
    """Test response evaluation metrics."""
    client = LLMClient()
    prompt = "What is the capital of France?"
    response = "The capital of France is Paris."
    
    metrics = client._evaluate_response(prompt, response)
    
    assert "response_length" in metrics
    assert "prompt_length" in metrics
    assert "response_ratio" in metrics
    assert "has_apology" in metrics
    assert "has_uncertainty" in metrics
    assert "has_repetition" in metrics
    assert "length_appropriate" in metrics
    assert "consistency_score" in metrics
