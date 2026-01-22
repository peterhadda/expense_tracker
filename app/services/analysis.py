from __future__ import annotations

import pandas as pd
from pathlib import Path


class Analysis:
    def __init__(self, csv_path: Path):
        self.csv_path = csv_path

    def _load_df(self) -> pd.DataFrame:
        if not self.csv_path.exists():
            return pd.DataFrame(columns=["amount", "type", "category", "date", "description"])
        df = pd.read_csv(self.csv_path)
        # basic cleanup
        if "amount" in df.columns:
            df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        if "type" in df.columns:
            df["type"] = df["type"].astype(str).str.lower().str.strip()
        if "category" in df.columns:
            df["category"] = df["category"].astype(str).str.lower().str.strip()
        return df.dropna(subset=["amount", "type", "category"])

    def print_analysis(self) -> None:
        df = self._load_df()

        total_income = df.loc[df["type"] == "income", "amount"].sum()
        total_expense = df.loc[df["type"] == "expense", "amount"].sum()

        print("####################### TOTALS ################################")
        print("Total Income  =", float(total_income))
        print("Total Expense =", float(total_expense))
        print("Net           =", float(total_income - total_expense))
        print("################################################################")

        if df.empty:
            print("\nNo data yet.")
            return

        top5_exp = (
            df[df["type"] == "expense"]
            .groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )

        print("\nTop 5 expense categories:")
        for cat, amt in top5_exp.items():
            print(f"- {cat}: {amt:.2f}")
