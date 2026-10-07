# Executive AI Agent — Virtual Data Analyst

An enterprise-grade, multi-agent AI system designed to act as a virtual Chief of Staff for C-level executives. This system answers complex business questions by autonomously orchestrating Text-to-SQL querying (for quantitative metrics) and Retrieval-Augmented Generation (RAG) (for qualitative strategic context), powered by LangGraph and the Groq API.

## Overview

Executives rarely need just a number or just a text extract; they need a synthesis of both. This project solves that by routing queries to specialized sub-agents:

* A **Sales SQL Agent** (`ventes.db`)
* An **HR SQL Agent** (`rh.db`)
* A **Strategic RAG Agent** (`chroma_db` via local HuggingFace embeddings)

The LangGraph supervisor analyzes the user's prompt, executes the necessary tools in parallel or sequentially, and formulates a strictly structured "Executive Summary" directly in a Streamlit dashboard.

## Features

* **Multi-Agent Orchestration**: Utilizes LangGraph to prevent hallucinations, strictly enforcing tool-calling boundaries (e.g., `outil_chiffres_ventes` vs `outil_ressources_humaines`).
* **Ultra-Low Latency LLM**: Powered by LLaMA 3 via the Groq API for near-instant reasoning and generation.
* **Local Privacy for Documents**: Uses HuggingFace `all-MiniLM-L6-v2` embeddings to vectorize sensitive corporate documents locally, keeping strategic data out of external APIs.
* **Automated Evaluation Suite**: Includes a custom golden-dataset tester (`test_agent.py`) that uses Regex to validate exact tool-calling behavior against a markdown test book, ensuring 100% CI/CD-style reliability.
* **Executive Dashboard**: Clean, responsive chat UI built with Streamlit.

## Tech Stack

| Category | Technology | Version | Purpose |
| --- | --- | --- | --- |
| **Language** | Python | 3.10+ | Core development |
| **Orchestration** | LangChain / LangGraph | 0.3.x / 0.2.x | Multi-agent framework and routing |
| **LLM Inference** | Groq API (`ChatOpenAI`) | Cloud | High-speed LLM reasoning |
| **Databases** | SQLite3 | Native | Relational data (Sales & HR) |
| **Vector Store** | ChromaDB | Latest | Local semantic document search |
| **Embeddings** | HuggingFace | `all-MiniLM` | Text vectorization |
| **Frontend** | Streamlit | 1.38+ | Interactive web dashboard |

## Architecture

```text
                             ┌──────────────────────┐
                             │  Executive (User)    │
                             └──────────┬───────────┘
                                        │
                                        ▼
                             ┌──────────────────────┐
                             │ Streamlit Dashboard  │
                             └──────────┬───────────┘
                                        │
                                        ▼
                             ┌──────────────────────┐
                             │ LangGraph Supervisor │
                             └────┬────────────┬────┘
                                  │            │
                 (Quantitative) ──┘            └── (Qualitative)
                 │        │                              │
                 ▼        ▼                              ▼
      ┌────────────┐    ┌────────────┐            ┌────────────┐
      │ SQL Ventes │    │   SQL RH   │            │  RAG Tool  │
      └─────┬──────┘    └─────┬──────┘            └─────┬──────┘
            │                 │                         │
            ▼                 ▼                         ▼
      ┌───────────┐     ┌───────────┐             ┌───────────┐
      │ ventes.db │     │   rh.db   │             │ ChromaDB  │
      └───────────┘     └───────────┘             └───────────┘

```

## Prerequisites

* Python 3.10 or higher
* Git
* Groq API Key (Free tier available at console.groq.com)
* Unix-based OS (Linux/macOS) or Windows Subsystem for Linux (WSL2)

## Installation on a Fresh Machine

Follow these exact steps to run the complete system locally.

1. **Clone the repository:**
```bash
git clone https://github.com/Lokmane-Abdessalam/ai_agent_data_analysis.git
cd ai_agent_data_analysis

```


2. **Set up the Python environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

```


3. **Configure Environment Variables:**
```bash
cp .env.example .env

```

Open `.env` and insert your actual Groq API key:

```env
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
GROQ_MODEL=llama3-70b-8192

```

4. **Initialize the Mock Databases and Vector Store:**
The project requires mock SQLite databases and a populated ChromaDB to run the tests and queries.
```bash
# 1. Generate the SQLite databases (ventes.db and rh.db)
python setup_mock_data.py

# 2. Ingest the text documents into ChromaDB
python ingest.py

```

---

## Running the Project

### Option A: Run via Startup Script (`entry_point.sh`)

Make the script executable and run it:

```bash
chmod +x entry_point.sh
./entry_point.sh

```

Open your browser at `http://localhost:8501`.

### Option B: Test the Backend in Terminal

```bash
python supervisor.py

```

---

## Final Project Tree

```text
ai_agent_data_analysis/
├── README.md
├── requirements.txt
├── .env.example
├── .env                  # Generated manually
├── entry_point.sh        # Startup script
├── setup.py    # Database generator
├── agent.py              # SQL logic for Sales
├── agent_rh.py           # SQL logic for HR
├── rag_tool.py           # ChromaDB search logic
├── ingest.py             # Vector embedding script
├── supervisor.py         # LangGraph Orchestrator
├── app.py                # Streamlit UI
├── test_agent.py         # Test automation script
├── questions_de_test.md  # Golden dataset
├── ventes.db             # Generated
├── rh.db                 # Generated
├── mes_documents/        # Text files for RAG
│   └── rapport_strat.txt
└── chroma_db/            # Generated Vector DB

```

---

## Fresh-Machine Quick Start

```bash
git clone https://github.com/Lokmane-Abdessalam/ai_agent_data_analysis.git
cd ai_agent_data_analysis
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and insert your GROQ_API_KEY
chmod +x entry_point.sh
./entry_point.sh

```