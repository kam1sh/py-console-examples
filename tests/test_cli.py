import pytest
import plac

import todo_argparse
import todo_cliff
import todo_cmd2
import todo_plac
import todo_plumbum
import todolib


@pytest.fixture(autouse=True)
def db(monkeypatch):
    """
    monkeypatch database load/save, so there would be empty database
    before each test and original db won't be changed
    """
    value = {"tasks": []}
    monkeypatch.setattr(todolib.TodoApp, "save", lambda _: ...)
    monkeypatch.setattr(todolib.TodoApp, "get_db", lambda _: value)
    return value


@pytest.yield_fixture(autouse=True)
def check(db):
    """ fixture for asserting database contents """
    yield
    assert db["tasks"] and db["tasks"][0]["title"] == "test"


EXPECTED = "Task 'test' created with number 0.\n"


def test_argparse(capsys):
    todo_argparse.main(["add", "test"])
    out, _ = capsys.readouterr()
    assert out == EXPECTED


def test_cliff(capsys):
    app = todo_cliff.App()
    code = app.run(["add", "test"])
    assert code == 0
    out, _ = capsys.readouterr()
    assert out == EXPECTED


def test_plac(capsys):
    plac.Interpreter.call(todo_plac.TodoInterface, arglist=["add", "test"])
    out, _ = capsys.readouterr()
    assert out == EXPECTED


def test_plumbum(capsys):
    _, code = todo_plumbum.App.run(["todo_plumbum", "add", "test"], exit=False)
    assert code == 0
    out, _ = capsys.readouterr()
    assert out == "Task test created with number 0.\n"


def test_cmd2():
    todo_cmd2.main(transcript_files=["tests/transcript.txt"])
