"""Text normalization utilities used before blocking and matching."""

import re
import unicodedata


def normalize_text(value: object) -> str:
    """Normalize a value for robust exact and fuzzy comparisons."""
    if value is None:
        return ""
    text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode()
    text = text.lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def normalize_columns(frame, columns):
    """Return a copy with normalized string columns suffixed by ``_normalized``."""
    result = frame.copy()
    for column in columns:
        result[f"{column}_normalized"] = result[column].map(normalize_text)
    return result

