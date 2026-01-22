from __future__ import annotations

from dataclasses import dataclass
import re
import pandas as pd

from app.storage.db_store import DataBase
from app.config import DB_PATH

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn import metrics



db = DataBase(DB_PATH)


def clean_text(s: str) -> str:
    s = str(s).strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s


def clean_category(s: str) -> str:
    s = str(s).strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s



def load_training_data() -> pd.DataFrame:
    query = """
    SELECT category, description
    FROM transactions
    WHERE category IS NOT NULL AND TRIM(category) != ''
      AND description IS NOT NULL AND TRIM(description) != ''
    """
    df = db.load_to_pandas(query)

    if df.empty:
        return df

    df["category"] = df["category"].map(clean_category)
    df["description"] = df["description"].map(clean_text)

    # Supprimer catégories trop rares
    counts = df["category"].value_counts()
    df = df[df["category"].isin(counts[counts >= 2].index)]

    return df



def safe_train_test_split(X, y, test_ratio=0.2, random_state=42):
    n_samples = len(y)
    n_classes = len(set(y))

    if n_samples < n_classes * 2:
        raise ValueError("Pas assez de données pour entraîner un modèle fiable")

    min_test_size = n_classes
    desired_test_size = int(n_samples * test_ratio)
    test_size = max(min_test_size, desired_test_size)

    if n_samples - test_size < n_classes:
        test_size = n_samples - n_classes

    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )



@dataclass
class ModelBundle:
    model: LogisticRegression
    vectorizer: TfidfVectorizer
    labels: list[str]



def train_model(texts: list[str], labels: list[str]) -> ModelBundle:
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        max_features=5000,
        ngram_range=(1, 2),
    )

    X = vectorizer.fit_transform(texts)

    X_train, X_test, y_train, y_test = safe_train_test_split(X, labels)

    model = LogisticRegression(
        solver="lbfgs",
        max_iter=2000
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("\n===== METRICS =====")
    print("Accuracy :", metrics.accuracy_score(y_test, y_pred))
    print("Precision:", metrics.precision_score(y_test, y_pred, average="weighted", zero_division=0))
    print("Recall   :", metrics.recall_score(y_test, y_pred, average="weighted", zero_division=0))
    print("F1       :", metrics.f1_score(y_test, y_pred, average="weighted", zero_division=0))
    print("\nClassification report:")
    print(metrics.classification_report(y_test, y_pred, zero_division=0))

    return ModelBundle(
        model=model,
        vectorizer=vectorizer,
        labels=sorted(set(labels))
    )



def predict_categories(bundle: ModelBundle, texts: list[str]) -> list[str]:
    texts = [clean_text(t) for t in texts]
    X = bundle.vectorizer.transform(texts)
    return bundle.model.predict(X).tolist()





