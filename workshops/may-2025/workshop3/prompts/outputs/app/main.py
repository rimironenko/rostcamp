from fastapi import FastAPI, HTTPException
from app.schemas import QueryRequest, SearchResponse, SearchResult
from app.services.search_engine import semantic_search

app = FastAPI()

@app.post("/search", response_model=SearchResponse)
def search(request: QueryRequest, rerank: bool = True):
    try:
        results = semantic_search(request.query, rerank_results=rerank)
        # Convert to SearchResult models
        search_results = [SearchResult(**{k: v for k, v in doc.items() if k in SearchResult.model_fields}) for doc in results]
        return SearchResponse(results=search_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 