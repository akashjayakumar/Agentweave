from app.rag.ingest import _collection


def retrieve_chunks(
    notebook_id: str,
    query: str,
    k: int = 5,
) -> list[str]:
    """
    Retrieve top-k semantically similar chunks
    for a notebook.
    """
    results = _collection.query(
        query_texts=[query],
        n_results=k,
        where={"notebook_id": notebook_id},
    )

    return results["documents"][0]
