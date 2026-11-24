import agent
import cli
from storage import ExpenseStorage


def test_print_help(capsys):
    cli.print_help()

    output = capsys.readouterr().out

    assert "add" in output
    assert "show" in output
    assert "change" in output
    assert "exit" in output


def test_cli_add_show_and_exit(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(
        agent,
        "storage",
        ExpenseStorage(tmp_path / "expenses.json"),
    )

    commands = iter(
        [
            "add 500 Покупки",
            "show",
            "exit",
        ]
    )

    monkeypatch.setattr("builtins.input", lambda _: next(commands))

    cli.run_cli()

    output = capsys.readouterr().out

    assert "Успешно добавлено" in output
    assert "Покупки" in output


def test_cli_help_and_exit(monkeypatch, capsys):
    commands = iter(["help", "exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(commands))

    cli.run_cli()

    output = capsys.readouterr().out

    assert "add" in output
    assert "show" in output


def test_cli_handles_unknown_command(monkeypatch, capsys):
    commands = iter(["unknown", "exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(commands))

    cli.run_cli()

    output = capsys.readouterr().out

    assert "Неизвестная команда" in output


def test_cli_handles_keyboard_interrupt(monkeypatch, capsys):
    def interrupt(_):
        raise KeyboardInterrupt

    monkeypatch.setattr("builtins.input", interrupt)

    cli.run_cli()

    output = capsys.readouterr().out

    assert "Завершение" in output


def test_cli_handles_eof(monkeypatch, capsys):
    def eof(_):
        raise EOFError

    monkeypatch.setattr("builtins.input", eof)

    cli.run_cli()

    output = capsys.readouterr().out

    assert "Завершение" in output


def test_cli_handles_invalid_arguments_and_continues(monkeypatch, capsys):
    commands = iter(
        [
            "add 500",
            "show extra",
            "exit",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(commands))

    cli.run_cli()

    output = capsys.readouterr().out
    assert "Ошибка: Неверный формат" in output
    assert "Завершение работы" in output
