from __future__ import annotations


def prompt_float(label: str) -> float:
    while True:
        raw = input(label).strip().replace(",", ".")
        try:
            return float(raw)
        except ValueError:
            print("Please enter a valid number.")


def prompt_choice(label: str, allowed: set[str]) -> str:
    allowed_lower = {a.lower() for a in allowed}
    while True:
        v = input(label).strip().lower()
        if v in allowed_lower:
            return v
        print(f"Choose one of: {', '.join(sorted(allowed_lower))}")


def prompt_int(label: str) -> int:
    while True:
        raw = input(label).strip()
        try:
            return int(raw)
        except ValueError:
            print("Please enter a valid integer.")
