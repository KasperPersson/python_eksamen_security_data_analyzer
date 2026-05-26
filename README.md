# Security Data Analyzer

A cybersecurity log analysis tool with AI-powered explanations.  
Analyzes ~6 million network traffic log entries to detect patterns, anomalies, and potential attack behavior.

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/KasperPersson/python_eksamen_security_data_analyzer.git
cd python_eksamen_security_data_analyzer

# 2. Add your API key
cp .env.example .env
# Edit .env and set ANTHROPIC_API_KEY

# 3. Download the dataset (~874 MB, not included in the repo)
# Source: https://www.kaggle.com/datasets/aryan208/cybersecurity-threat-detection-logs
# Download and place the CSV at: data/logs.csv

# 4. Start
docker compose up --build
```

| Service | URL |
|---|---|
| Frontend (Streamlit) | http://localhost:8501 |
| Backend API docs | http://localhost:8000/docs |

```bash
# Stop
docker compose down
```

## Dataset

Download from Kaggle and rename the file to `logs.csv`, then place it at `data/logs.csv`. The `data/` folder already exists in the repo (kept via `.gitkeep`) - just drop the CSV in.

| Field | Description |
|---|---|
| `timestamp` | Time of the log entry |
| `source_ip` / `dest_ip` | Source and destination IP addresses |
| `protocol` | Network protocol (TCP, UDP, HTTP, ...) |
| `action` | Firewall action: `allowed` or `blocked` |
| `threat_label` | Classification: `benign`, `suspicious`, or `malicious` |
| `bytes_transferred` | Bytes transferred in the session |
| `user_agent` | User agent string (curl, Nmap, SQLMap, ...) |
| `request_path` | Requested URI path |

## Environment Variables

| Variable | Set in | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | `.env` | Powers the AI assessment and chat features |
| `DATA_PATH` | `docker-compose.yml` | Path to the CSV inside the backend container (`/app/data/logs.csv`). Locally, the code default `../data/logs.csv` is used automatically - do not add to `.env` |
| `BACKEND_URL` | `docker-compose.yml` | Backend URL seen by the frontend (`http://backend:8000`). Locally defaults to `http://localhost:8000` - do not add to `.env` |

Copy `.env.example` to `.env` and set `ANTHROPIC_API_KEY` - Docker Compose picks it up automatically.

## Features

- **Overview** - row count, time range, threat label breakdown, bytes stats
- **Top IPs** - bar chart of the most active source IPs
- **Attack Distribution** - pie chart of benign vs. suspicious vs. malicious traffic
- **Timeline** - network activity over time, aggregated by hour or day
- **AI Assessment** - one-click security assessment of the full dataset
- **Chat** - ask follow-up questions about the logs in a conversational interface

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| Data processing | Pandas, Numpy |
| Visualization | Matplotlib |
| LLM | Anthropic Claude (`claude-sonnet-4-6`) |
| Containerization | Docker Compose |

## Running Locally (without Docker)

```bash
# Make sure .env is set up with your ANTHROPIC_API_KEY (see Quick Start step 2)

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# Terminal 1 - backend
cd backend
uvicorn main:app --reload

# Terminal 2 - frontend
cd frontend
streamlit run app.py
```

## Tests

```bash
pip install -r backend/requirements.txt
pip install pytest httpx
pytest tests/ -v
```

## Exploratory Data Analysis

See [`notebooks/eda.ipynb`](notebooks/eda.ipynb) for an interactive walkthrough of the dataset using Pandas, Numpy, and Matplotlib.
