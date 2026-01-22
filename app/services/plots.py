from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


class Graphs:
    def __init__(self, csv_path: Path):
        self.csv_path = csv_path
        self._df: pd.DataFrame | None = None

    def load_clean_data(self) -> pd.DataFrame:
        if self._df is not None:
            return self._df

        if not self.csv_path.exists():
            self._df = pd.DataFrame(columns=["amount", "type", "category", "date", "description"])
            return self._df

        df = pd.read_csv(self.csv_path)

        df["amount"] = pd.to_numeric(df.get("amount"), errors="coerce")
        df["date"] = pd.to_datetime(df.get("date"), errors="coerce")
        df["type"] = df.get("type", "").astype(str).str.lower().str.strip()
        df["category"] = df.get("category", "").astype(str).str.lower().str.strip()

        self._df = df.dropna(subset=["amount", "date", "type", "category"])
        return self._df

    def plot_expenses_by_category(self) -> None:
        df = self.load_clean_data()
        exp = df[df["type"] == "expense"]
        if exp.empty:
            print("No expense data to plot.")
            return

        sums = exp.groupby("category")["amount"].sum().sort_values(ascending=False).head(10)
        sums.plot(kind="bar")
        plt.title("Top expenses by category")
        plt.xlabel("Category")
        plt.ylabel("Amount")
        plt.tight_layout()
        plt.show()

    def plot_expense_trend(self) -> None:
        df = self.load_clean_data()
        exp = df[df["type"] == "expense"]
        if exp.empty:
            print("No expense data to plot.")
            return


        exp["date"] = pd.to_datetime(exp["date"])


        monthly = exp.set_index("date")["amount"].resample("ME").sum()


        monthly = monthly.asfreq("ME", fill_value=0)

        # Plot
        monthly.plot(kind="line", marker="o")
        plt.title("Yearly Expense Trend")
        plt.xlabel("Year")
        plt.ylabel("Amount")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()