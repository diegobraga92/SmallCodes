'''
Enunciado

Crie uma API com um endpoint:

POST /analyze-text


Payload:

{ "text": "ola mundo ola" }


Resposta:

{
  "words": 3,
  "unique_words": 2,
  "frequency": {
    "ola": 2,
    "mundo": 1
  }
}
'''


from flask import Flask, request, jsonify, abort
from collections import Counter

app = Flask(__name__)


@app.route("/analyze-text", methods=["POST"])
def analyze_text():
    data = request.get_json()

    if not data or "text" not in data:
        abort(400, "text is required")

    words = data["text"].lower().split()
    counter = Counter(words)

    response = {
        "words": sum(counter.values()),
        "unique_words": len(counter),
        "frequency": dict(counter),
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
