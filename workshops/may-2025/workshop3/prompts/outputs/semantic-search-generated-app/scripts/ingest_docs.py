import os
from pathlib import Path
from typing import Dict, Any
import json
from app.utils.text_cleaner import clean_text
from app.services.vector_store import add_document

def load_text_file(file_path: Path) -> str:
    """Load and return the contents of a text file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_metadata(file_path: Path) -> Dict[str, Any]:
    """Extract metadata from file path and name."""
    return {
        "filename": file_path.name,
        "file_type": file_path.suffix[1:],  # Remove the dot
        "source": "raw_files"
    }

def ingest_documents(raw_dir: str = "data/raw", collection_name: str = "default"):
    """
    Ingest all text files from the raw directory into the vector store.
    
    Args:
        raw_dir (str): Path to directory containing raw text files
        collection_name (str): Name of the collection to store documents in
    """
    raw_path = Path(raw_dir)
    if not raw_path.exists():
        raise ValueError(f"Raw directory not found: {raw_dir}")
    
    # Process each text file
    for file_path in raw_path.glob("*.txt"):
        try:
            # Load and clean text
            content = load_text_file(file_path)
            cleaned_content = clean_text(content)
            
            # Extract metadata
            metadata = extract_metadata(file_path)
            
            # Add to vector store
            doc_id = f"doc_{file_path.stem}"
            add_document(
                id=doc_id,
                content=cleaned_content,
                metadata=metadata,
                collection_name=collection_name
            )
            print(f"Successfully ingested: {file_path.name}")
            
        except Exception as e:
            print(f"Error processing {file_path.name}: {str(e)}")

if __name__ == "__main__":
    # Create some test documents if raw directory is empty
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    test_docs = {
        "doc1.txt": "The quick brown fox jumps over the lazy dog.",
        "doc2.txt": "A lazy dog sleeps in the sun.",
        "doc3.txt": "The fox is quick and brown."
    }
    
    # Write test documents
    for filename, content in test_docs.items():
        with open(raw_dir / filename, 'w') as f:
            f.write(content)
    
    # Ingest documents
    ingest_documents() 