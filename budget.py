class Budget:
    """
    Tracks spending limit and current spent amount.
    """
    def __init__(self, limit):
        """
        Initialize with spending limit and reset spent to 0.
        """
        self.limit = limit
        self.spent = 0

    def record_expense(self, amount):
        """
        Add amount to total spent. Only call for expenses.
        """
        self.spent += amount


    def is_exceeded(self):
        """
        Return True if spent exceeds or equals limit.
        """
        if self.spent >= self.limit:
            return True
        else:
            return False

    def to_dict(self):
        """
        Return dict with limit and spent for JSON saving.
        """
        return {"limit": self.limit, "spent": self.spent}

    def load_from_dict(self, data):
        """
        Load budget values from dict (limit, spent).
        """
        self.limit = data["limit"]
        self.spent = data["spent"]