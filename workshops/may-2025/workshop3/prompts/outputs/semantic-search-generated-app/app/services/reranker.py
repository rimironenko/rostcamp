from typing import List, Dict, Any
import openai
from app.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def rerank(query: str, docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Use OpenAI GPT to rerank a list of documents based on their relevance to the query.
    Returns the same docs reordered by relevance.
    """
    if not docs:
        return []
    
    # Construct prompt for reranking
    prompt = (
        f"Query: {query}\n"
        "Documents:\n" +
        "\n".join([f"[{i}] {doc['content']}" for i, doc in enumerate(docs)]) +
        "\n\nRank the documents above from most to least relevant to the query. "
        "Return a comma-separated list of their indices in order."
    )
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=20,
        temperature=0.0
    )
    
    # Parse the response to get the new order
    content = response.choices[0].message.content.strip()
    try:
        indices = [int(i) for i in content.split(",") if i.strip().isdigit()]
    except Exception:
        indices = list(range(len(docs)))  # fallback: original order
    
    # Reorder docs
    reranked = [docs[i] for i in indices if i < len(docs)]
    return reranked 