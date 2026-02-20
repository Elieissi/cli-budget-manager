from datetime import date, datetime

from sqlalchemy import func, select
from sqlalchemy.exc import OperationalError

from database import Base, SessionLocal, engine
from models import Budget, Transaction, Wallet


def init_db() -> None:
    """Create DB tables and ensure a default wallet and budget exist."""
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as session:
        wallet = session.scalar(select(Wallet).limit(1))
        if wallet is None:
            wallet = Wallet(name="Default Wallet")
            wallet.budget = Budget(limit=0, spent=0)
            session.add(wallet)
            session.commit()


def get_wallet(session) -> Wallet:
    wallet = session.scalar(select(Wallet).limit(1))
    if wallet is None:
        wallet = Wallet(name="Default Wallet")
        wallet.budget = Budget(limit=0, spent=0)
        session.add(wallet)
        session.commit()
        session.refresh(wallet)
    if wallet.budget is None:
        wallet.budget = Budget(limit=0, spent=0)
        session.commit()
        session.refresh(wallet)
    return wallet


def add_transaction(session, wallet: Wallet) -> None:
    while True:
        try:
            amount = float(input("what is the amount of the transaction? ").strip())
            break
        except ValueError:
            print("invalid amount, try again")

    while True:
        t_type = input("is the transaction 'income' or 'expense'? ").strip().lower()
        if t_type in ("income", "expense"):
            break
        print("enter 'income' or 'expense'")

    category = input("what is the category of the transaction? ").strip()

    while True:
        date_input = input("what is the date of this transaction? (YYYY-MM-DD) ").strip()
        try:
            transaction_date = datetime.strptime(date_input, "%Y-%m-%d").date()
            break
        except ValueError:
            print("invalid format. use YYYY-MM-DD")

    transaction = Transaction(
        amount=amount,
        type=t_type,
        category=category,
        transaction_date=transaction_date,
        wallet=wallet,
    )
    session.add(transaction)

    if t_type == "expense":
        wallet.budget.record_expense(amount)

    session.commit()
    print("Transaction saved.")


def view_balance(session, wallet: Wallet) -> None:
    count_stmt = select(func.count(Transaction.id)).where(Transaction.wallet_id == wallet.id)
    transaction_count = session.scalar(count_stmt) or 0
    print(f"Wallet with {transaction_count} transactions. Balance: {wallet.get_balance(session)}")


def view_history(wallet: Wallet) -> None:
    if not wallet.transactions:
        print("No transactions found.")
        return
    for trans in wallet.transactions:
        print(trans)


def search_data(wallet: Wallet, session) -> None:
    stmt = select(Transaction).where(Transaction.wallet_id == wallet.id)

    while True:
        print("1: Filter by date range\t 2: Filter by Type")
        option = input("Select 1 or 2:\n").strip()
        if option in ("1", "2"):
            break
        print("Invalid Selection.")

    if option == "1":
        while True:
            try:
                start = input("Enter start date (YYYY-MM-DD): ").strip()
                end = input("Enter end date (YYYY-MM-DD): ").strip()

                start_date = date.fromisoformat(start)
                end_date = date.fromisoformat(end)

                if start_date > end_date:
                    print("Start date must be before end date.")
                    continue
                break
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD.")

        stmt = stmt.where(Transaction.transaction_date.between(start_date, end_date))

    if option == "2":
        while True:
            print("Filter by 1: Expense\t Filter by 2: Income")
            e_or_i = input("Select 1 or 2:\n").strip()
            if e_or_i in ("1", "2"):
                break
            print("Invalid selection")

        filter_type = "expense" if e_or_i == "1" else "income"
        stmt = stmt.where(Transaction.type == filter_type)

    stmt = stmt.order_by(Transaction.transaction_date)
    filtered = session.scalars(stmt).all()

    if not filtered:
        print("No transactions found.")
        return

    print("\nAmount   Type       Category    Date")
    print("---------------------------------------------")
    for t in filtered:
        amount_str = f"{t.amount:<8}"
        type_str = f"{t.type:<10}"
        category_str = f"{t.category:<12}"
        date_str = t.transaction_date.isoformat()
        print(f"{amount_str}{type_str}{category_str}{date_str}")


def view_budget(wallet: Wallet) -> None:
    print(f"Current budget limit: {wallet.budget.limit}")
    print(f"Current spent amount: {wallet.budget.spent}")
    if wallet.budget.is_exceeded():
        print("Warning: you have exceeded your limit!")


def set_budget(session, wallet: Wallet) -> None:
    while True:
        try:
            new_limit = float(input("Enter new budget limit: "))
            if new_limit < 0:
                print("Budget limit cannot be negative.")
                continue
            wallet.budget.limit = new_limit
            session.commit()
            print("Budget updated.")
            return
        except ValueError:
            print("Invalid amount. Enter a numeric value.")


def clear_transactions(session, wallet: Wallet) -> None:
    confirm = input("Are you sure you want to clear all transactions? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Clear operation cancelled.")
        return

    deleted = session.query(Transaction).filter(Transaction.wallet_id == wallet.id).delete()
    wallet.budget.spent = 0
    session.commit()

    # Clear SQLAlchemy's in-memory relationship cache so next reads come from DB.
    session.expire(wallet, ["transactions", "budget"])
    print(f"Cleared {deleted} transaction(s).")


def show_menu() -> str:
    print("\n=== Personal Finance Tracker ===")
    print("1. Add transaction")
    print("2. View balance")
    print("3. View transaction history")
    print("4. Set budget")
    print("5. View budget status")
    print("6. Search by Type or Date")
    print("7. Clear all transactions")
    print("8. Exit")
    return input("Choose an option: ").strip()


def main() -> None:
    try:
        init_db()
    except OperationalError as error:
        print("Could not connect to PostgreSQL.")
        print(f"Error details: {error.orig}")
        print("For local runs, set DB_HOST=localhost (or your DB server host).")
        print("For Docker Compose runs, use DB_HOST=db and start with: docker compose up --build")
        return

    with SessionLocal() as session:
        while True:
            wallet = get_wallet(session)
            action = show_menu()

            if action == "1":
                add_transaction(session, wallet)
            elif action == "2":
                view_balance(session, wallet)
            elif action == "3":
                view_history(wallet)
            elif action == "4":
                set_budget(session, wallet)
            elif action == "5":
                view_budget(wallet)
            elif action == "6":
                search_data(wallet, session)
            elif action == "7":
                clear_transactions(session, wallet)
            elif action == "8":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number from 1-8.")


if __name__ == "__main__":
    main()
