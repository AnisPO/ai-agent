class ExpenseStorage:
    def __init__(self):
        self.expenses = []
        self._next_id = 1

    def add_expense(self, amount, category):
        expense = {"id": self._next_id, "amount": amount, "category": category}
        self.expenses.append(expense)
        self._next_id += 1
        return expense

    def get_all(self):
        return self.expenses

    def change_category(self, expense_id, new_category):
        for exp in self.expenses:
            if exp["id"] == expense_id:
                exp["category"] = new_category
                return True
        return False
