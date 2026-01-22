from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pandas as pd

from app.config import CSV_PATH, DB_PATH
from app.models.transaction import Transaction
from app.storage.csv_store import load_transactions, save_transactions
from app.storage.db_store import DataBase


@dataclass
class Totals:
    income: float
    expense: float

    @property
    def net(self) -> float:
        return self.income - self.expense


class TransactionManager:
    def __init__(self):
        self.transactions: List[Transaction] = load_transactions(CSV_PATH)
        self.database = DataBase(DB_PATH)
        self.database.init_db()
        self.database.replace_transactions(self.transactions)

    def add(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)

    def list(self) -> None:
        for i, t in enumerate(self.transactions):
            print(i, t.to_dict())

    def totals(self) -> Totals:
        income = sum(t.amount for t in self.transactions if t.type == "income")
        expense = sum(t.amount for t in self.transactions if t.type == "expense")
        return Totals(income=income, expense=expense)

    def delete(self, index: int) -> bool:
        if 0 <= index < len(self.transactions):
            self.transactions.pop(index)
            return True
        return False

    def save(self) -> None:
        save_transactions(CSV_PATH, self.transactions)
        self.database.replace_transactions(self.transactions)

    def to_dataframe(self) -> pd.DataFrame:
        """Convertit la liste des transactions en DataFrame pour analyse."""
        if not self.transactions:
            return pd.DataFrame(columns=["amount", "type", "category", "description", "date"])

        data = [
            {
                "amount": t.amount,
                "type": t.type,
                "category": t.category,
                "description": t.description,
                "date": t.date,
            }
            for t in self.transactions
        ]
        return pd.DataFrame(data)