from app.schemas import PromptRequest, LLMResponse
from pydantic import ValidationError
import pytest

def test_prompt_request_valid():
    data = {"prompt": "Hello, world!"}
    req = PromptRequest(**data)
    assert req.prompt == "Hello, world!"

def test_prompt_request_invalid():
    with pytest.raises(ValidationError):
        PromptRequest()

def test_llm_response():
    data = {"response": "Hi there!"}
    resp = LLMResponse(**data)
    assert resp.response == "Hi there!" 