import pytest
from deepeval import assert_test
from deepeval.metrics import HallucinationMetric, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
from app.llm_client import LLMClient

@pytest.fixture
def llm_client():
    return LLMClient()

def test_llm_response_hallucination(llm_client):
    # Test case for hallucination
    test_case = LLMTestCase(
        input="What is the capital of France?",
        actual_output=llm_client.get_completion("What is the capital of France?"),
        expected_output="Paris",
        context=["France is a country in Europe", "Paris is its capital city"]
    )
    
    assert_test(test_case, [HallucinationMetric()])

def test_llm_response_relevancy(llm_client):
    # Test case for answer relevancy
    test_case = LLMTestCase(
        input="Explain quantum computing in simple terms",
        actual_output=llm_client.get_completion("Explain quantum computing in simple terms"),
        expected_output="A simple explanation of quantum computing",
        context=["Quantum computing uses quantum bits or qubits", "It can solve certain problems faster than classical computers"]
    )
    
    assert_test(test_case, [AnswerRelevancyMetric()])

def test_llm_response_combined_metrics(llm_client):
    # Test case using multiple metrics
    test_case = LLMTestCase(
        input="What is machine learning?",
        actual_output=llm_client.get_completion("What is machine learning?"),
        expected_output="An explanation of machine learning",
        context=["Machine learning is a subset of AI", "It involves training models on data to make predictions"]
    )
    
    assert_test(test_case, [
        HallucinationMetric(),
        AnswerRelevancyMetric()
    ]) 