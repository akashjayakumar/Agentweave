from sentence_transformers import SentenceTransformer

# Small, fast, free, CPU-friendly
_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Convert list of texts into vector embeddings.
    """
    return _model.encode(texts).tolist()
