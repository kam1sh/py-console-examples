#!/usr/bin/env python3
import plac
import todolib

class TodoInterface:
    commands = "add", "show", "done", "remove"

    def __init__(self):
        self.app = todolib.TodoApp.fromenv()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.app.save()

    def add(self, task):
        """ Add new task. """
        task = self.app.add_task(title=task)
        print(task, "created with number", task.number, end=".\n")

    def show(self, show_done: plac.Annotation("Include done tasks", kind="flag")):
        """ Show current tasks. """
        self.app.print_tasks(show_done=show_done)

    def done(self, number: "Task number"):
        """ Mark task as done. """
        task = self.app.task_done(number=int(number))
        print(task, "marked as done.")

    def remove(self, number):
        """ Remove task from the list. """
        task = self.app.remove_task(number=int(number))
        print(task, "removed from the list.")

if __name__ == "__main__":
    plac.Interpreter.call(TodoInterface)
