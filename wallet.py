from transaction import Transaction

class Wallet:
    """
    Manages list of Transaction objects and calculates net balance.
    """
    def __init__(self):
        """
        Initialize empty transaction list.
        """
        pass

    def add_transaction(self, transaction):
        """
        Add a Transaction object to the list.
        """
        pass

    def get_balance(self):
        """
        Return current balance by summing all transactions.
        """
        pass

    def get_history(self, t_type, category):
        """
        Return list of transactions filtered by type and/or category.
        t_type and category may be used optionally.
        (hint: consider letting them default to None later)
        """
        pass

    def to_dict(self):
        """
        Convert all transactions into list of dicts for JSON saving.
        """
        pass

    def load_from_dict(self, data):
        """
        Load transactions from a list of dictionaries.
        """
        pass