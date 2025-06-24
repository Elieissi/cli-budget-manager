from transaction import Transaction

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
            new_transaction = Transaction( #create new transaction object
            transaction["amount"], transaction["type"], transaction["category"], transaction["date"]

            )

            self.transactions.append(new_transaction) #add the new transaction
