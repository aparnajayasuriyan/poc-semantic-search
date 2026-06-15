# Semantic Search — Local Run Instructions

Quick guide to set up and run this project locally.

Prerequisites
- Python 3.10+ and pip
- Optional: Docker & docker-compose (for Qdrant)

Setup (recommended)
1. Create and activate a virtual environment from the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

Environment variables
- `QDRANT_HOST` (default: `localhost`)
- `OLLAMA_HOST` (default: `http://localhost:11434`)

You can export these before running the app, for example:

```bash
export QDRANT_HOST=localhost
export OLLAMA_HOST=http://localhost:11434
```

Running the vector DB (Qdrant)
- Quick start with docker-compose (from the repo root):

```bash
docker-compose -f data/docker-compose.yml up -d
```

Note: The provided `docker-compose.yml` brings up `qdrant`. It does not start Ollama; run Ollama locally or point `OLLAMA_HOST` at a reachable embeddings service.

Seeding data
- Ensure `data/camera_catalog.json` exists (it is included in the repo).
- From the project root run:

```bash
python scripts/seed.py
```

This will vectorize the products using the Ollama embeddings endpoint and upload vectors to Qdrant.

Run the API
- Start the FastAPI app with `uvicorn` from the project root:

```bash
uvicorn main.app:app --host 0.0.0.0 --port 8000 --reload
```

API example
- POST a search request to the discover endpoint:

```bash
curl -s -X POST http://localhost:8000/api/v1/discover \
  -H "Content-Type: application/json" \
  -d '{"query":"best mirrorless lens for landscapes","limit":3}'
```

Docker alternative
- The compose file also defines a `backend` service that expects a Docker build context in the project root. To run both services with Docker:

```bash
docker-compose -f data/docker-compose.yml up --build
```

Troubleshooting
- If Qdrant is remote, set `QDRANT_HOST` accordingly (seed and the app read this variable).
- If Ollama is not running on `localhost:11434`, set `OLLAMA_HOST` to the correct URL.
- Run scripts from the repository root so relative paths like `data/camera_catalog.json` resolve correctly.

Files of interest
- `requirements.txt` — Python dependencies
- `scripts/seed.py` — seeds the Qdrant collection from `data/camera_catalog.json`
- `main/app.py` — FastAPI application

If you want, I can also:
- Pin versions in `requirements.txt` (from your env or using conservative constraints)
- Add a minimal `Dockerfile` for the `backend` service
