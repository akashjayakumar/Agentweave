from app.rag.embeddings import embed_texts
from app.rag.ingest import _collection
import numpy as np


SIMILARITY_THRESHOLD = 0.85


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def detect_changes(
    notebook_id: str,
    new_chunks: list[str],
) -> list[str]:
    """
    Returns chunks that are NEW or MEANINGFULLY CHANGED.
    """
    if not new_chunks:
        return []

    # Embed new chunks
    new_embeddings = embed_texts(new_chunks)

    # Get existing chunks for notebook
    existing = _collection.get(
        where={"notebook_id": notebook_id},
        include=["documents", "embeddings"],
    )

    if not existing["documents"]:
        # First ingestion → everything is new
        return new_chunks

    existing_embeddings = existing["embeddings"]

    changed_chunks = []

    for chunk, emb in zip(new_chunks, new_embeddings):
        similarities = [
            cosine_similarity(emb, old_emb)
            for old_emb in existing_embeddings
        ]

        max_similarity = max(similarities)

        if max_similarity < SIMILARITY_THRESHOLD:
            changed_chunks.append(chunk)

    return changed_chunks
