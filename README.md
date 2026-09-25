# Amazon ML Challenge 2026

Starter workspace for entity matching and product-record deduplication experiments.

## Layout

- `dataset/train/` and `dataset/test/`: local competition files (ignored by Git)
- `src/`: reusable data, normalization, blocking, matching, and evaluation code
- `notebooks/`: exploratory and modeling workflow
- `experiments/`: saved experiment notes and configurations
- `output/`: generated predictions and reports (ignored by Git)

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

The competition schema is intentionally not assumed. Start with
`notebooks/01_data_exploration.ipynb`, then adapt column names in the later
notebooks and scripts to the supplied files.

