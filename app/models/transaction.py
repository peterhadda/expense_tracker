from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass(frozen=True)
class Transaction:
    amount: float
    type: str  # "income" or "expense"
    category: str
    description: str
    date: datetime | None = None

    def __post_init__(self):
        # dataclass frozen => object.__setattr__
        object.__setattr__(self, "amount", float(self.amount))
        object.__setattr__(self, "type", str(self.type).strip().lower())
        object.__setattr__(self, "category", str(self.category).strip().lower())
        object.__setattr__(self, "description", str(self.description).strip())
        object.__setattr__(self, "date", self.date or datetime.now())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "amount": self.amount,
            "type": self.type,
            "category": self.category,
            "date": self.date.isoformat(),
            "description": self.description,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Transaction":
        # tolerant parsing
        date_raw = d.get("date")
        parsed_date = None
        if date_raw:
            try:
                parsed_date = datetime.fromisoformat(str(date_raw))
            except Exception:
                parsed_date = None
        return Transaction(
            amount=float(d.get("amount", 0)),
            type=str(d.get("type", "")),
            category=str(d.get("category", "")),
            description=str(d.get("description", "")),
            date=parsed_date,
        )
