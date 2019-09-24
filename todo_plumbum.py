#!/usr/bin/env python3
import atexit
import logging

from plumbum import cli, colors
import todolib

levels = [logging.WARNING, logging.INFO, logging.DEBUG]


class App(cli.Application):
    """Todo notes on plumbum."""
    VERSION = todolib.__version__
    verbosity = cli.CountOf("-v", help="Increase verbosity")

    def main(self, *args):
        if args:
            print(colors.red | f"Unknown command: {args[0]!r}.")
            return 1
        if not self.nested_command:           # will be ``None`` if no sub-command follows
            print(colors.red | "No command given.")
            return 1
        level = levels[min(self.verbosity, 2)]
        logging.basicConfig(level=level)
        todolib.log.setLevel(level)


class Command(cli.Application):
    """Command with todoapp object"""
    def __init__(self, executable):
        super().__init__(executable)
        self.todoapp = todolib.TodoApp.fromenv()
        atexit.register(self.todoapp.save)

    def log_task(self, task, msg):
        print("Task", colors.green | task.title, msg, end=".\n")

@App.subcommand("add")
class Add(Command):
    """Add new task"""
    def main(self, task):
        task = self.todoapp.add_task(title=task)
        self.log_task(task, "added to the list")


@App.subcommand("show")
class Show(Command):
    """Show current tasks"""
    show_done = cli.Flag("--show-done", help="Include done tasks")
    def main(self):
        self.todoapp.print_tasks(self.show_done)


@App.subcommand("done")
class Done(Command):
    """Mark task as done"""
    def main(self, number: int):
        task = self.todoapp.task_done(number)
        self.log_task(task, "marked as done")


@App.subcommand("remove")
class Remove(Command):
    """Remove task from the list"""
    def main(self, number: int):
        task = self.todoapp.remove_task(number)
        self.log_task(task, "removed from the list.")

if __name__ == '__main__':
    App.run()
