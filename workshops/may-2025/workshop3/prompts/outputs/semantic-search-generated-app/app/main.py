from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from app.schemas import QueryRequest, SearchResponse, SearchResult
from app.services.search_engine import semantic_search

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Semantic Search API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                h1 { color: #333; }
                .endpoint { background: #f5f5f5; padding: 20px; border-radius: 5px; margin: 20px 0; }
                code { background: #e0e0e0; padding: 2px 5px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <h1>Welcome to Semantic Search API</h1>
            <div class="endpoint">
                <h2>Available Endpoints:</h2>
                <p><code>POST /search</code> - Perform semantic search</p>
                <p><code>GET /docs</code> - API documentation (Swagger UI)</p>
                <p><code>GET /redoc</code> - Alternative API documentation (ReDoc)</p>
            </div>
            <p>Visit <a href="/docs">/docs</a> for interactive API documentation.</p>
        </body>
    </html>
    """

@app.post("/search", response_model=SearchResponse)
def search(request: QueryRequest, rerank: bool = True):
    try:
        results = semantic_search(request.query, rerank_results=rerank)
        # Convert to SearchResult models
        search_results = [SearchResult(**{k: v for k, v in doc.items() if k in SearchResult.model_fields}) for doc in results]
        return SearchResponse(results=search_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 