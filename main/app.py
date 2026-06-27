import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from qdrant_client import QdrantClient

app = FastAPI(title="Semantic Discovery Engine API", version="1.0")

# Read environment configurations
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
COLLECTION_NAME = "camera_gear"

qdrant_client = QdrantClient(host=QDRANT_HOST, port=6333)

class SearchQuery(BaseModel):
    query: str
    limit: int = 3

@app.post("/api/v1/discover")
async def discover_gear(search: SearchQuery):
    """
    Accepts a natural language query, converts it to an embedding, 
    and executes a high-concurrency vector search against Qdrant.
    """
    # 1. Asynchronously fetch embedding from local Ollama model
    async with httpx.AsyncClient() as client:
        try:
            ollama_response = await client.post(
                f"{OLLAMA_HOST}/api/embeddings",
                json={"model": "nomic-embed-text", "prompt": search.query},
                timeout=10.0
            )
            ollama_response.raise_for_status()
            query_vector = ollama_response.json()["embedding"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ollama embedding failure: {str(e)}")

    # 2. Query Qdrant for the closest semantic vector matches
    try:
        query_response = qdrant_client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=search.limit,
            with_payload=True,
            with_vectors=False,
        )
        search_results = query_response.points
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Qdrant database error: {str(e)}")

    # 3. Format and return structured payload response
    results = []
    for hit in search_results:
        results.append({
            "product_id": hit.id,
            "confidence_score": round(hit.score, 4),
            "name": hit.payload.get("name"),
            "category": hit.payload.get("category"),
            "specs": hit.payload.get("specs"),
            "description": hit.payload.get("description"),
            "price": hit.payload.get("price")
        })
        
    return {"query": search.query, "results": results}
