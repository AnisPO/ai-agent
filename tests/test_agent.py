import agent
from storage import ExpenseStorage


def setup_storage(tmp_path, monkeypatch):
    storage = ExpenseStorage(tmp_path / "expenses.json")
    monkeypatch.setattr(agent, "storage", storage)
    return storage


def test_handle_add_success(tmp_path, monkeypatch):
    storage = setup_storage(tmp_path, monkeypatch)

    result = agent.handle_add("500", " Покупки ")

    assert "Успешно добавлено" in result
    assert storage.get_all()[0]["category"] == "Покупки"


def test_handle_add_invalid_amount(tmp_path, monkeypatch):
    setup_storage(tmp_path, monkeypatch)

    assert agent.handle_add("abc", "Еда") == "Ошибка: Сумма должна быть числом."


def test_handle_add_non_finite_amount(tmp_path, monkeypatch):
    setup_storage(tmp_path, monkeypatch)

    assert "конечным числом" in agent.handle_add("nan", "Еда")
    assert "конечным числом" in agent.handle_add("inf", "Еда")


def test_handle_add_non_positive_amount(tmp_path, monkeypatch):
    setup_storage(tmp_path, monkeypatch)

    assert "больше нуля" in agent.handle_add("0", "Еда")
    assert "больше нуля" in agent.handle_add("-10", "Еда")


def test_handle_add_empty_category(tmp_path, monkeypatch):
    setup_storage(tmp_path, monkeypatch)

    assert "не должна быть пустой" in agent.handle_add("100", "   ")


def test_handle_show_empty_storage(tmp_path, monkeypatch):
    setup_storage(tmp_path, monkeypatch)

    assert agent.handle_show() == "Список расходов пуст."


def test_handle_show_expenses(tmp_path, monkeypatch):
    storage = setup_storage(tmp_path, monkeypatch)
    storage.add_expense(100, "Еда")

    result = agent.handle_show()

    assert "Еда" in result
    assert "100" in result


def test_handle_change_category_success(tmp_path, monkeypatch):
    storage = setup_storage(tmp_path, monkeypatch)
    storage.add_expense(100, "Еда")

    result = agent.handle_change_category("1", "Покупки")

    assert "изменена" in result
    assert storage.get_all()[0]["category"] == "Покупки"


def test_handle_change_category_invalid_id(tmp_path, monkeypatch):
    setup_storage(tmp_path, monkeypatch)

    assert "ID должен быть целым числом" in agent.handle_change_category("abc", "Еда")


def test_handle_change_category_unknown_id(tmp_path, monkeypatch):
    setup_storage(tmp_path, monkeypatch)

    assert "не найден" in agent.handle_change_category("999", "Еда")


def test_handle_change_category_empty_category(tmp_path, monkeypatch):
    setup_storage(tmp_path, monkeypatch)

    assert "не должна быть пустой" in agent.handle_change_category("1", "   ")


def test_agent_handles_storage_error(tmp_path, monkeypatch):
    storage = setup_storage(tmp_path, monkeypatch)

    def fail_add(amount, category):
        from storage import StorageError

        raise StorageError("Тестовая ошибка")

    monkeypatch.setattr(storage, "add_expense", fail_add)

    assert "Ошибка хранения данных" in agent.handle_add("100", "Еда")
