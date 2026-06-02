# Security Data Analyzer

A cybersecurity log analysis dashboard with AI explanations.

Built around a dataset of approximately 6 million network traffic log entries.
The application provides visualizations, AI explanations, and a conversational interface for exploring network activity.

**The project was developed and tested with Python 3.13**

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/KasperPersson/python_eksamen_security_data_analyzer.git
cd python_eksamen_security_data_analyzer

# 2. Add your API key
cp .env.example .env

# 3. Download the dataset. See the [Dataset](#dataset) section below.

# 4. Make sure Docker Desktop is running, then:
docker compose up --build
```

| Service | URL |
|---|---|
| Frontend (Streamlit) | http://localhost:8501 |
| Backend API docs | http://localhost:8000/docs |

```bash
# Stop the application
docker compose down
```

## Dataset

The dataset is not included in this repository.

1. Create a free Kaggle account and log in
2. Download the dataset
3. Rename the CSV file to `logs.csv`
4. Place it in `data/logs.csv`

The `data/` folder is kept in the repository using a `.gitkeep` file.

Dataset source:
https://www.kaggle.com/datasets/aryan208/cybersecurity-threat-detection-logs

## Environment Variables

| Variable | Set in | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | `.env` | Required for the AI Assessment and Chat features |
| `DATA_PATH` | `docker-compose.yml` | Path to the CSV inside the backend container (`/app/data/logs.csv`). Locally, the code default `../data/logs.csv` is used automatically - do not add to `.env` |
| `BACKEND_URL` | `docker-compose.yml` | Backend URL seen by the frontend (`http://backend:8000`). Locally defaults to `http://localhost:8000` - do not add to `.env` |

Copy `.env.example` to `.env` and set `ANTHROPIC_API_KEY` - Docker Compose picks it up automatically.
> Note: The dashboard can be used without an Anthropic API key. The API key is only required for the AI Assessment and Chat features.

## Features

- **Overview** - row count, time range, threat label breakdown, bytes stats
- **Top IPs** - bar chart of the most active source IPs
- **Attack Distribution** - pie chart of benign vs. suspicious vs. malicious traffic
- **Timeline** - network activity over time, aggregated by hour or day
- **AI Explain** - one-click security assessment of the full dataset
- **Chat** - ask follow-up questions about the logs in a conversational interface

## Architecture

The application consists of:

- A **Streamlit** frontend
- A **FastAPI** backend
- A **CSV** dataset
- **Claude** for AI assessment and chat features

The frontend communicates with the backend through a REST API.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| Data processing | Pandas, NumPy |
| Visualization | Matplotlib |
| LLM | Anthropic Claude (`claude-sonnet-4-6`) |
| Containerization | Docker Compose |

## Running Locally (without Docker)

```bash
# Make sure .env is set up with your ANTHROPIC_API_KEY (see Quick Start step 2)

# Create and activate virtual environment (Python 3.13 recommended)

python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate

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

## Development / Tests

Install dependencies:

```bash
pip install -r requirements-dev.txt
pre-commit install
```
Run tests:
```bash
pytest tests/ -v
```

Run manually:
```bash
ruff check .
ruff format .
pyright
```

> Note: ruff and pyright run automatically via pre-commit on every commit.