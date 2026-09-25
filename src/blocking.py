"""Candidate-pair generation to reduce the fuzzy matching search space."""

import pandas as pd


def block_pairs(left: pd.DataFrame, right: pd.DataFrame, key: str) -> pd.DataFrame:
    """Create candidate pairs sharing a normalized blocking key."""
    left_view = left.reset_index(names="left_index")[["left_index", key]].drop_duplicates()
    right_view = right.reset_index(names="right_index")[["right_index", key]].drop_duplicates()
    pairs = left_view.merge(right_view, on=key, how="inner")
    return pairs[["left_index", "right_index", key]]

