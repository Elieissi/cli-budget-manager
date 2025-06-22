#Represents a single transaction, and inits them.
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
        self.amount = amount
        self.type = t_type
        self.category = category
        self.date = date

    def __str__(self):
        return f"{self.amount}, {self.type}, {self.category}, {self.date}"

    def to_dict(self):
        """
        Return dictionary representation for JSON serialization.
        """
        return {"amount": self.amount, "type": self.type, "category": self.category, "date": self.date}
