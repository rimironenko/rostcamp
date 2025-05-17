# Semantic Search with Re-ranking

This project implements a semantic search system with advanced re-ranking capabilities, allowing you to:

1. **Index documents** for semantic search using OpenAI embeddings
2. **Search by meaning** rather than just keywords 
3. **Improve relevance** with various re-ranking techniques

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rimironenko/rostcamp.git
cd workshops/may-2025/workshop3/semantic-search 
```

2. Set up a virtual environment:
```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Project Structure

```
semantic-search/
├── .env                    # Environment variables (API keys)
├── .gitignore              # Git ignore file
├── README.md               # Project documentation
├── requirements.txt        # Project dependencies
├── semantic_search/        # Main package
│   ├── __init__.py         # Package initialization
│   ├── cli.py              # Command line interface
│   ├── config.py           # Configuration handling
│   ├── embedding.py        # Embedding generation module
│   ├── search.py           # Main semantic search class
│   └── utils.py            # Utility functions
```

## Usage

### Adding Documents

```bash
# Add a document to the search index
python3 -m semantic_search.cli add document.txt

# You can specify a collection name
python3 -m semantic_search.cli add document.txt --collection custom_collection
```

### Basic Search

```bash
# General query about vector search
python -m semantic_search.cli search "how do vector search engines work"

# More specific technical query
python -m semantic_search.cli search "similarity metrics in vector search"
```

### Re-ranking Techniques

The application supports four re-ranking methods to improve search relevance:

#### 1. BM25 Re-ranking

Combines traditional lexical search with semantic search for a hybrid approach:

```bash
python3 -m semantic_search.cli search "database optimization techniques" --rerank bm25
```

#### 2. Diversity Re-ranking

Increases variety in search results using Maximal Marginal Relevance (MMR):

```bash
python3 -m semantic_search.cli search "machine learning applications" --rerank diversity --diversity 0.7
```
The diversity factor (0-1) controls the balance between relevance and diversity. Higher values increase diversity.

#### 3. Recency Re-ranking

Boosts more recent documents in search results (requires date metadata):

```bash
python3 -m semantic_search.cli search "latest developments" --rerank recency --recency 0.4
```
The recency weight (0-1) controls how much recent documents are favored. Higher values give more weight to recent content.

#### 4. Personalized Re-ranking

Adjusts ranking based on user interests defined in a profile file:

```bash
# First create a user profile JSON file with weighted interests:
# {
#   "machine learning": 0.9,
#   "python": 0.7,
#   "databases": 0.6
# }

python3 -m semantic_search.cli search "optimization techniques" --rerank personalized --profile user_profile.json
```

### Collection Management

View information about your collections:

```bash
python3 -m semantic_search.cli info

# Specify a collection
python3 -m semantic_search.cli info --collection custom_collection
```

## How It Works

### Document Processing

1. Documents are split into manageable chunks
2. Each chunk is converted to a vector embedding using OpenAI's API
3. Embeddings and metadata are stored in ChromaDB for efficient retrieval

### Semantic Search

1. The search query is converted to the same vector space
2. ChromaDB performs similarity search to find the most relevant documents
3. Results are ranked by similarity score

### Re-ranking Methods

1. **BM25**: Combines lexical relevance (term frequencies) with semantic relevance
2. **Diversity**: Uses MMR to select diverse results that maximize information content
3. **Recency**: Applies a time-based boost to more recent documents 
4. **Personalized**: Adjusts scores based on presence of terms from user profile

## Example

```bash
# Add a document
python3 -m semantic_search.cli add sample_document.txt

# Comparing re-ranking methods
# Base query
python3 -m semantic_search.cli search "similarity metrics"

# With different re-ranking
python3 -m semantic_search.cli search "similarity metrics" --rerank bm25
python3 -m semantic_search.cli search "similarity metrics" --rerank diversity --diversity 0.7
python3 -m semantic_search.cli search "similarity metrics" --rerank personalized --profile user_profile.json
```

Even if the exact phrase "impact of climate change on coral reefs" doesn't appear in your documents, the application will find semantically relevant content about climate effects on marine ecosystems.

## Troubleshooting

### Memory Issues

If you encounter a "killed" message or memory errors when processing large files:

1. **Adjust Configuration Parameters**:
   
   Edit `semantic_search/config.py` to reduce memory usage:
   ```python
   # Reduce these values for large files
   CHUNK_SIZE = 300  # Smaller chunks (default is 500)
   CHUNK_OVERLAP = 50  # Less overlap (default is 100)
   MAX_CHUNKS_PER_BATCH = 3  # Process fewer chunks at once (default is 5)
   ```

2. **Process Smaller Files**:
   
   Split large documents into smaller files before processing.

3. **System Resources**:
   
   - Close other memory-intensive applications
   - Ensure you have sufficient free RAM
   - Consider using a machine with more memory for very large documents

The application is designed to gracefully handle memory constraints by processing documents in batches, but very large files may still require configuration adjustments.

### ChromaDB Warnings

If you see a warning message about deprecated ChromaDB configuration:

1. **Update ChromaDB**:
   ```bash
   pip install --upgrade chromadb
   ```

2. **Clear Previous Database**:
   If you're still experiencing issues after updating, you might need to clear your previous database:
   ```bash
   rm -rf ./chroma_db
   ```
   Note: This will delete all your indexed documents, so you'll need to re-add them.

The code has been updated to use the current ChromaDB API, but previous database formats might cause compatibility warnings.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
