class Budget:
    """
    Tracks spending limit and current spent amount.
    """
    def __init__(self, limit):
        """
        Initialize with spending limit and reset spent to 0.
        """
        pass

    def record_expense(self, amount):
        """
        Add amount to total spent. Only call for expenses.
        """
        pass

    def is_exceeded(self):
        """
        Return True if spent exceeds or equals limit.
        """
        pass

    def to_dict(self):
        """
        Return dict with limit and spent for JSON saving.
        """
        pass

    def load_from_dict(self, data):
        """
        Load budget values from dict (limit, spent).
        """
        pass