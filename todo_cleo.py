#!/usr/bin/env python3

from cleo import Application as BaseApplication, Command as BaseCommand
# cleo is a wrapper around clikit, and sometimes you have to access low-level library
from clikit.api.io import flags as verbosity

import todolib


# command with methods common for our application
class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.todoapp = None

    def handle(self):
        with todolib.TodoApp.fromenv() as app:
            self.todoapp = app
            self.do_handle()

    def do_handle(self):
        raise NotImplementedError


class AddCommand(Command):
    """
    Add new task.

    add {task : Task to add}
    """

    def do_handle(self):
        title = self.argument("task")
        task = self.todoapp.add_task(title)
        # will be printed only on "-vvv"
        self.line(f"Title: {title}", style="comment", verbosity=verbosity.DEBUG)
        self.line(f"Task <info>{task.title}</> created with number {task.number}.")


class ShowCommand(Command):
    """
    Show current tasks.

    show {--show-done : Include tasks that are done.}
    """

    def do_handle(self):
        tasks = self.todoapp.list_tasks(self.option("show-done"))
        if not tasks:
            self.line("There is no TODOs.", style="info")
        self.render_table(
            ["Number", "Title", "Status"],
            [
                [str(task.number), task.title, "✔" if task.done else "✘"]
                for task in tasks
            ],
        )


class DoneCommand(Command):
    """
    Mark task as done.

    done {number : Task number}
    """

    def do_handle(self):
        task = self.todoapp.task_done(int(self.argument("number")))
        self.line(f"Task <info>{task.title}</> marked as done.")


class RemoveCommand(Command):
    """
    Removes task from the list.

    remove {number : Task number}
    """

    def do_handle(self):
        task = self.todoapp.remove_task(int(self.argument("number")))
        self.line(f"Task <info>{task.title}</> removed from the list.")


class TodoApp(BaseApplication):
    def __init__(self):
        super().__init__(name="ToDo app - cleo version", version=todolib.__version__)
        self.add_commands(AddCommand(), ShowCommand(), DoneCommand(), RemoveCommand())


def main(args=None):
    TodoApp().run(args=args)


if __name__ == "__main__":
    main()
