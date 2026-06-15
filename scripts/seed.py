import os
import json
import requests
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import time
import requests

# Initialize Qdrant connection (read host/port from env so containerized runs work)
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
client = QdrantClient(url=f"http://{QDRANT_HOST}:{QDRANT_PORT}")
COLLECTION_NAME = "camera_gear"

def wait_for_qdrant(host: str, port: int, timeout: int = 60) -> None:
    url = f"http://{host}:{port}/"
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                return
        except Exception:
            pass
        time.sleep(1)
    raise RuntimeError(f"Qdrant not reachable at {host}:{port} after {timeout}s")

# Initialize Qdrant Collection with 768 dimensions (matching nomic-embed-text)
wait_for_qdrant(QDRANT_HOST, QDRANT_PORT, timeout=60)
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
)

def get_embedding(text: str) -> list:
    """Generates a semantic vector embedding using local Ollama (configurable via OLLAMA_HOST)."""
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    url = f"{OLLAMA_HOST}/api/embeddings"
    payload = {"model": "nomic-embed-text", "prompt": text}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["embedding"]

def seed_database():
    with open("data/camera_catalog.json", "r") as f:
        products = json.load(f)
    
    points = []
    for product in products:
        # Create a single textual chunk for the AI to understand context
        text_to_embed = f"{product['name']} - {product['specs']} - {product['description']}"
        vector = get_embedding(text_to_embed)
        
        points.append(
            PointStruct(
                id=product["id"],
                vector=vector,
                payload={
                    "name": product["name"],
                    "category": product["category"],
                    "specs": product["specs"],
                    "description": product["description"]
                }
            )
        )
    
    # Batch upload vectors into Qdrant
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"Successfully vectorized and seeded {len(points)} products.")

if __name__ == "__main__":
    seed_database()