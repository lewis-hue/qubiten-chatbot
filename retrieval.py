import json, pathlib, re
from sentence_transformers import SentenceTransformer, util

_MODEL = SentenceTransformer("all-MiniLM-L6-v2")   # 22 MB, fast ⏩

def load_kb(path: str):
    """Return list of {"q": str, "a": str}."""
    path = pathlib.Path(path)
    items = []
    with path.open() as f:
        for line in f:
            doc = json.loads(line)
            q = doc["contents"][0]["parts"][0]["text"]
            a = doc["contents"][1]["parts"][0]["text"]
            items.append({"q": q, "a": a})
    return items

def get_answer(question: str, kb):
    """Semantic similarity against stored questions."""
    # pre-compute embeddings once
    if not hasattr(get_answer, "_emb"):
        get_answer._emb = _MODEL.encode([item["q"] for item in kb], normalize_embeddings=True)

    q_emb = _MODEL.encode(question, normalize_embeddings=True)
    scores = util.dot_score(q_emb, get_answer._emb)[0]          # cosine similarity

    best_idx = int(scores.argmax())
    return kb[best_idx]["a"], scores[best_idx].item()
