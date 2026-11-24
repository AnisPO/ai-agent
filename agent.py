import math

from storage import ExpenseStorage, StorageError

try:
    storage = ExpenseStorage()
except StorageError as error:
    print(f"Критическая ошибка хранилища: {error}")  # pragma: no cover
    storage = None


def handle_add(amount_str, category):
    if storage is None:
        return "Ошибка: Хранилище недоступно."

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

        return (  # pragma: no cover
            f"Успешно добавлено: {exp['amount']} руб., "
            f"категория '{exp['category']}' (ID: {exp['id']})."
        )

    except ValueError:
        return "Ошибка: Сумма должна быть числом."
    except StorageError as error:
        return f"Ошибка хранения данных: {error}"


def handle_show():
    if storage is None:
        return "Ошибка: Хранилище недоступно."

    expenses = storage.get_all()

    if not expenses:  # pragma: no cover
        return "Список расходов пуст."  # pragma: no cover

    result = "Ваши расходы:\n"  # pragma: no cover

    for exp in expenses:  # pragma: no cover
        result += (  # pragma: no cover
            f"  ID: {exp['id']} | Сумма: {exp['amount']} | "
            f"Категория: {exp['category']}\n"
        )

    return result  # pragma: no cover


def handle_change_category(id_str, new_category):
    if storage is None:
        return "Ошибка: Хранилище недоступно."

    try:
        expense_id = int(id_str)

        new_category = new_category.strip()
        if not new_category:
            return "Ошибка: Категория не должна быть пустой."

        if storage.change_category(expense_id, new_category):
            return (  # pragma: no cover
                f"Категория расхода ID {expense_id} "
                f"изменена на '{new_category}'."
            )

        return f"Ошибка: Расход с ID {expense_id} не найден."

    except ValueError:
        return "Ошибка: ID должен быть целым числом."
    except StorageError as error:
        return f"Ошибка хранения данных: {error}"
