import chromadb
from typing import Dict, Any, List
from app.config import CHROMA_PATH
from app.services.embedder import get_embedding

def get_or_create_collection(name: str = "default"):
    """
    Initialize and return a ChromaDB collection with the given name.
    """
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = client.get_or_create_collection(name=name)
    return collection

def add_document(id: str, content: str, metadata: Dict[str, Any], collection_name: str = "default"):
    """
    Add a document to the vector store with its embedding.
    
    Args:
        id (str): Unique identifier for the document
        content (str): The text content to embed and store
        metadata (Dict[str, Any]): Additional metadata for the document
        collection_name (str): Name of the collection to add to
    """
    # Get or create collection
    collection = get_or_create_collection(collection_name)
    
    # Generate embedding for the content
    embedding = get_embedding(content)
    
    # Add document to collection
    collection.add(
        ids=[id],
        embeddings=[embedding],
        documents=[content],
        metadatas=[metadata]
    )

def search_similar(query: str, top_k: int = 3, collection_name: str = "default") -> List[Dict[str, Any]]:
    """
    Search for similar documents using vector similarity.
    
    Args:
        query (str): The search query
        top_k (int): Number of results to return
        collection_name (str): Name of the collection to search in
        
    Returns:
        List[Dict[str, Any]]: List of similar documents with their metadata and scores
    """
    # Get collection
    collection = get_or_create_collection(collection_name)
    
    # Generate embedding for the query
    query_embedding = get_embedding(query)
    
    # Search for similar documents
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    
    # Format results
    similar_docs = []
    for i in range(len(results["ids"][0])):
        similar_docs.append({
            "id": results["ids"][0][i],
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "score": 1 - results["distances"][0][i]  # Convert distance to similarity score
        })
    
    return similar_docs 