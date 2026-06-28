# Semantic Search — Local Run Instructions

Quick guide to set up and run this project locally.

Prerequisites:
- Python 3.10+ and pip
- Docker & docker-compose (for Qdrant)
- Ollama

Setup:
1. Download the project locally

2. Create and activate a virtual environment from the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Install  relevant Ollama model

```bash
ollama pull nomic-embed-text
```

5. Environment variables
You can export these before running the app, for example:

```bash
export QDRANT_HOST=localhost
export OLLAMA_HOST=http://localhost:11434
```

6. To run the app locally, ensure docker and Ollama are running.
Then, type in the following command:

```bash
docker-compose -f data/docker-compose.yml up -d --build
```

To restart the application, use the following command:
```bash
docker-compose -f data/docker-compose.yml down
docker-compose -f data/docker-compose.yml up -d --build
```

7. The application is now accessible at [localhost:8501](http://localhost:8501/)