from flask import Flask, request, jsonify
from retrieval import load_kb, get_answer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)                                       # allow requests from the React dev server

# ---- load knowledge base once on startup ----
KB = load_kb("Tunning.jsonl")                   # list[dict]: {"q": "...", "a": "..."}
print(f"🔍 Loaded {len(KB)} Q-A pairs")

@app.route("/ask", methods=["POST"])
def ask():
    payload = request.get_json(silent=True) or {}
    question = (payload.get("question") or "").strip()

    if not question:
        return jsonify(error="Question cannot be empty."), 400

    answer, score = get_answer(question, KB)

    return jsonify(
        answer=answer,
        confidence=round(float(score), 4)       # might be useful to display later
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
