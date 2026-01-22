from __future__ import annotations

from pathlib import Path

# Root of the project (budget_app/)
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

CSV_PATH = DATA_DIR / "transactions.csv"

# app/config.py (BEST place for this)



DB_PATH = PROJECT_ROOT / "data" / "transactions.db"