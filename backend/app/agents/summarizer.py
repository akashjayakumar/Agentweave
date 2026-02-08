def summarize_changes(changed_chunks: list[str]) -> dict:
    """
    Simple summarization without LLM.
    """

    if not changed_chunks:
        return {
            "tldr": "No significant changes detected.",
            "bullets": [],
            "email_summary": "No significant regulatory updates were detected.",
        }

    bullets = [
        chunk.strip()[:150] + "..."
        for chunk in changed_chunks
    ]

    tldr = f"{len(changed_chunks)} significant regulatory change(s) detected."

    email = (
        "The following regulatory updates were identified:\n\n"
        + "\n".join(f"- {b}" for b in bullets)
    )

    return {
        "tldr": tldr,
        "bullets": bullets,
        "email_summary": email,
    }
