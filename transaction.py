import json
from datetime import datetime
from pathlib import Path

class Transaction:
    """
    Represents a financial transaction (income or expense).
    Stores amount, type, category/source, and date.
    """
    def __init__(self, amount, t_type, category, date):
        """
        Initialize transaction with amount, type (e.g. 'income' or 'expense'),
        category (e.g. 'food', 'salary'), and date (string).
        """
        pass

    def to_dict(self):
        """
        Return dictionary representation for JSON serialization.
        """
        pass
