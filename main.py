from wallet import Wallet
from budget import Budget
from transaction import Transaction
import json
from pathlib import Path
import jsonschema
import datetime

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
    pass

def add_transaction(wallet, budget):
    """
    Prompt user for transaction details.
    Create Transaction object and add it to wallet.
    If expense, update budget as well.
    """
    pass

def view_balance(wallet):
    """
    Print the current balance to user.
    """
    pass

def view_history(wallet):
    """
    Ask user if they want to filter by type/category.
    Print filtered transaction history.
    (hint: this is where t_type/category filters get passed to Wallet)
    """
    pass

def set_budget(budget):
    """
    Prompt user to set a new monthly budget limit.
    Overwrite existing value.
    """
    pass

def show_menu():
    """
    Display options menu to user.
    Return chosen action.
    """
    pass

def main():
    """
    Main CLI loop:
    - Load data
    - Show menu
    - Perform actions until user exits
    - Save data on exit
    """
    pass

if __name__ == "__main__":
    main()