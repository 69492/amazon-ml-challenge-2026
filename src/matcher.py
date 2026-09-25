"""Simple threshold matcher that can serve as a baseline."""

from .features import string_features


def match_value(left_value: object, right_value: object, threshold: float = 0.85) -> bool:
    """Match two normalized values using the stronger of two fuzzy scores."""
    scores = string_features(left_value, right_value)
    return max(scores.values()) >= threshold

