"""Pairwise similarity features for entity matching models."""

from rapidfuzz.fuzz import ratio, token_set_ratio


def string_features(left_value: object, right_value: object) -> dict[str, float]:
    """Return normalized edit and token-set similarity scores in [0, 1]."""
    left = str(left_value or "")
    right = str(right_value or "")
    return {"ratio": ratio(left, right) / 100.0, "token_set_ratio": token_set_ratio(left, right) / 100.0}

