import pytest
from app.services.search_engine import semantic_search
from app.services.reranker import rerank

def test_semantic_search():
    # Test basic search functionality
    results = semantic_search("fox", top_k=2)
    assert len(results) > 0
    assert all(isinstance(r, dict) for r in results)
    assert all("id" in r and "content" in r and "score" in r for r in results)

def test_semantic_search_with_reranking():
    # Test search with reranking enabled
    results = semantic_search("fox", top_k=2, rerank_results=True)
    assert len(results) > 0
    assert all(isinstance(r, dict) for r in results)
    assert all("id" in r and "content" in r and "score" in r for r in results)

def test_reranker():
    # Test reranker with sample documents
    docs = [
        {"id": "1", "content": "the quick brown fox", "score": 0.9},
        {"id": "2", "content": "a lazy dog", "score": 0.7},
        {"id": "3", "content": "the fox is quick", "score": 0.8}
    ]
    
    reranked = rerank("fox", docs)
    assert len(reranked) == len(docs)
    assert all(isinstance(r, dict) for r in reranked)
    assert all("id" in r and "content" in r for r in reranked)
    
    # Verify that reranking changed the order
    original_ids = [doc["id"] for doc in docs]
    reranked_ids = [doc["id"] for doc in reranked]
    assert original_ids != reranked_ids  # Order should be different

def test_empty_search():
    # Compare top scores for relevant and unrelated queries
    relevant_results = semantic_search("fox", top_k=2)
    unrelated_results = semantic_search("xyzabc123", top_k=2)
    max_relevant = max(r["score"] for r in relevant_results)
    max_unrelated = max(r["score"] for r in unrelated_results)
    assert max_unrelated < max_relevant

def test_invalid_query():
    # Test search with invalid query
    with pytest.raises(Exception):
        semantic_search("", top_k=2) 