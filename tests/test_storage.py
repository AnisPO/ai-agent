import json

import pytest

from storage import ExpenseStorage, StorageError


def test_first_run_creates_empty_storage(tmp_path):
    file_path = tmp_path / "expenses.json"

    storage = ExpenseStorage(file_path)

    assert storage.get_all() == []
    assert not file_path.exists()


def test_add_expense_saves_data_and_restores_it(tmp_path):
    file_path = tmp_path / "expenses.json"

    storage = ExpenseStorage(file_path)
    expense = storage.add_expense(500.0, "Покупки")

    restored_storage = ExpenseStorage(file_path)

    assert expense == {
        "id": 1,
        "amount": 500.0,
        "category": "Покупки",
    }
    assert restored_storage.get_all() == [expense]


def test_add_expenses_uses_sequential_ids(tmp_path):
    file_path = tmp_path / "expenses.json"
    storage = ExpenseStorage(file_path)

    first = storage.add_expense(100.0, "Еда")
    second = storage.add_expense(200.0, "Транспорт")

    assert first["id"] == 1
    assert second["id"] == 2


def test_change_category_is_saved_and_other_records_are_unchanged(tmp_path):
    file_path = tmp_path / "expenses.json"
    storage = ExpenseStorage(file_path)

    storage.add_expense(100.0, "Еда")
    storage.add_expense(200.0, "Транспорт")

    assert storage.change_category(1, "Покупки") is True

    restored_storage = ExpenseStorage(file_path)

    assert restored_storage.get_all() == [
        {"id": 1, "amount": 100.0, "category": "Покупки"},
        {"id": 2, "amount": 200.0, "category": "Транспорт"},
    ]


def test_change_category_returns_false_for_unknown_id(tmp_path):
    storage = ExpenseStorage(tmp_path / "expenses.json")

    assert storage.change_category(999, "Покупки") is False


def test_get_all_returns_copies(tmp_path):
    storage = ExpenseStorage(tmp_path / "expenses.json")
    storage.add_expense(100.0, "Еда")

    expenses = storage.get_all()
    expenses[0]["category"] = "Изменено"

    assert storage.get_all()[0]["category"] == "Еда"


def test_invalid_json_raises_storage_error(tmp_path):
    file_path = tmp_path / "expenses.json"
    file_path.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(StorageError):
        ExpenseStorage(file_path)


def test_invalid_storage_structure_raises_storage_error(tmp_path):
    file_path = tmp_path / "expenses.json"
    file_path.write_text(
        json.dumps({"expenses": "not a list", "next_id": 1}),
        encoding="utf-8",
    )

    with pytest.raises(StorageError):
        ExpenseStorage(file_path)


def test_failed_save_rolls_back_new_expense(tmp_path, monkeypatch):
    storage = ExpenseStorage(tmp_path / "expenses.json")

    def fail_save():
        raise StorageError("Ошибка тестового сохранения")

    monkeypatch.setattr(storage, "_save", fail_save)

    with pytest.raises(StorageError):
        storage.add_expense(100.0, "Еда")

    assert storage.get_all() == []


def test_failed_category_change_rolls_back(tmp_path, monkeypatch):
    storage = ExpenseStorage(tmp_path / "expenses.json")
    storage.add_expense(100.0, "Еда")

    def fail_save():
        raise StorageError("Ошибка тестового сохранения")

    monkeypatch.setattr(storage, "_save", fail_save)

    with pytest.raises(StorageError):
        storage.change_category(1, "Покупки")

    assert storage.get_all() == [{"id": 1, "amount": 100.0, "category": "Еда"}]
