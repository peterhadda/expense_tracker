# Budget App (CLI)

Petit projet Python pour gérer des transactions (income/expense), les sauver en CSV + les copier dans SQLite, puis afficher une analyse et des graphes.

## Lancer
```bash
pip install -r requirements.txt
python -m app.main
```

## Fichiers de données
- CSV: `data/transactions.csv`
- SQLite: `data/transactions.db`

## ML (optionnel)
Exemple simple: prédire la `category` depuis `description` (nécessite des données).
```bash
python -m app.ml.train
```
