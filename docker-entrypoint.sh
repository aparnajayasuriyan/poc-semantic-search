#!/bin/sh
set -e

# Seed the Qdrant collection before starting the app.
# This runs at container startup.
python scripts/seed.py

exec uvicorn main.app:app --host 0.0.0.0 --port 8000
exec streamlit run app/ui.py --server.port=8501 --server.address=0.0.0.0
