from wallet import Wallet
from budget import Budget
from transaction import Transaction
import json
from pathlib import Path
import jsonschema
from datetime import datetime


def load_data():
    """
    Load wallet and budget data from JSON file.
    Return a Wallet object and a Budget object.
    Create empty ones if file doesn't exist or is malformed.
    
    """
    finance_schema = {
        "type": "object",
        "properties": {
            "transactions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string"},
                        "amount": {"type": "number"},
                        "category": {"type": "string"},
                        "date": {"type": "string"}
                    },
                    "required": ["type", "amount", "category", "date"]
                }
            },
            "budget": {
                "type": "object",
                "properties": {
                    "limit": {"type": "number"},
                    "spent": {"type": "number"}
                },
                "required": ["limit", "spent"]
            }
        },
        "required": ["transactions", "budget"]
    }

    if Path("finance_data.json").exists(): 
            try:
                with open("finance_data.json", "r") as file:
                    contents = json.load(file)
                    jsonschema.validate(instance=contents, schema=finance_schema)
                

            except (json.JSONDecodeError, jsonschema.ValidationError):  # malformed case
                with open("finance_data.json", "w") as file:
                    json.dump({"transactions": [], "budget": {"limit": 0, "spent": 0}}, file, indent=4)
                    contents = {"transactions": [], "budget": {"limit": 0, "spent": 0}}

    else:  # if path doesn't exist
        with open("finance_data.json", "w") as file:
            json.dump({"transactions": [], "budget": {"limit": 0, "spent": 0}}, file, indent=4)
            contents = {"transactions": [], "budget": {"limit": 0, "spent": 0}}
            
    wallet = Wallet()
    wallet.load_from_dict(contents["transactions"])

    budget = Budget()
    budget.load_from_dict(contents["budget"])

    return wallet, budget

def save_data(wallet, budget):
    """
    Save current wallet and budget state to JSON file.
    """
    with open("finance_data.json", "w") as file:
        json.dump( {"transactions": wallet.to_dict(), "budget": {"limit": budget.limit, "spent": budget.spent}}, file, indent=4 )


def add_transaction(wallet, budget):
    """
    prompt user for transaction details.
    create transaction and add it to wallet.
    if expense, update budget as well.
    """

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
        date_input = input(
            "what is the date of this transaction? (YYYY-MM-DD) "
        ).strip()
        try:
            date = str(datetime.strptime(date_input, "%Y-%m-%d").date())
            break
        except ValueError:
            print("invalid format. use YYYY-MM-DD")

    #init
    transaction = Transaction(amount, t_type, category, date)

    # add to wallet
    wallet.add_transaction(transaction)

    # update budget if expense
    if t_type == "expense":
        budget.record_expense(amount)

        
def view_balance(wallet):
    """
    Print the current balance to user.
    """
    print(wallet)

def view_history(wallet):
    """
    Print transaction history
    """
    wallet.get_history()


def show_menu():
    """
    Display options menu to user.
    Return chosen action.
    """
    print("\n=== Personal Finance Tracker ===")
    print("1. Add transaction")
    print("2. View balance")
    print("3. View transaction history")
    print("4. Set budget")
    print("5. View budget status")
    print("6. Exit")
    choice = input("Choose an option: ").strip()
    return choice

def view_budget(budget):
    print(f"Current budget limit: {budget.limit}")
    print(f"Current spent amount: {budget.spent}")
    if budget.is_exceeded():
        print("Warning: you have exceeded your limit!")

def main():
    """
    Main CLI loop:
    - Load data
    - Show menu
    - Perform actions until user exits
    - Save data on exit
    """
    wallet, budget = load_data()

    while True:
        action = show_menu()

        if action == "1":
            add_transaction(wallet, budget)
        elif action == "2":
            view_balance(wallet)
        elif action == "3":
            view_history(wallet)
        elif action == "4":
            new_limit = float(input("Enter new budget limit: "))
            budget.limit = new_limit
        elif action == "5":
            view_budget(budget)
        elif action == "6":
            save_data(wallet, budget)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1-5.")
    
if __name__ == "__main__":
    main()