# Utility functions for the semantic search application
import os
import re
from typing import List, Dict, Any
from semantic_search.config import CHUNK_SIZE, CHUNK_OVERLAP

def process_file(filepath: str) -> str:
    """Read and return the content of a text file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return content

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, 
               chunk_overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split text into chunks with overlap."""
    if not text:
        return []
    
    # Clean the text - replace multiple whitespace with single space
    text = re.sub(r'\s+', ' ', text).strip()
    
    # If text is shorter than chunk_size, return it as is
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    # For very large texts, print progress
    total_length = len(text)
    is_large_text = total_length > 100000  # About 100KB
    
    if is_large_text:
        print(f"Processing large text ({total_length} characters)...")
    
    while start < len(text):
        # Get the current chunk
        end = start + chunk_size
        
        # Adjust the end to avoid cutting words in half
        if end < len(text):
            # Find the last period, question mark, or exclamation point before the end
            # This helps create more natural chunk boundaries at sentence ends
            for punctuation in ['. ', '? ', '! ']:
                last_punct = text.rfind(punctuation, start, end)
                if last_punct != -1 and last_punct > start + chunk_size // 2:
                    end = last_punct + 1  # Include the punctuation
                    break
            
            # If no suitable punctuation found, try to find a space
            if end == start + chunk_size:
                # Try to find a space to break at
                while end > start and text[end] != ' ':
                    end -= 1
                
                # If we couldn't find a space, just use the original end
                if end == start:
                    end = start + chunk_size
        else:
            end = len(text)
        
        # Add the chunk to the list
        chunks.append(text[start:end].strip())
        
        # Move the start pointer, considering overlap
        start = end - chunk_overlap
        
        # Handle edge case where overlap is larger than the end of text
        if start < 0:
            break
        
        # Print progress for large texts
        if is_large_text and len(chunks) % 10 == 0:
            progress = min(100, round((end / total_length) * 100))
            print(f"Chunking progress: {progress}% ({len(chunks)} chunks created)")
    
    if is_large_text:
        print(f"Chunking complete. Created {len(chunks)} chunks.")
    
    return chunks

def create_metadata(filepath: str, chunk_id: int, total_chunks: int) -> Dict[str, Any]:
    """Create metadata for a document chunk."""
    filename = os.path.basename(filepath)
    return {
        "source": filepath,
        "filename": filename,
        "chunk_id": chunk_id,
        "total_chunks": total_chunks,
        "file_ext": os.path.splitext(filename)[1]
    }

def format_search_results(results: Dict, query: str) -> str:
    """Format search results for display."""
    if not results or not results['documents'] or len(results['documents'][0]) == 0:
        return f"No results found for query: '{query}'"
    
    output = []
    output.append(f"\nSearch results for: '{query}'")
    output.append("=" * 50)
    
    for i, (doc, metadata, distance) in enumerate(zip(
        results['documents'][0],
        results['metadatas'][0],
        results['distances'][0]
    )):
        similarity_score = 1 - distance  # Convert distance to similarity
        output.append(f"\n[{i+1}] Score: {similarity_score:.4f}")
        output.append(f"Source: {metadata.get('filename', 'Unknown')} (Chunk {metadata.get('chunk_id', 'Unknown')})")
        output.append("-" * 40)
        # Truncate long documents for display
        preview = doc[:300] + "..." if len(doc) > 300 else doc
        output.append(preview)
        output.append("-" * 40)
    
    return "\n".join(output)