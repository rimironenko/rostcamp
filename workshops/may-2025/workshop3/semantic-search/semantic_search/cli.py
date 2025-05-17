# Command Line Interface for the semantic search application
import argparse
import sys
import os
import gc
import time
from typing import List, Dict

from semantic_search.search import SemanticSearch
from semantic_search.utils import process_file, chunk_text, create_metadata, format_search_results
from semantic_search.config import DEFAULT_COLLECTION_NAME, DEFAULT_SEARCH_RESULTS
from semantic_search.reranker import ReRanker

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Semantic Search with OpenAI and ChromaDB')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Add documents command
    add_parser = subparsers.add_parser('add', help='Add documents to the vector database')
    add_parser.add_argument('file', help='Text file to process')
    add_parser.add_argument('--collection', default=DEFAULT_COLLECTION_NAME, help='Collection name')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for documents')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--collection', default=DEFAULT_COLLECTION_NAME, help='Collection name')
    search_parser.add_argument('--results', type=int, default=DEFAULT_SEARCH_RESULTS, help='Number of results to return')
    search_parser.add_argument('--rerank', choices=['bm25', 'diversity', 'recency', 'personalized'], 
                              help='Re-ranking method to apply')
    search_parser.add_argument('--diversity', type=float, default=0.5, 
                              help='Diversity factor for diversity re-ranking (0-1)')
    search_parser.add_argument('--recency', type=float, default=0.3, 
                              help='Recency weight for recency re-ranking (0-1)')
    search_parser.add_argument('--profile', help='Path to user profile JSON file for personalized re-ranking')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Get information about collections')
    info_parser.add_argument('--collection', default=DEFAULT_COLLECTION_NAME, help='Collection name')
    
    return parser.parse_args()

def add_document(file_path, collection_name, chunk_size):
    """Process a document in tiny chunks to minimize memory usage."""
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            return 1
        
        file_size = os.path.getsize(file_path)
        print(f"Processing file: {file_path} ({file_size} bytes)")
        print(f"Using chunk size: {chunk_size} characters")
        
        # Initialize counters
        chunks_added = 0
        current_position = 0
        file_base = os.path.basename(file_path)
        
        # Process the file in small chunks
        with open(file_path, 'r', encoding='utf-8') as file:
            while True:
                # Read a small chunk of text
                text_chunk = file.read(chunk_size)
                
                # Exit loop if we've reached the end of the file
                if not text_chunk:
                    break
                
                # Create a unique ID for this chunk
                chunk_id = f"{file_base}_{chunks_added}"
                
                # Process this chunk
                success = add_chunk_to_database(text_chunk, chunk_id, file_path, chunks_added, collection_name)
                
                if success:
                    chunks_added += 1
                
                # Update position
                current_position += len(text_chunk)
                
                # Print progress
                progress = (current_position / file_size) * 100
                print(f"Progress: {progress:.1f}% - Added {chunks_added} chunks so far")
                
                # Force memory cleanup
                text_chunk = None
                gc.collect()
                
                # Small delay to allow memory to be fully released
                time.sleep(0.1)
        
        print(f"\nCompleted processing {file_path}")
        print(f"Added {chunks_added} chunks to collection '{collection_name}'")
        return 0
        
    except Exception as e:
        print(f"Error processing document: {e}")
        return 1

def add_chunk_to_database(text, chunk_id, source_file, chunk_index, collection_name):
    """Add a single text chunk to the database."""
    try:
        # Import here to minimize memory usage
        from semantic_search.search import SemanticSearch
        from semantic_search.utils import create_metadata
        
        # Create metadata
        metadata = create_metadata(source_file, chunk_index, 0)
        
        # Initialize searcher
        searcher = SemanticSearch(collection_name=collection_name)
        
        # Add the single chunk
        searcher.add_documents([text], ids=[chunk_id], metadatas=[metadata])
        
        # Explicitly delete objects to free memory
        del searcher
        
        return True
        
    except Exception as e:
        print(f"Error adding chunk {chunk_id}: {e}")
        return False
    finally:
        # Force garbage collection
        gc.collect()

def apply_reranking(results, query, rerank_method, diversity_factor=0.5, recency_weight=0.3, profile_path=None):
    """Apply the specified re-ranking method to the search results."""
    reranker = ReRanker()
    
    if rerank_method == 'bm25':
        print("Applying BM25 re-ranking...")
        return reranker.bm25_rerank(query, results)
        
    elif rerank_method == 'diversity':
        print(f"Applying diversity re-ranking (factor: {diversity_factor})...")
        return reranker.diversity_rerank(results, diversity_factor)
        
    elif rerank_method == 'recency':
        print(f"Applying recency re-ranking (weight: {recency_weight})...")
        return reranker.recency_rerank(results, recency_weight)
        
    elif rerank_method == 'personalized':
        if not profile_path:
            print("Warning: Personalized re-ranking requires a profile file. Skipping re-ranking.")
            return results
            
        try:
            import json
            with open(profile_path, 'r') as f:
                user_profile = json.load(f)
                
            print(f"Applying personalized re-ranking with profile from {profile_path}...")
            return reranker.personalized_rerank(results, user_profile)
        except Exception as e:
            print(f"Error loading user profile: {e}")
            return results
    
    return results

def search_documents(query: str, collection_name: str, n_results: int, rerank_method=None, 
                     diversity_factor=0.5, recency_weight=0.3, profile_path=None):
    """Search for documents matching the query."""
    try:
        searcher = SemanticSearch(collection_name=collection_name)
        
        # Check if collection has documents
        count = searcher.get_collection_count()
        if count == 0:
            print(f"Collection '{collection_name}' is empty. Add documents before searching.")
            return 1
        
        # Perform search
        results = searcher.search(query, n_results=n_results)
        
        # Apply re-ranking if specified
        if rerank_method:
            results = apply_reranking(
                results, query, rerank_method, 
                diversity_factor, recency_weight, profile_path
            )
        
        # Format and display results
        formatted_results = format_search_results(results, query)
        print(formatted_results)
        
        return 0
        
    except Exception as e:
        print(f"Error searching documents: {e}")
        return 1

def show_info(collection_name: str):
    """Show information about the collection."""
    try:
        searcher = SemanticSearch(collection_name=collection_name)
        count = searcher.get_collection_count()
        
        print(f"\nCollection: {collection_name}")
        print(f"Number of documents: {count}")
        print(f"Storage location: {searcher.db_client.get_settings().persist_directory}")
        
        return 0
        
    except Exception as e:
        print(f"Error getting collection info: {e}")
        return 1

def main():
    """Main entry point for the CLI."""
    args = parse_args()
    
    if args.command == 'add':
        return add_document(args.file, args.collection, 200)
    
    elif args.command == 'search':
        return search_documents(
            args.query, args.collection, args.results, 
            args.rerank, args.diversity, args.recency, args.profile
        )
    
    elif args.command == 'info':
        return show_info(args.collection)
    
    else:
        print("Please specify a command. Use --help for more information.")
        return 1

if __name__ == "__main__":
    sys.exit(main())