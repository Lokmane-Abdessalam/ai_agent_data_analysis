#!/usr/bin/env bash
set -euo pipefail

echo "=============================================="
echo " Starting Executive AI Agent Environment..."
echo "=============================================="

# 1. Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "[-] Virtual environment not found. Creating .venv..."
    python3 -m venv .venv
fi

# 2. Activate virtual environment
echo "[+] Activating virtual environment..."
source .venv/bin/activate

# 3. Check for .env file
if [ ! -f ".env" ]; then
    echo "[!] Warning: .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "[!] Please update your .env file with a valid GROQ_API_KEY before executing queries."
    exit 1
fi

# 4. Check if ChromaDB exists, if not run ingestion
if [ ! -d "chroma_db" ]; then
    echo "[+] ChromaDB vector store not found. Running ingestion..."
    python ingest.py
fi

# 5. Launch Streamlit UI
echo "[+] Launching Streamlit Executive Dashboard..."
streamlit run app.py

