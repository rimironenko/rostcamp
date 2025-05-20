from pydantic import BaseModel
from typing import List, Any, Dict

class QueryRequest(BaseModel):
    query: str

class SearchResult(BaseModel):
    id: str
    content: str
    score: float
    metadata: Dict[str, Any] = {}

class SearchResponse(BaseModel):
    results: List[SearchResult] 