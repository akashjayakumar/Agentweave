def analyze_impact(changed_chunks: list[str]) -> dict:
    """
    Rule-based impact analysis.
    Deterministic and explainable.
    """

    impact = {
        "banks": False,
        "nbfcs": False,
        "fintechs": False,
        "customers": False,
        "compliance": False,
    }

    for chunk in changed_chunks:
        text = chunk.lower()

        if "bank" in text:
            impact["banks"] = True
        if "nbfc" in text:
            impact["nbfcs"] = True
        if "fintech" in text or "digital onboarding" in text:
            impact["fintechs"] = True
        if "customer" in text or "kyc" in text:
            impact["customers"] = True
        if "compliance" in text or "reporting" in text:
            impact["compliance"] = True

    return impact

