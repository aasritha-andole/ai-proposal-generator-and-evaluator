from sentence_transformers import SentenceTransformer

# load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str):
    """
    Convert text into embedding vector
    """
    embedding = model.encode(text)

    return embedding.tolist()