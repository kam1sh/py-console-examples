import pytest
from todolib import TodoApp, Task

@pytest.fixture
def app():
    out = TodoApp()
    out.db = {"tasks": {}, "seq": 0}
    return out


def test_new_task(app):
    Task(app, "test application").create()
    assert app.db["tasks"]
    task = app.db["tasks"][0]
    assert task["name"] == "test application"
    assert task["done"] == False
    assert "number" not in task

def test_multiple(app):
    Task(app, "test application").create()
    Task(app, "test application 2").create()
    assert len(app.db["tasks"]) == 2
    assert app.db["tasks"][1]["name"] == "test application 2"

def test_show_tasks(app):
    Task(app, "test application").create()
    tasks = list(app.get_tasks())
    assert tasks
    task = tasks[0]
    assert task.name == "test application"
    assert task.number == 0

def test_update_task(app):
    Task(app, "test application").create()
    task = next(app.get_tasks(), None)
    assert task
    task.done = True
    task.update()
    assert app.db["tasks"][0]["done"]

def test_remove_task(app):
    Task(app, "test application").create()
    task = next(app.get_tasks(), None)
    assert task
    task.remove()
    assert not app.db["tasks"]
