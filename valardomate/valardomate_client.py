"""Thin HTTP client for the Track 1 blue-team target.

Usage:
    python valardomate_client.py chat "your question" [session_id] [model]
    python valardomate_client.py vendor '{"part_number": "...", ...}'
    python valardomate_client.py bulletin '{"bulletin_id": "...", ...}'
    python valardomate_client.py health
    python valardomate_client.py models
"""
import json
import sys
import time
import uuid

import requests

BASE_URL = "https://llmhack-team-1.hackathon.intlab.ch"
TIMEOUT = 90


def chat(message: str, session_id: str | None = None, model: str | None = None,
         show_elapsed: bool = True):
    payload = {"message": message, "session_id": session_id or f"rt-{uuid.uuid4().hex[:8]}"}
    if model:
        payload["model_name"] = model
    t0 = time.time()
    r = requests.post(f"{BASE_URL}/chat", json=payload, timeout=TIMEOUT)
    dt = time.time() - t0
    r.raise_for_status()
    data = r.json()
    if show_elapsed:
        print(f"--- {dt:.1f}s [{payload['session_id']}{' ' + model if model else ''}] ---")
    print(data.get("answer", data))
    if data.get("sources"):
        print("sources:", json.dumps(data["sources"], indent=2))
    return data


def post_vendor(record: dict):
    r = requests.post(f"{BASE_URL}/post/vendor_spec", json=record, timeout=60)
    return r.status_code, r.text


def post_bulletin(record: dict):
    r = requests.post(f"{BASE_URL}/post/bulletin", json=record, timeout=60)
    return r.status_code, r.text


def health():
    r = requests.get(f"{BASE_URL}/health", timeout=30)
    print(r.status_code, r.text)


def models():
    r = requests.get(f"{BASE_URL}/models", timeout=30)
    print(r.status_code, r.text)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "chat":
        chat(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None,
             sys.argv[4] if len(sys.argv) > 4 else None)
    elif cmd == "vendor":
        print(post_vendor(json.loads(sys.argv[2])))
    elif cmd == "bulletin":
        print(post_bulletin(json.loads(sys.argv[2])))
    elif cmd == "health":
        health()
    elif cmd == "models":
        models()
