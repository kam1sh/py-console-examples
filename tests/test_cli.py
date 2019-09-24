import cleo
import click.testing
import pytest
import plac

import todo_argparse
import todo_cement
import todo_cleo
import todo_click
import todo_cliff
import todo_docopt
import todo_fire
import todo_plac
import todo_plumbum
import todolib


@pytest.fixture(autouse=True)
def db(monkeypatch):
    """
    monkeypatch database load, so there would be empty database
    before each test
    """
    value = {"tasks": []}
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


def test_docopt(capsys):
    todo_docopt.main(["add", "test"])
    out, _ = capsys.readouterr()
    assert out == EXPECTED


def test_click():
    runner = click.testing.CliRunner()
    result = runner.invoke(todo_click.cli, ["add", "test"])
    assert result.exit_code == 0
    assert result.output == EXPECTED


def test_fire(capsys):
    todo_fire.main(["add", "test"])
    out, _ = capsys.readouterr()
    assert out == EXPECTED


def test_cement(capsys):
    with todo_cement.TodoApp(argv=["add", "test"]) as app:
        app.run()
        out, _ = capsys.readouterr()
        assert out == EXPECTED
        # for asserting jinja output, not used in this application
        assert app.last_rendered is None


def test_cleo():
    app = todo_cleo.TodoApp()
    command = app.find("add")
    tester = cleo.CommandTester(command)
    tester.execute("test")
    assert tester.status_code == 0
    assert tester.io.fetch_output() == "Task test created with number 0.\n"


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
    todo_plumbum.App.run(["todo_plumbum", "add", "test"], exit=False)
    out, _ = capsys.readouterr()
    assert out == "Task test added to the list.\n"


