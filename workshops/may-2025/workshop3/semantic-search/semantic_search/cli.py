# Command Line Interface for the semantic search application
import argparse
import sys
from typing import List

from semantic_search.search import SemanticSearch
from semantic_search.utils import process_file, chunk_text, create_metadata, format_search_results
from semantic_search.config import DEFAULT_COLLECTION_NAME, DEFAULT_SEARCH_RESULTS

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
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Get information about collections')
    info_parser.add_argument('--collection', default=DEFAULT_COLLECTION_NAME, help='Collection name')
    
    return parser.parse_args()

def add_document(file_path: str, collection_name: str):
    """Process a file and add it to the vector database."""
    try:
        print(f"Processing file: {file_path}")
        content = process_file(file_path)
        
        # Split content into chunks
        chunks = chunk_text(content)
        
        if not chunks:
            print("No content found in the file.")
            return 1
        
        print(f"Split document into {len(chunks)} chunks.")
        
        # Create metadata for each chunk
        ids = [f"{file_path}_{i}" for i in range(len(chunks))]
        metadatas = [create_metadata(file_path, i, len(chunks)) for i in range(len(chunks))]
        
        # Add to the database
        searcher = SemanticSearch(collection_name=collection_name)
        searcher.add_documents(chunks, ids=ids, metadatas=metadatas)
        # Note: With PersistentClient, explicit persist is not needed
        
        print(f"Successfully added {len(chunks)} chunks from {file_path} to collection '{collection_name}'")
        print("Database persisted to disk.")
        return 0
        
    except MemoryError:
        print("\nERROR: Not enough memory to process this file.")
        print("Suggestions:")
        print("  1. Reduce the CHUNK_SIZE in semantic_search/config.py")
        print("  2. Close other memory-intensive applications")
        print("  3. Split your document into smaller files")
        return 1
    except Exception as e:
        print(f"Error adding document: {e}")
        return 1

def search_documents(query: str, collection_name: str, n_results: int):
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
        return add_document(args.file, args.collection)
    
    elif args.command == 'search':
        return search_documents(args.query, args.collection, args.results)
    
    elif args.command == 'info':
        return show_info(args.collection)
    
    else:
        print("Please specify a command. Use --help for more information.")
        return 1

if __name__ == "__main__":
    sys.exit(main())