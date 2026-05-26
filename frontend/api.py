import os

import requests

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")


def get_overview():
    resp = requests.get(f"{BACKEND_URL}/analysis/overview", timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_top_ips(n=10):
    resp = requests.get(f"{BACKEND_URL}/analysis/top-ips", params={"n": n}, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_attack_distribution():
    resp = requests.get(f"{BACKEND_URL}/analysis/attack-distribution", timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_timeline(interval="hour"):
    resp = requests.get(
        f"{BACKEND_URL}/analysis/timeline", params={"interval": interval}, timeout=30
    )
    resp.raise_for_status()
    return resp.json()


def post_explain():
    resp = requests.post(f"{BACKEND_URL}/ai/explain", timeout=120)
    resp.raise_for_status()
    return resp.json()["text"]


def post_chat(message, history):
    payload = {"message": message, "history": history}
    resp = requests.post(f"{BACKEND_URL}/ai/chat", json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()["text"]
