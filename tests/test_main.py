import runpy

import cli


def test_main_starts_cli(monkeypatch):
    called = []

    monkeypatch.setattr(cli, "run_cli", lambda: called.append(True))

    runpy.run_module("main", run_name="__main__")

    assert called == [True]
