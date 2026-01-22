from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, List

from app.models.transaction import Transaction


FIELDNAMES = ["amount", "type", "category", "date", "description"]


def load_transactions(csv_path: Path) -> List[Transaction]:
    if not csv_path.exists():
        return []

    loaded: List[Transaction] = []
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row:
                continue
            try:
                loaded.append(Transaction.from_dict(row))
            except Exception:
                # skip bad rows silently (could log later)
                continue
    return loaded


def save_transactions(csv_path: Path, transactions: Iterable[Transaction]) -> None:
    """Overwrite CSV (no duplicates)."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for t in transactions:
            writer.writerow(t.to_dict())
