"""
Example todo application.
Some parts may not be as performant or elegant as you expect,
but hey, the matter is CLI interfaces.
"""

import pytest
from todolib import TodoApp, Task

@pytest.fixture
def app():
    out = TodoApp()
    out.db = {"tasks": []}
    return out


def test_new_task(app):
    Task(app, "test application").create()
    assert app.db["tasks"]
    task = app.db["tasks"][0]
    assert task["title"] == "test application"
    assert task["done"] == False
    assert "number" not in task

def test_multiple(app):
    Task(app, "test application").create()
    Task(app, "test application 2").create()
    assert len(app.db["tasks"]) == 2
    assert app.db["tasks"][1]["title"] == "test application 2"

def test_show_tasks(app):
    Task(app, "test application").create()
    tasks = list(app.list_tasks())
    assert tasks
    task = tasks[0]
    assert task.title == "test application"
    assert task.number == 0

def test_update_task(app):
    Task(app, "test application").create()
    task = app.list_tasks()[0]
    assert task
    task.done = True
    task.update()
    assert app.db["tasks"][0]["done"]

def test_remove_task(app):
    Task(app, "test application").create()
    task = app.list_tasks()[0]
    assert task
    task.remove()
    assert not app.db["tasks"]

def test_update_size(app):
    Task(app, "test application").create()
    Task(app, "test application 2").create()
    Task(app, "test application 3").create()
    tasks = list(app.list_tasks())
    tasks[1].remove()
    assert list(app.list_tasks())[1].title.endswith("3")

