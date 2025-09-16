# 💰 Personal Finance Tracker (CLI)

A simple, object-oriented CLI application for tracking personal finances.  
Manage income, expenses, and monthly budgets, with data saved to a JSON file for persistence.

---

## ✨ Features
- **Add transactions** — record income or expenses with amount, category, and date.
- **View balance** — check current balance based on all transactions.
- **Transaction history** — list all past transactions.
- **Set a budget** — define a spending limit and track your spending.
- **Search & filter** — filter transactions by type or date range for insights.
- **Persistent data** — transactions and budget saved to `finance_data.json`.
- **Error handling** — validates file contents and recovers gracefully if corrupted.

---

## 🧠 Design
- **OOP structure** — `Transaction`, `Wallet`, and `Budget` classes encapsulate data and behavior.
- **JSON file I/O** — persisted with `json` and validated with `jsonschema`.
- **CLI interface** — simple menu-driven interface.
- **Dockerized** — lightweight container image with persistent data support using `-v` mounts.

---

## ⚙️ Installation (Local)

1. **Clone the repo:**
    ```bash
    git clone <your-repo-url>
    cd finance-tracker/
    ```
2. **(Optional) Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # on Linux/Mac
    venv\Scripts\activate     # on Windows
    ```
3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
> `requirements.txt` contains:
> ```
> jsonschema
> ```

---

## 🛠 Usage (Local)
Run the CLI:
```bash
python main.py
```

## 🐳 Run with Docker

```
docker build -t finance-tracker .
```
## Run the container with persistent data:

```
docker run -it --rm -v ${PWD}:/app finance-tracker
```

The -v flag mounts your local project folder into the container so finance_data.json persists between runs.
