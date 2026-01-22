from __future__ import annotations

import re
import pandas as pd
from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


def clean_text(s: str) -> str:
    s = str(s).strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s



@dataclass
class ModelBundle:
    model: LogisticRegression
    vectorizer: TfidfVectorizer
    labels: list[str]



def predict_category(
    bundle: ModelBundle,
    description: str,
    confidence_threshold: float = 0.6
) -> tuple[str, float]:
    """
    Predict category + confidence from description
    """
    clean_desc = clean_text(description)
    X = bundle.vectorizer.transform([clean_desc])

    probs = bundle.model.predict_proba(X)[0]
    best_idx = probs.argmax()

    category = bundle.model.classes_[best_idx]
    confidence = probs[best_idx]

    if confidence < confidence_threshold:
        return "other", confidence

    return category, confidence


def expense_by_category(df: pd.DataFrame) -> pd.Series:
    return (
        df[df["type"] == "expense"]
        .groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )


def monthly_expenses(df: pd.DataFrame) -> pd.Series:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    return (
        df[df["type"] == "expense"]
        .set_index("date")
        .resample("ME")["amount"]
        .sum()
    )


def advice_high_category(df: pd.DataFrame) -> list[str]:
    expenses = expense_by_category(df)

    if expenses.empty:
        return []

    total = expenses.sum()
    advices = []

    for cat, amount in expenses.items():
        ratio = amount / total
        if ratio > 0.35:
            advices.append(
                f"You spend {ratio:.0%} of your expenses on '{cat}'. Consider reducing it."
            )

    return advices


def advice_spending_trend(df: pd.DataFrame) -> list[str]:
    monthly = monthly_expenses(df)

    if len(monthly) < 2:
        return []

    if monthly.iloc[-1] > monthly.iloc[-2] * 1.2:
        return [
            "Your expenses increased significantly this month. Review recent payments."
        ]

    return []


def advice_small_frequent(df: pd.DataFrame) -> list[str]:
    small = df[
        (df["type"] == "expense") &
        (df["amount"] < 10)
    ]

    if len(small) >= 10:
        return [
            "Many small expenses detected (coffee/snacks). They add up over time."
        ]

    return []


def generate_advices(df: pd.DataFrame) -> list[str]:
    advices = []
    advices += advice_high_category(df)
    advices += advice_spending_trend(df)
    advices += advice_small_frequent(df)

    if not advices:
        advices.append("Your spending looks well balanced. Keep it up!")

    return advices
