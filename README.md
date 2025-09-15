# Personal Finance Tracker (CLI)

A simple, object-oriented CLI application for tracking personal finances.  
Manage your income, expenses, and monthly budget, with data saved to a JSON file.

---

## ✨ Features
- **Add transactions** — record income or expenses with amount, category, and date.
- **View balance** — check current balance based on all transactions.
- **Transaction history** — list all past transactions.
- **Set a budget** — define a spending limit and track your spending.
- **Persistent data** — transactions and budget saved to `finance_data.json`.
- **Error handling** — validates file contents and recovers gracefully if corrupted.

---

## 🧠 Design
- **OOP structure** — `Transaction`, `Wallet`, and `Budget` classes encapsulate data and behavior.
- **JSON file I/O** — data persisted with `json` and validated with `jsonschema`.
- **CLI interface** — simple menu-driven interface.

---

## ⚙️ Installation
1. Clone the repo:
    ```bash
    git clone <your-repo-url>
    cd project/
    ```
2. (Optional) Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # on Linux/Mac
    venv\Scripts\activate     # on Windows
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
> **requirements.txt** contains:
> ```
> jsonschema
> ```

---

## 🛠 Usage
Run the CLI:
```bash
python main.py
