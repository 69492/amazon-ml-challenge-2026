"""Submission-file helper."""

from pathlib import Path


def write_submission(frame, path: str | Path, index: bool = False) -> Path:
    """Write predictions as CSV and return the resolved output path."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(destination, index=index)
    return destination

