#!/usr/bin/env python3
"""
client.py

Demo client that calls many endpoints from the sample Flask API.

Requirements:
    pip install requests

Usage:
    python client.py
    OR
    BASE_URL=http://localhost:5000 python client.py
"""

import os
import io
import time
import tempfile
import requests

BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")
API_TOKEN = "secret-token-123"  # matches the demo token in the Flask app

def pretty_print_resp(r):
    print(f"\n--- {r.request.method} {r.request.url} -> {r.status_code} ---")
    ct = r.headers.get("Content-Type", "")
    if "application/json" in ct:
        try:
            print(r.json())
        except Exception:
            print(r.text)
    else:
        # for other content-types (csv, text)
        text = r.text
        if len(text) > 500:
            print(text[:500] + "\n...[truncated]")
        else:
            print(text)

def index():
    r = requests.get(f"{BASE_URL}/")
    pretty_print_resp(r)

def health():
    r = requests.get(f"{BASE_URL}/health")
    pretty_print_resp(r)

def list_items(page=1, per_page=10, min_price=None, max_price=None):
    params = {"page": page, "per_page": per_page}
    if min_price is not None:
        params["min_price"] = min_price
    if max_price is not None:
        params["max_price"] = max_price
    r = requests.get(f"{BASE_URL}/items", params=params)
    pretty_print_resp(r)
    return r.json() if r.ok and r.headers.get("Content-Type","").startswith("application/json") else None

def create_item(name, price):
    payload = {"name": name, "price": price}
    r = requests.post(f"{BASE_URL}/items", json=payload)
    pretty_print_resp(r)
    return r.json() if r.ok else None

def get_item(item_id):
    r = requests.get(f"{BASE_URL}/items/{item_id}")
    pretty_print_resp(r)
    return r.json() if r.ok else None

def update_item(item_id, new_data):
    r = requests.put(f"{BASE_URL}/items/{item_id}", json=new_data)
    pretty_print_resp(r)
    return r.json() if r.ok else None

def delete_item(item_id):
    r = requests.delete(f"{BASE_URL}/items/{item_id}")
    pretty_print_resp(r)
    return r.ok

def search(q):
    r = requests.get(f"{BASE_URL}/search", params={"q": q})
    pretty_print_resp(r)
    return r.json() if r.ok else None

def upload_file(field_name="file", file_content=b"hello world\n", filename="demo.txt"):
    # create an in-memory file-like for upload
    files = {field_name: (filename, io.BytesIO(file_content))}
    r = requests.post(f"{BASE_URL}/upload", files=files)
    pretty_print_resp(r)
    return r.json() if r.ok else None

def stream_numbers(timeout_seconds=5):
    """
    Demonstrates reading a streaming endpoint (SSE-style or chunked).
    We use requests.iter_lines to avoid depending on additional libs.
    """
    print(f"\n--- STREAM {BASE_URL}/stream ---")
    try:
        with requests.get(f"{BASE_URL}/stream", stream=True, timeout=timeout_seconds) as r:
            print(f"status: {r.status_code}, content-type: {r.headers.get('Content-Type')}")
            # iterate lines (decode unicode)
            for line in r.iter_lines(decode_unicode=True):
                if line:
                    print("STREAM LINE:", line)
    except requests.exceptions.ReadTimeout:
        print("Stream read timeout (stopping).")

def protected_endpoint():
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    r = requests.get(f"{BASE_URL}/protected", headers=headers)
    pretty_print_resp(r)
    return r.json() if r.ok else None

def download_report(save_path="report.csv"):
    r = requests.get(f"{BASE_URL}/report")
    print(f"\n--- GET {r.request.url} -> {r.status_code} (download) ---")
    if r.ok:
        with open(save_path, "wb") as f:
            f.write(r.content)
        print(f"Saved report to {save_path} ({len(r.content)} bytes)")
    else:
        print("Failed to download report:", r.text)

def demo_sequence():
    print("BASE_URL =", BASE_URL)
    index()
    health()

    # List initial items
    response = list_items()
    time.sleep(0.2)

    # Create a few items
    item_a = create_item("ClientThing A", 3.14)
    item_b = create_item("ClientThing B", 7.77)
    time.sleep(0.2)

    # List again, with filter
    list_items(page=1, per_page=5, min_price=2, max_price=10)
    time.sleep(0.2)

    # Get one item
    if item_a:
        get_item(item_a.get("id"))
        time.sleep(0.2)

    # Update item
    if item_b:
        update_item(item_b.get("id"), {"name": "ClientThing B (updated)", "price": 8.88})
        time.sleep(0.2)

    # Search
    search("ClientThing")
    time.sleep(0.2)

    # Upload a small temporary file
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    try:
        tmp.write(b"This is a temporary file created by the client.\nLine 2.\n")
        tmp.flush()
        tmp.close()
        with open(tmp.name, "rb") as fh:
            files = {"file": (os.path.basename(tmp.name), fh)}
            r = requests.post(f"{BASE_URL}/upload", files=files)
            pretty_print_resp(r)
    finally:
        try:
            os.unlink(tmp.name)
        except Exception:
            pass
    time.sleep(0.2)

    # Stream endpoint - read a few lines
    stream_numbers()

    # Protected endpoint with token
    protected_endpoint()

    # Download csv report
    download_report("report_from_server.csv")

    # Delete created items (cleanup)
    if item_a:
        delete_item(item_a.get("id"))
    if item_b:
        delete_item(item_b.get("id"))

    # Final list
    list_items()

if __name__ == "__main__":
    demo_sequence()
