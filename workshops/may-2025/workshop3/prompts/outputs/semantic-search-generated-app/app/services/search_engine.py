from typing import List, Dict, Any
from app.services.embedder import get_embedding
from app.services.vector_store import search_similar
from app.utils.text_cleaner import clean_text
from app.services.reranker import rerank

def semantic_search(query: str, top_k: int = 3, collection_name: str = "default", rerank_results: bool = False) -> List[Dict[str, Any]]:
    """
    Perform semantic search on the vector store, with optional reranking.
    
    Args:
        query (str): The search query
        top_k (int): Number of results to return
        collection_name (str): Name of the collection to search in
        rerank_results (bool): Whether to rerank results using LLM
        
    Returns:
        List[Dict[str, Any]]: List of similar documents with their metadata and scores
    """
    # Clean the query
    cleaned_query = clean_text(query)
    
    # Search for similar documents
    results = search_similar(
        query=cleaned_query,
        top_k=top_k,
        collection_name=collection_name
    )
    
    if rerank_results:
        results = rerank(cleaned_query, results)
    
    return results 