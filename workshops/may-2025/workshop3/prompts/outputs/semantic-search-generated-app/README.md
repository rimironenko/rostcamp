# Semantic Search Application with Reranking

This project is a semantic search engine that leverages embeddings, vector similarity search, and LLM-based reranking. It provides a FastAPI interface for querying documents and returns the most relevant results, optionally reranked by OpenAI GPT.

## Features
- Document ingestion and cleaning
- Embedding generation and vector storage
- Fast semantic search
- Optional reranking of results using OpenAI GPT
- REST API with FastAPI
- Unit tests for core functionality

## Setup

1. **Clone the repository**

```bash
git clone https://github.com/rimironenko/rostcamp.git
cd workshops/may-2025/workshop3/prompts/outputs/semantic-search-generated-app
```

2. **Create and activate a virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies**

```bash
pip install-e .
```

4. **Set up environment variables**

Create a `.env` file or export the following variables:
- `OPENAI_API_KEY`: Your OpenAI API key

## Document Ingestion

To ingest documents from the `data/raw/` directory:

```bash
python scripts/ingest_docs.py
```

## Running the API

Start the FastAPI server:

```bash
uvicorn app.main:app --reload --port 8000
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive API docs.

## API Usage

### POST `/search`
- **Request Body:**
  ```json
  {
    "query": "your search query"
  }
  ```
- **Query Parameters:**
  - `rerank` (bool, default: true): Whether to rerank results with GPT
- **Response:**
  ```json
  {
    "results": [
      {
        "id": "doc1",
        "content": "...",
        "score": 0.87,
        "metadata": { ... }
      },
      ...
    ]
  }
  ```

## Testing

Run all unit tests with:

```bash
pytest
```

## Project Structure

```
app/
  main.py           # FastAPI app
  schemas.py        # Pydantic schemas
  services/
    search_engine.py
    reranker.py
    embedder.py
    vector_store.py
  utils/
    text_cleaner.py
scripts/
  ingest_docs.py    # Document ingestion script
tests/
  test_search.py    # Unit tests
```

## License
MIT 