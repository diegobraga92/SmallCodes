from flask import Flask, request, jsonify, g
from datetime import datetime

app = Flask(__name__)

# In-memory storage (for study only)
SAVED_PASS = None


# -------------------------
# 1. Health check endpoint
# -------------------------
@app.route("/health", methods=["GET"])
def hello_world():
    return jsonify(status="ok")


# -------------------------------------
# 2. Save pass endpoint
#    Saves a value sent via header
# -------------------------------------
@app.route("/save-pass", methods=["POST"])
def save_pass():
    global SAVED_PASS

    saved_pass = request.headers.get("X-Pass")
    if not saved_pass:
        return jsonify(error="Missing X-Pass header"), 400

    SAVED_PASS = saved_pass
    g.saved_pass = saved_pass

    return jsonify(message="Pass saved successfully")


# ------------------------------------------------
# 3. Time endpoint
#    Only returns time if pass was previously saved
# ------------------------------------------------
@app.route("/time", methods=["GET"])
def get_time():
    if not SAVED_PASS:
        return jsonify(error="Pass not set"), 403

    return jsonify(time=datetime.utcnow().isoformat())


# ------------------------------------------------
# 4. Add saved pass to ALL response headers
# ------------------------------------------------
@app.after_request
def add_pass_to_headers(response):
    if SAVED_PASS:
        response.headers["X-Saved-Pass"] = SAVED_PASS
    return response


if __name__ == "__main__":
    app.run(debug=True)
