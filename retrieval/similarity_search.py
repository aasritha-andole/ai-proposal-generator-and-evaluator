import sqlite3
import json
from sklearn.metrics.pairwise import cosine_similarity
from retrieval.embedder import get_embedding


DB_PATH = "database/proposals.db"


def find_similar_proposal(idea: str, threshold=0.80):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, idea, embedding FROM proposals")

    rows = cursor.fetchall()

    if not rows:
        conn.close()
        return None

    new_embedding = get_embedding(idea)

    best_score = 0
    best_proposal = None

    for row in rows:

        proposal_id, stored_idea, stored_embedding = row

        if stored_embedding is None:
            continue

        stored_embedding = json.loads(stored_embedding)

        score = cosine_similarity(
            [new_embedding],
            [stored_embedding]
        )[0][0]

        if score > best_score:

            best_score = score
            best_proposal = {
                "proposal_id": proposal_id,
                "idea": stored_idea,
                "score": score
            }

    conn.close()

    if best_score >= threshold:
        return best_proposal

    return None