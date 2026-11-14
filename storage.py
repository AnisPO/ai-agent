import json
from pathlib import Path


class StorageError(Exception):
    """Ошибка чтения или сохранения расходов."""


class ExpenseStorage:
    def __init__(self, file_path=None):
        if file_path is None:
            file_path = Path(__file__).resolve().parent / "data" / "expenses.json"

        self.file_path = Path(file_path)
        self.expenses = []
        self._next_id = 1

        if self.file_path.exists():
            self._load()

    def _load(self):
        try:
            data = json.loads(self.file_path.read_text(encoding="utf-8"))

            if not isinstance(data, dict):
                raise ValueError("Корневой элемент должен быть объектом.")

            expenses = data.get("expenses")
            next_id = data.get("next_id")

            if not isinstance(expenses, list):
                raise ValueError("Поле expenses должно быть списком.")

            for expense in expenses:
                if (
                    not isinstance(expense, dict)
                    or not isinstance(expense.get("id"), int)
                    or isinstance(expense.get("id"), bool)
                    or not isinstance(expense.get("amount"), (int, float))
                    or isinstance(expense.get("amount"), bool)
                    or not isinstance(expense.get("category"), str)
                ):
                    raise ValueError("Некорректная запись расхода.")

            max_id = max((expense["id"] for expense in expenses), default=0)

            if (
                not isinstance(next_id, int)
                or isinstance(next_id, bool)
                or next_id <= max_id
            ):
                raise ValueError("Некорректный следующий ID.")

            self.expenses = expenses
            self._next_id = next_id

        except (OSError, json.JSONDecodeError, ValueError, TypeError) as error:
            raise StorageError(f"Не удалось загрузить расходы: {error}") from error

    def _save(self):
        data = {
            "expenses": self.expenses,
            "next_id": self._next_id,
        }

        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            temp_path = self.file_path.with_name(self.file_path.name + ".tmp")
            temp_path.write_text(
                json.dumps(data, ensure_ascii=False, indent=4),
                encoding="utf-8",
            )
            temp_path.replace(self.file_path)

        except OSError as error:
            raise StorageError(f"Не удалось сохранить расходы: {error}") from error

    def add_expense(self, amount, category):
        expense = {
            "id": self._next_id,
            "amount": amount,
            "category": category,
        }

        self.expenses.append(expense)
        self._next_id += 1

        try:
            self._save()
        except StorageError:
            self.expenses.pop()
            self._next_id -= 1
            raise

        return expense.copy()

    def get_all(self):
        return [expense.copy() for expense in self.expenses]

    def change_category(self, expense_id, new_category):
        for expense in self.expenses:
            if expense["id"] == expense_id:
                old_category = expense["category"]
                expense["category"] = new_category

                try:
                    self._save()
                except StorageError:
                    expense["category"] = old_category
                    raise

                return True

        return False
