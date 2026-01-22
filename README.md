# Expense Tracker ML 💸🤖

An end-to-end **expense tracking and analysis system** built with Python.  
The project combines **data storage, analytics, visualization, and machine learning** to help users understand and categorize their expenses intelligently.

---

## 🚀 Features

- Add, list, and delete financial transactions
- Store data using **CSV** and **SQLite database**
- Perform data analysis with **Pandas**
- Generate visual insights using **Matplotlib**
- Automatically **predict expense categories** using Machine Learning
- Provide **basic spending advice** based on user data
- Modular and scalable architecture

---

## 🧠 Machine Learning

- Text-based classification on transaction descriptions
- Model: **Logistic Regression**
- Vectorization: **TF-IDF**
- Automatic prediction of expense categories (e.g., food, transport, gym, work)
- Train / test split with evaluation metrics (accuracy, precision, recall)

---

## 📊 Visualizations

The project generates meaningful charts for financial insights:

- **Bar chart** – Expenses by category
- **Line chart** – Expense trends over time
- (Optional) Pie chart – Expense distribution

Screenshots of the plots can be used as **CV / portfolio assets**.

---

## 🗂️ Project Structure

app/
│
├── ml/ # Machine Learning logic
│ ├── train.py # Train ML model for expense categorization
│ ├── predict_and_advise.py # Predict category + generate spending advice
│
├── models/ # Domain models
│ └── transaction.py # Transaction entity definition
│
├── services/ # Business logic
│ ├── manager.py # Transaction management (CRUD)
│ ├── analysis.py # Data analysis (totals, insights)
│ └── plots.py # Data visualizations (charts)
│
├── storage/ # Data persistence layer
│ ├── csv_store.py # CSV read/write operations
│ └── db_store.py # SQLite database operations
│
├── utils/ # Configuration & helpers
│ └── config.py # Centralized configuration
│
└── main.py # Application entry point
│
data/
├── transactions.csv # CSV data storage
└── transactions.db # SQLite database

---

## 🛠️ Technologies Used

- Python 3
- Pandas
- Matplotlib
- SQLite
- Scikit-learn
- TF-IDF Vectorization
- Logistic Regression

---

## ▶️ How to Run

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies
4. Run the application:

```bash
python app/main.py
##📌 Example Use Cases
Track personal expenses

Analyze spending habits

Visualize financial trends

Automatically classify expenses

Use as a portfolio project for data / ML roles

🎯 Why This Project?
This project demonstrates:

Clean architecture and modular design

Data analysis and visualization skills

Practical machine learning integration

Real-world problem solving

📈 Future Improvements
Improve ML accuracy with more data

Add category auto-fill during transaction input

Export reports (PDF / CSV)

Web or API interface (Flask / FastAPI)
