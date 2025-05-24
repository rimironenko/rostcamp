import pytest
import yaml
import json
from pathlib import Path
from app.llm_client import LLMClient

@pytest.fixture
def llm_client():
    return LLMClient()

@pytest.fixture
def eval_config():
    config_path = Path(__file__).parent.parent / "eval" / "openai_eval_config.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)

@pytest.fixture
def test_cases():
    cases_path = Path(__file__).parent.parent / "eval" / "openai_eval.jsonl"
    cases = []
    with open(cases_path) as f:
        for line in f:
            cases.append(json.loads(line))
    return cases

def test_factual_qa(llm_client, test_cases):
    """Test factual question answering capabilities"""
    factual_cases = [case for case in test_cases if case["category"] == "factual_qa"]
    for case in factual_cases:
        response = llm_client.get_completion(case["input"])
        # Basic assertion that response contains expected answer
        assert case["expected"].lower() in response.lower(), \
            f"Expected '{case['expected']}' in response, got '{response}'"

def test_explanations(llm_client, test_cases):
    """Test explanation capabilities"""
    explanation_cases = [case for case in test_cases if case["category"] == "explanation"]
    for case in explanation_cases:
        response = llm_client.get_completion(case["input"])
        # Check that response is not too short (indicating a proper explanation)
        assert len(response.split()) > 20, \
            f"Response too short for explanation: '{response}'"

def test_creative_writing(llm_client, test_cases):
    """Test creative writing capabilities"""
    creative_cases = [case for case in test_cases if case["category"] == "creative_writing"]
    for case in creative_cases:
        response = llm_client.get_completion(case["input"])
        # Check that response is not too short and contains some creative elements
        assert len(response.split()) > 50, \
            f"Response too short for creative writing: '{response}'"

def test_all_metrics(llm_client, eval_config, test_cases):
    """Test all metrics defined in the config"""
    for case in test_cases:
        response = llm_client.get_completion(case["input"])
        
        # Test accuracy
        if case["category"] == "factual_qa":
            assert case["expected"].lower() in response.lower(), \
                f"Accuracy check failed for '{case['input']}'"
        
        # Test relevance
        assert len(response) > 0, \
            f"Relevance check failed - empty response for '{case['input']}'"
        
        # Test coherence (allow short answers for factual_qa)
        if case["category"] == "factual_qa":
            assert len(response.split()) > 3, \
                f"Coherence check failed - response too short for '{case['input']}'"
        else:
            assert len(response.split()) > 10, \
                f"Coherence check failed - response too short for '{case['input']}'"
        
        # Test helpfulness
        assert not response.startswith("I don't know") and not response.startswith("I cannot"), \
            f"Helpfulness check failed - unhelpful response for '{case['input']}'" 