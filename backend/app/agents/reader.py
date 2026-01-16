from typing import List


def reader_agent(chunks: List[str]) -> List[str]:
    """
    Extract key points from retrieved text chunks.

    Input: raw text chunks from RAG
    Output: list of concise, meaningful points
    """
    points: list[str] = []

    for chunk in chunks:
        sentences = chunk.split(".")
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Simple heuristic for MVP
            if len(sentence) > 20:
                points.append(sentence)

    return points
