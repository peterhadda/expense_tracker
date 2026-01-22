from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable

import pandas as pd

from app.models.transaction import Transaction


class DataBase:
    def __init__(self, db_file: Path | str):
        self.db_file = str(db_file)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        Path(self.db_file).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT,
                    amount REAL,
                    category TEXT,
                    date TEXT,
                    description TEXT
                )
                """
            )
            conn.commit()

    def replace_transactions(self, transactions: Iterable[Transaction]) -> None:
        """Simple strategy for now: wipe + reinsert (keeps code easy)."""
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM transactions;")
            cur.executemany(
                """
                INSERT INTO transactions (type, amount, category, date, description)
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    (t.type, t.amount, t.category, t.date.isoformat(), t.description)
                    for t in transactions
                ],
            )
            conn.commit()

    def load_to_pandas(self, query: str = "SELECT * FROM transactions") -> pd.DataFrame:
        with self._connect() as conn:
            return pd.read_sql_query(query, conn)
