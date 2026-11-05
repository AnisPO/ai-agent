import math

from storage import ExpenseStorage

storage = ExpenseStorage()


def handle_add(amount_str, category):
    try:
        amount = float(amount_str)

        if not math.isfinite(amount):
            return "Ошибка: Сумма должна быть конечным числом."

        if amount <= 0:
            return "Ошибка: Сумма должна быть больше нуля."

        category = category.strip()
        if not category:
            return "Ошибка: Категория не должна быть пустой."

        exp = storage.add_expense(amount, category)

        return (
            f"Успешно добавлено: {exp['amount']} руб., "
            f"категория '{exp['category']}' (ID: {exp['id']})."
        )

    except ValueError:
        return "Ошибка: Сумма должна быть числом."


def handle_show():
    expenses = storage.get_all()

    if not expenses:
        return "Список расходов пуст."

    result = "Ваши расходы:\n"

    for exp in expenses:
        result += (
            f"  ID: {exp['id']} | Сумма: {exp['amount']} | "
            f"Категория: {exp['category']}\n"
        )

    return result


def handle_change_category(id_str, new_category):
    try:
        expense_id = int(id_str)

        new_category = new_category.strip()
        if not new_category:
            return "Ошибка: Категория не должна быть пустой."

        if storage.change_category(expense_id, new_category):
            return (
                f"Категория расхода ID {expense_id} " f"изменена на '{new_category}'."
            )

        return f"Ошибка: Расход с ID {expense_id} не найден."

    except ValueError:
        return "Ошибка: ID должен быть целым числом."
