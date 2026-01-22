from __future__ import annotations

from app.config import CSV_PATH
from app.ml.predict_and_advise import generate_advices
from app.models.transaction import Transaction
from app.services.manager import TransactionManager
from app.services.analysis import Analysis
from app.services.plots import Graphs
from app.utils.input import prompt_choice, prompt_float, prompt_int


def run() -> None:
    manager = TransactionManager()
    analysis_obj = Analysis(CSV_PATH)
    graphs = Graphs(CSV_PATH)

    while True:
        print(
            """
1. Add transaction
2. List transactions
3. Show totals
4. Delete transaction
5. Show analysis (text)
6. Show Expense By Category (bar)
7. Show Expense By Months (line)
8. Expense Advice
9. Save & Exit
"""
        )

        choice = input("Choose: ").strip()

        if choice == "1":
            amount = prompt_float("Amount: ")
            t_type = prompt_choice("Type (income/expense): ", {"income", "expense"})
            category = input("Category: ").strip()
            description = input("Description: ").strip()
            manager.add(Transaction(amount, t_type, category, description))
            print("Added.")

        elif choice == "2":
            manager.list()

        elif choice == "3":
            totals = manager.totals()
            print(f"Income:  {totals.income:.2f}")
            print(f"Expense: {totals.expense:.2f}")
            print(f"Net:     {totals.net:.2f}")

        elif choice == "4":
            idx = prompt_int("Index to delete: ")
            if manager.delete(idx):
                print("Deleted.")
            else:
                print("Invalid index.")

        elif choice == "5":
            analysis_obj.print_analysis()

        elif choice == "6":
            graphs.plot_expenses_by_category()

        elif choice == "7":
            graphs.plot_expense_trend()

        elif choice == "8":
            df = manager.to_dataframe()
            advices = generate_advices(df)
            print("\n--- Spending Advice ---")
            for advice in advices:
                print(advice)


        elif choice == "9":
            manager.save()
            print("Saved. Bye!")
            break


        else:
            print("Invalid choice.")


if __name__ == "__main__":
    run()
