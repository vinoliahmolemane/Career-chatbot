import json
import numpy as np
import cohere


def load_career_data(json_path="careers.json"):
    """Load career options from a local JSON file."""
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_career_matches(user_input, careers, cohere_api_key, min_score=0.3):
    """Embed user input and career data using Cohere, and return similar careers."""
    co = cohere.Client(cohere_api_key)

    # Prepare input text and descriptions
    career_texts = [
        f"{c['title']} - {c['description']} Tags: {', '.join(c['tags'])}" for c in careers
    ]

    # Get embeddings from Cohere
    response = co.embed(
        texts=[user_input] + career_texts,
        model="embed-english-v3.0",
        input_type="search_query"
    )

    user_emb = response.embeddings[0]
    career_embs = response.embeddings[1:]

    def cosine_similarity(a, b):
        a = np.array(a)
        b = np.array(b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    # Compute similarity scores
    scores = [cosine_similarity(user_emb, emb) for emb in career_embs]

    # Pair each career with its score
    ranked = sorted(
        zip(careers, scores),
        key=lambda x: x[1],
        reverse=True
    )

    # Filter by minimum confidence threshold
    filtered = [
        {
            "title": c["title"],
            "description": c["description"],
            "tags": c["tags"],
            "score": round(score, 3)
        }
        for c, score in ranked if score >= min_score
    ]

    return filtered
