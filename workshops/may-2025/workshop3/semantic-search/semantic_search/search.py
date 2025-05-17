# Main semantic search implementation
import os
from typing import List, Dict, Any

import openai
import chromadb
from chromadb.config import Settings

from semantic_search.config import (
    OPENAI_API_KEY, 
    EMBEDDING_MODEL, 
    CHROMA_PERSIST_DIRECTORY,
    DEFAULT_COLLECTION_NAME,
    SIMILARITY_METRIC
)

class SemanticSearch:
    def __init__(self, openai_api_key: str = None, collection_name: str = DEFAULT_COLLECTION_NAME):
        """Initialize the semantic search with OpenAI and ChromaDB."""
        # Set up OpenAI client
        self.openai_api_key = openai_api_key or OPENAI_API_KEY
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required. Set it in .env file or pass it directly.")
        
        self.client = openai.OpenAI(api_key=self.openai_api_key)
        
        # Set up ChromaDB with current configuration
        chroma_settings = Settings(
            persist_directory=CHROMA_PERSIST_DIRECTORY
        )
        
        self.db_client = chromadb.PersistentClient(
            path=CHROMA_PERSIST_DIRECTORY,
            settings=chroma_settings
        )
        
        # Get or create collection
        self.collection = self.db_client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": SIMILARITY_METRIC}
        )
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embeddings for a text using OpenAI's API."""
        response = self.client.embeddings.create(
            input=text,
            model=EMBEDDING_MODEL
        )
        return response.data[0].embedding
    
    def add_documents(self, documents: List[str], ids: List[str] = None, metadatas: List[Dict[str, Any]] = None):
        """Add documents to the vector database."""
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
        
        # Get max chunks per batch from config
        from semantic_search.config import MAX_CHUNKS_PER_BATCH
        
        # Process in batches to avoid memory issues
        for i in range(0, len(documents), MAX_CHUNKS_PER_BATCH):
            batch_end = min(i + MAX_CHUNKS_PER_BATCH, len(documents))
            batch_docs = documents[i:batch_end]
            batch_ids = ids[i:batch_end]
            batch_metadatas = None if metadatas is None else metadatas[i:batch_end]
            
            print(f"Processing batch {i//MAX_CHUNKS_PER_BATCH + 1}/{(len(documents)-1)//MAX_CHUNKS_PER_BATCH + 1} " 
                  f"(chunks {i+1}-{batch_end} of {len(documents)})...")
            
            try:
                # Get embeddings for the current batch
                batch_embeddings = [self.get_embedding(doc) for doc in batch_docs]
                
                # Add to ChromaDB
                self.collection.add(
                    embeddings=batch_embeddings,
                    documents=batch_docs,
                    ids=batch_ids,
                    metadatas=batch_metadatas
                )
                
                # With PersistentClient, data is automatically persisted
                print(f"Successfully added batch {i//MAX_CHUNKS_PER_BATCH + 1}.")
            except Exception as e:
                print(f"Error processing batch {i//MAX_CHUNKS_PER_BATCH + 1}: {e}")
                # Continue with next batch
        
        print(f"Added {len(documents)} documents to the collection.")

    
    def search(self, query: str, n_results: int = None) -> Dict:
        """Search for similar documents based on the query."""
        from semantic_search.config import DEFAULT_SEARCH_RESULTS
        n_results = n_results or DEFAULT_SEARCH_RESULTS

        query_embedding = self.get_embedding(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        return results
    
    def get_collection_count(self) -> int:
        """Get the number of documents in the collection."""
        return self.collection.count()
    
    def persist(self):
        """Persist the database to disk."""
        # In newer versions of ChromaDB (with PersistentClient), 
        # the data is automatically persisted, so this method is kept
        # for backward compatibility but doesn't need to do anything
        print("Database persisted to disk.")
        # Note: With PersistentClient, ChromaDB automatically persists data
        # after operations, so no explicit persist call is needed