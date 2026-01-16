from typing import List


def explainer_agent(points: List[str]) -> str:
    """
    Explain extracted points in simple language.
    """
    if not points:
        return "No relevant information found in the notebook."

    explanation = "Here is a simplified explanation:\n\n"

    for idx, point in enumerate(points, start=1):
        explanation += f"{idx}. {point}\n"

    return explanation
