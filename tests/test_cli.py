import click.testing
import pytest

import todo_argparse
import todo_click
import todo_docopt
import todolib


@pytest.fixture(autouse=True)
def db(monkeypatch):
    """
    monkeypatch получения базы данных из файла,
    чтобы перед тестами всегда была пустая база.
    """
    value = {"tasks": []}
    monkeypatch.setattr(todolib.TodoApp, "get_db", lambda _: value)
    return value


@pytest.yield_fixture(autouse=True)
def check(db):
    """ Функция для проверки содержимого БД. """
    yield
    assert db["tasks"] and db["tasks"][0]["title"] == "test"


EXPECTED = "Task 'test' created with number 1.\n"


def test_argparse(capsys):
    todo_argparse.main(["add", "test"])
    out, _ = capsys.readouterr()
    assert out == EXPECTED


def test_docopt(capsys):
    todo_docopt.main(["add", "test"])
    out, _ = capsys.readouterr()
    assert out == EXPECTED


def test_click():
    runner = click.testing.CliRunner()
    result = runner.invoke(todo_click.cli, ["add", "test"])
    assert result.exit_code == 0
    assert result.output == EXPECTED
