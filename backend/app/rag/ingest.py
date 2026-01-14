import chromadb
from app.rag.embeddings import embed_texts

# Local persistent Chroma store
_client = chromadb.Client(
    chromadb.config.Settings(
        persist_directory="./chroma",
    )
)

_collection = _client.get_or_create_collection(
    name="agentweave_chunks"
)
def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks


def ingest_chunks(
    notebook_id: str,
    chunks: list[str],
):
    """
    Store chunks + embeddings in ChromaDB.
    """
    embeddings = embed_texts(chunks)

    ids = [f"{notebook_id}_{i}" for i in range(len(chunks))]

    metadatas = [
        {"notebook_id": notebook_id}
        for _ in chunks
    ]

    _collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids,
    )
