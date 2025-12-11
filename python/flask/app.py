# app.py
from flask import Flask, request, jsonify, abort, Response, send_file
from werkzeug.utils import secure_filename
import io
import time

app = Flask(__name__)

# --- Simple in-memory "database" ---
# Each item: { "id": int, "name": str, "price": float }
ITEMS = [
    {"id": 1, "name": "Widget", "price": 9.99},
    {"id": 2, "name": "Gadget", "price": 12.50},
]
NEXT_ID = 3

# --- Simple token-based auth (demo only) ---
API_TOKEN = "secret-token-123"  # DO NOT use in production


def require_token():
    token = request.headers.get("Authorization", "")
    if token.startswith("Bearer "):
        token = token[len("Bearer ") :]
    if token != API_TOKEN:
        abort(401, description="Unauthorized")


# --- Helpers ---
def find_item(item_id):
    return next((it for it in ITEMS if it["id"] == item_id), None)


# --- Routes ---


@app.route("/", methods=["GET"])
def index():
    return jsonify(
        {
            "message": "Welcome to the sample Flask API",
            "endpoints": [
                "GET /health",
                "GET /items",
                "POST /items",
                "GET /items/<id>",
                "PUT /items/<id>",
                "DELETE /items/<id>",
                "GET /search?q=",
                "POST /upload",
                "GET /stream",
                "GET /protected (requires Authorization: Bearer <token>)",
            ],
        }
    )


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "time": time.time()})


# LIST items, with optional pagination & filtering
@app.route("/items", methods=["GET"])
def list_items():
    # simple pagination
    try:
        page = max(int(request.args.get("page", 1)), 1)
        per_page = min(int(request.args.get("per_page", 10)), 100)
    except ValueError:
        abort(400, description="page and per_page must be integers")

    # optional price filter: ?min_price= &max_price=
    try:
        min_price = float(request.args.get("min_price")) if "min_price" in request.args else None
        max_price = float(request.args.get("max_price")) if "max_price" in request.args else None
    except ValueError:
        abort(400, description="price filters must be numbers")

    filtered = ITEMS
    if min_price is not None:
        filtered = [it for it in filtered if it["price"] >= min_price]
    if max_price is not None:
        filtered = [it for it in filtered if it["price"] <= max_price]

    start = (page - 1) * per_page
    end = start + per_page
    return jsonify({"items": filtered[start:end], "page": page, "per_page": per_page, "total": len(filtered)})


# CREATE
@app.route("/items", methods=["POST"])
def create_item():
    global NEXT_ID
    if not request.is_json:
        abort(415, description="Content-Type must be application/json")

    data = request.get_json()
    name = data.get("name")
    price = data.get("price")

    if not name or not isinstance(name, str):
        abort(400, description="name is required and must be a string")
    try:
        price = float(price)
    except (TypeError, ValueError):
        abort(400, description="price is required and must be a number")

    item = {"id": NEXT_ID, "name": name, "price": price}
    NEXT_ID += 1
    ITEMS.append(item)
    return jsonify(item), 201


# READ
@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = find_item(item_id)
    if not item:
        abort(404, description="Item not found")
    return jsonify(item)


# UPDATE
@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    if not request.is_json:
        abort(415, description="Content-Type must be application/json")
    item = find_item(item_id)
    if not item:
        abort(404, description="Item not found")

    data = request.get_json()
    # partial update allowed
    if "name" in data:
        if not isinstance(data["name"], str):
            abort(400, description="name must be a string")
        item["name"] = data["name"]
    if "price" in data:
        try:
            item["price"] = float(data["price"])
        except (TypeError, ValueError):
            abort(400, description="price must be a number")
    return jsonify(item)


# DELETE
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = find_item(item_id)
    if not item:
        abort(404, description="Item not found")
    ITEMS.remove(item)
    return jsonify({"deleted": item_id})


# SEARCH using query param ?q=
@app.route("/search", methods=["GET"])
def search():
    q = request.args.get("q", "").strip().lower()
    if not q:
        return jsonify({"results": []})
    results = [it for it in ITEMS if q in it["name"].lower()]
    return jsonify({"query": q, "results": results})


# FILE UPLOAD (multipart/form-data with field "file")
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        abort(400, description="No file part (field name must be 'file')")
    f = request.files["file"]
    if f.filename == "":
        abort(400, description="No selected file")
    filename = secure_filename(f.filename)
    # For demo, we'll just read into memory and return size (do NOT do this for large files)
    content = f.read()
    size = len(content)
    # Optionally return the uploaded file back for download
    return jsonify({"filename": filename, "size_bytes": size})


# STREAMING endpoint (Server-Sent Events style or chunked)
@app.route("/stream", methods=["GET"])
def stream_numbers():
    def generate():
        for i in range(1, 6):
            yield f"data: number {i}\n\n"
            time.sleep(0.5)

    return Response(generate(), mimetype="text/event-stream")


# PROTECTED endpoint requiring token
@app.route("/protected", methods=["GET"])
def protected():
    require_token()
    return jsonify({"secret": "This is protected data. You provided a valid token."})


# Simple file download example (dynamic content)
@app.route("/report", methods=["GET"])
def report():
    # create a small CSV in memory
    csv = "id,name,price\n" + "\n".join(f'{it["id"]},{it["name"]},{it["price"]}' for it in ITEMS)
    return send_file(io.BytesIO(csv.encode("utf-8")), mimetype="text/csv", as_attachment=True, attachment_filename="report.csv")


# Generic error handler that returns JSON
@app.errorhandler(Exception)
def handle_exception(e):
    code = getattr(e, "code", 500)
    description = getattr(e, "description", str(e))
    return jsonify({"error": description}), code


if __name__ == "__main__":
    # For development only; use a proper WSGI server for production (gunicorn/uvicorn)
    app.run(host="0.0.0.0", port=5000, debug=True)
