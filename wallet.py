from transaction import Transaction
from datetime import date
#Holds list of transactions and tracks the list of dictionaries
class Wallet:
    """
    Manages list of Transaction objects and calculates net balance.
    """
    def __init__(self):
        """
        Initialize empty transaction list.
        """
        self.transactions = [] #holds all transaction objects

    def add_transaction(self, transaction):
        """
        Add a Transaction object to the list.
        """
        self.transactions.append(transaction)
    
    def __str__(self):
        return f"Wallet with {len(self.transactions)} transactions. Balance: {self.get_balance()}"


    def get_balance(self):
        """
        Return current balance by summing all transactions.
        datastructure:
        wallet.add_transaction(Transaction(100, "income", "salary", "2025-06-01"))
        """
        balance = 0
        for t in self.transactions:
            if t.type == "income":
                balance += t.amount
            
            elif t.type == "expense":
                balance -= t.amount
            
        return balance

    

    def filter_search(self, start_date=None, end_date=None, e_or_i=None):
        """
        Filter transactions by type (income/expense) or date range.
        Prints matching transactions in a clean table format.
        """

        # get all the transactions in a list that can be easily mutable
        filtered = []
        for t in self.transactions:
            filtered.append(t)

        # Run if E_or_i is provided
        if e_or_i is not None:
            type_filtered = [] #declare type filtered list

            #For each transaction in transactions, if the type matches the one we are saerching for, add it to the filtered list
            for t in filtered: 
                if t.type == e_or_i:
                    type_filtered.append(t)
            filtered = type_filtered

        # If we are searching by start and end dates
        if start_date is not None and end_date is not None:
            date_filtered = []

            #For each transaction in transactions, if the date is within our range, add it to the filtered list
            for t in filtered:
                transaction_date = date.fromisoformat(t.date)
                if start_date <= transaction_date <= end_date:
                    date_filtered.append(t)
            filtered = date_filtered

        # If no results found
        if len(filtered) == 0:
            print("No transactions found.")
            return

        # Print results in table format
        print("\nAmount   Type       Category    Date")
        print("---------------------------------------------")
        for t in filtered:
            # Format each column so it lines up and is pretty
            amount_str = f"{t.amount:<8}"
            type_str = f"{t.type:<10}"
            category_str = f"{t.category:<12}"
            date_str = t.date
            print(f"{amount_str}{type_str}{category_str}{date_str}")


    
    def get_history(self):
        """
        Return list of transactions -> Scrapped sorting feature
        """
        for trans in self.transactions:
            print(trans)


    def to_dict(self):
        """
        Convert all transactions into list of dicts for JSON saving.
        """
        data = []
        for trans in self.transactions:
            data.append(trans.to_dict()) 
        
        return data
            


    def load_from_dict(self, data):
        """
        Load transactions from a list of dictionaries.
        """
        for transaction in data:
            #create new transaction object
            new_transaction = Transaction(transaction["amount"], transaction["type"], transaction["category"], transaction["date"])

            self.transactions.append(new_transaction) #add the new transaction
