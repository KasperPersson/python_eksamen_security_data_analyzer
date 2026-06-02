import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

import numpy as np
import pandas as pd
from anthropic import Anthropic
from anthropic.types import MessageParam, TextBlock
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv(Path(__file__).parent.parent / ".env")

DATA_PATH = os.environ.get("DATA_PATH", "../data/logs.csv")

df: pd.DataFrame | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global df
    df = pd.read_csv(DATA_PATH, parse_dates=["timestamp"])
    yield


app = FastAPI(title="Security Data Analyzer", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# models


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = []


# helpers


def get_df() -> pd.DataFrame:
    if df is None:
        raise RuntimeError("Data not loaded")
    return df


def build_summary() -> str:
    data = get_df()
    total = len(data)
    label_counts = data["threat_label"].value_counts()
    top_ips = data["source_ip"].value_counts().head(10)
    bytes_arr = data["bytes_transferred"].to_numpy()

    lines = [
        f"Total log entries: {total:,}",
        f"Time range: {data['timestamp'].min()} to {data['timestamp'].max()}",
        "",
        "Threat label distribution:",
    ]
    for label, count in label_counts.items():
        pct = count / total * 100
        lines.append(f"  {label}: {count:,} ({pct:.1f}%)")

    lines += [
        "",
        f"Bytes transferred - mean: {np.mean(bytes_arr):,.0f} B, "
        f"min: {np.min(bytes_arr):,} B, max: {np.max(bytes_arr):,} B",
        "",
        "Top source IPs:",
    ]
    for ip, count in top_ips.items():
        lines.append(f"  {ip}: {count:,} requests")

    return "\n".join(lines)


# llm

SYSTEM_PROMPT = (
    "You are an expert cybersecurity analyst examining network security log data. "
    "You have access to a structured summary of a dataset containing millions of "
    "network log entries. The dataset includes fields such as source/destination IPs, "
    "protocol, firewall action (allowed/blocked), threat label "
    "(benign, suspicious, or malicious), "
    "bytes transferred, user agent strings, and request paths.\n\n"
    "Your role is to:\n"
    "- Identify patterns and anomalies in the data\n"
    "- Explain potential attack behaviors and threat indicators\n"
    "- Reference specific IPs, counts, and statistics from the dataset summary\n"
    "- Give security recommendations based on the data\n\n"
    "Use the actual numbers from the data in your answers."
)


# routes


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/analysis/overview")
def overview():
    data = get_df()
    bytes_arr = data["bytes_transferred"].to_numpy()
    return {
        "total_rows": len(data),
        "start_time": str(data["timestamp"].min()),
        "end_time": str(data["timestamp"].max()),
        "label_counts": {
            str(k): int(v) for k, v in data["threat_label"].value_counts().items()
        },
        "bytes_mean": float(np.mean(bytes_arr)),
        "bytes_max": int(np.max(bytes_arr)),
        "bytes_min": int(np.min(bytes_arr)),
    }


@app.get("/analysis/top-ips")
def top_ips(n: int = Query(default=10, ge=1, le=100)):
    data = get_df()
    counts = data["source_ip"].value_counts().head(n)
    return {"items": [{"ip": str(ip), "count": int(c)} for ip, c in counts.items()]}


@app.get("/analysis/attack-distribution")
def attack_distribution():
    data = get_df()
    result = []
    for label, group in data.groupby("threat_label", observed=True)[
        "bytes_transferred"
    ]:
        arr = group.to_numpy()
        result.append(
            {
                "label": str(label),
                "count": int(len(arr)),
                "bytes_mean": float(np.mean(arr)),
                "bytes_total": int(np.sum(arr)),
            }
        )
    return {"items": result}


@app.get("/analysis/timeline")
def timeline(interval: str = Query(default="hour", pattern="^(hour|day)$")):
    data = get_df()
    freq = "h" if interval == "hour" else "D"
    series = data.set_index("timestamp").resample(freq).size()
    return {
        "interval": interval,
        "items": [{"time": str(ts), "count": int(c)} for ts, c in series.items()],
    }


@app.post("/ai/explain")
def explain():
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    summary = build_summary()
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    f"{summary}\n\n"
                    "Analyze this dataset and give a security summary. "
                    "Point out the main threat patterns, flag suspicious IPs, "
                    "and describe the overall security situation."
                ),
            }
        ],
    )
    block = response.content[0]
    if not isinstance(block, TextBlock):
        raise RuntimeError(f"Unexpected response type: {type(block)}")
    return {"text": block.text}


@app.post("/ai/chat")
def chat(req: ChatRequest):
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    summary = build_summary()
    history: list[MessageParam] = [
        {"role": m.role, "content": m.content} for m in req.history
    ]
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=f"{SYSTEM_PROMPT}\n\n{summary}",
        messages=[*history, {"role": "user", "content": req.message}],
    )
    block = response.content[0]
    if not isinstance(block, TextBlock):
        raise RuntimeError(f"Unexpected response type: {type(block)}")
    return {"text": block.text}
