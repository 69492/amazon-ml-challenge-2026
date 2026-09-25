"""Small, schema-agnostic helpers for loading competition tables."""

from pathlib import Path
from typing import Iterable

import pandas as pd


def load_table(path: str | Path) -> pd.DataFrame:
    """Load a CSV, Parquet, or JSON table based on its extension."""
    path = Path(path)
    loaders = {".csv": pd.read_csv, ".parquet": pd.read_parquet, ".json": pd.read_json}
    try:
        loader = loaders[path.suffix.lower()]
    except KeyError as exc:
        raise ValueError(f"Unsupported table format: {path.suffix}") from exc
    return loader(path)


def discover_tables(directory: str | Path) -> list[Path]:
    """Return supported table files in a directory, sorted by filename."""
    supported = {".csv", ".parquet", ".json"}
    return sorted(p for p in Path(directory).iterdir() if p.suffix.lower() in supported)


def load_directory(directory: str | Path) -> dict[str, pd.DataFrame]:
    """Load every supported table in a directory keyed by its stem."""
    return {path.stem: load_table(path) for path in discover_tables(directory)}

