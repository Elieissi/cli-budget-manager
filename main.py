from wallet import Wallet
from budget import Budget
from transaction import Transaction
import json
from pathlib import Path

def load_data():
    """
    Load wallet and budget data from JSON file.
    Return a Wallet object and a Budget object.
    Create empty ones if file doesn't exist or is malformed.
    """
    pass

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