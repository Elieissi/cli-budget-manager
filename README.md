# 💰 Personal Finance Tracker (CLI)

A simple CLI application for tracking personal finances with PostgreSQL persistence.

---

## ✨ Features
- Add transactions (income or expense) with amount, category, and date.
- View balance and transaction history.
- Set and view budget status.
- Search transactions by type or date range.
- Persistent storage using PostgreSQL and SQLAlchemy ORM.

---

## 🧠 Design
- ORM models:
  - `Wallet` has many `Transaction` rows.
  - `Wallet` has one `Budget` row.
- SQLAlchemy manages all database reads/writes.
- Environment variables configure database credentials.

---

## ⚙️ Installation (Local)

1. Clone the repo and move into it.
2. (Optional) Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set database environment variables (example values):

```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=finance_tracker
export DB_USER=finance_user
export DB_PASSWORD=finance_pass
```

5. Run:

```bash
python main.py
```

---

## 🐳 Run with Docker Compose

1. Copy example env file and edit if needed:

```bash
cp .env.example .env
```

2. Build and run app + PostgreSQL:

```bash
docker compose up --build
```

This starts:
- `app`: CLI finance tracker container.
- `db`: PostgreSQL container with persistent volume `postgres_data`.

