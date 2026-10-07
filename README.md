# Executive AI Agent — Virtual Data Analyst

## Overview

The **Executive AI Agent** is an advanced, production-ready virtual data analyst designed specifically for company leadership (C-Level, Directors, and Managers). It bridges the gap between structured business metrics and unstructured qualitative strategy by combining **Text-to-SQL data extraction** with **Retrieval-Augmented Generation (RAG)**.

When leadership asks complex business questions—such as *"What was our total revenue in France, and what qualitative factors impacted those results this quarter?"*—the system orchestrates multiple specialized tools under a single intelligent supervisor to deliver a structured "Executive Summary" combining exact figures and contextual narrative.

### High-Level Architecture

1. **Supervisor Agent (LangGraph)**: Evaluates the executive prompt, determines which tools are needed, handles multi-step reasoning, and synthesizes the final response.
2. **SQL Tool (LCEL + SQLite)**: Translates natural language into secure, executable SQLite queries to fetch exact quantitative KPIs (sales, revenue, volumes).
3. **RAG Tool (ChromaDB + HuggingFace Embeddings)**: Performs semantic search across internal strategic documents (`.txt` / PDF) to retrieve qualitative context and justifications.
4. **Interface (Streamlit)**: Provides a clean, conversational chat interface tailored for executive reporting.

---

## Features

* **Multi-Agent Orchestration**: Powered by LangGraph's reactive agent loop (`create_agent`), enabling sequential tool usage (SQL first, then RAG, or vice versa).
* **Ultra-Fast LLM Inference**: Powered by the Groq API (`ChatOpenAI` connector) for near-instantaneous response times.
* **Local Privacy & Embeddings**: Uses local HuggingFace open-source embeddings (`sentence-transformers`) for vectorizing internal documents without sending sensitive data to external embedding APIs.
* **Executive-Ready Formatting**: Enforces strict system prompts for pyramid-structured reporting, clear separation of quantitative data vs. qualitative analysis, and elimination of technical jargon.

---

## Tech Stack

| Category | Technology | Version | Purpose |
| --- | --- | --- | --- |
| **Language** | Python | 3.10+ (tested on 3.14) | Core programming language |
| **Orchestration** | LangChain / LangGraph | Latest (v1.x) | Agent loops, prompts, and LCEL chains |
| **LLM Inference** | Groq API (`ChatOpenAI`) | Cloud API | Low-latency LLM execution |
| **Vector Database** | ChromaDB (`langchain-chroma`) | Latest | Local storage for document embeddings |
| **Embeddings** | HuggingFace (`sentence-transformers`) | `all-MiniLM-L6-v2` | Local text vectorization |
| **Structured Database** | SQLite (`langchain_community.utilities`) | 3.x | Relational storage for business sales data |
| **Web Interface** | Streamlit | Latest | Executive chat dashboard |
| **Configuration** | python-dotenv | Latest | Secure environment variable management |
| **Package Manager** | `uv` / `pip` | Latest | Dependency management and virtual environments |

---

## Architecture Diagram

```text
               ┌──────────────────────┐
               │    Executive (User)  │
               └──────────┬───────────┘
                          │
                          ▼
               ┌──────────────────────┐
               │  Streamlit Dashboard │
               └──────────┬───────────┘
                          │
                          ▼
               ┌──────────────────────┐
               │ LangGraph Supervisor │
               └────┬────────────┬────┘
                    │            │
         (Quantitative)          (Qualitative)
                    │            │
                    ▼            ▼
             ┌────────────┐    ┌────────────┐
             │  SQL Tool  │    │  RAG Tool  │
             └─────┬──────┘    └─────┬──────┘
                   │                 │
                   ▼                 ▼
             ┌───────────┐     ┌───────────┐
             │ SQLite DB │     │ ChromaDB  │
             │ (ventes)  │     │ (vectors) │
             └───────────┘     └───────────┘

```

---

## Project Structure

```text
ai_agent_data_analysis/
├── README.md
├── requirements.txt
├── .env.example
├── entry_point.sh
├── agent.py
├── rag_tool.py
├── ingest.py
├── supervisor.py
├── app.py
├── ventes.db
├── rapport_strat.txt
└── chroma_db/

```

* `agent.py`: LCEL pipeline translating natural language into SQL and querying `ventes.db`.
* `rag_tool.py`: LangChain tool exposing ChromaDB semantic search over documents.
* `ingest.py`: Ingestion script that parses, chunks, and embeds text reports into ChromaDB.
* `supervisor.py`: LangGraph orchestrator integrating tools and the system prompt.
* `app.py`: Streamlit web chat application.
* `ventes.db`: SQLite database containing sales data.
* `rapport_strat.txt`: Strategic company document used by the RAG pipeline.

---

## Prerequisites

Ensure your fresh machine has the following installed:

* **Operating System**: Linux, macOS, or Windows (WSL2 recommended)
* **Python**: Version 3.10 or higher
* **Git**: For cloning repositories
* **Groq API Key**: Obtainable for free from [Groq Console](https://console.groq.com/)

---

## Installation on a Fresh Machine

Follow these sequential steps to set up and run the project from scratch.

### 1. Clone the Repository

```bash
git clone https://github.com/Lokmane-Abdessalam/ai_agent_data_analysis.git
cd ai_agent_data_analysis

```

### 2. Set Up Python Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

```

### 3. Install Dependencies

Using `uv` (recommended for speed) or standard `pip`:

```bash
pip install -r requirements.txt

```

*(Or via `uv pip install -r requirements.txt` if `uv` is installed).*

### 4. Configure Environment Variables

Create your local `.env` file from the template:

```bash
cp .env.example .env

```

Open `.env` and insert your actual Groq API key:

```env
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
GROQ_MODEL=llama3-70b-8192

```

### 5. Initialize the RAG Vector Database

Run the ingestion script to parse `rapport_strat.txt` and populate ChromaDB:

```bash
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

FILE: .env.example

```env
# Groq API Configuration
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b

```
---

## Final Project Tree

```text
virtual-data-analyst/
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