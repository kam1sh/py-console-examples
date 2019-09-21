#!/usr/bin/env python3
import sys

from cliff import app
from cliff.commandmanager import CommandManager
from cliff.command import Command
from cliff.lister import Lister

from todolib import TodoApp, __version__


class Add(Command):
    """Add new task."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name=prog_name)
        parser.add_argument("title", help="Task title")
        return parser

    def take_action(self, parsed_args):
        task = self.app.todoapp.add_task(parsed_args.title)
        print(task, "created with number", task.number, end=".\n")


class Show(Lister):
    """Show current tasks."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name=prog_name)
        parser.add_argument(
            "--show-done", action="store_true", help="Include done tasks"
        )
        return parser

    def take_action(self, parsed_args):
        tasks = self.app.todoapp.list_tasks(show_done=parsed_args.show_done)
        # no 'there is no todos' message in order to support csv/etc
        # empty result formatting properly
        return (
            ("Number", "Title", "Status"),
            [
                [task.number, task.title, "✔" if task.done else "✘"]
                for task in tasks
            ],
        )


class Done(Command):
    """Mark task as done."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name=prog_name)
        parser.add_argument("number", type=int, help="Task number")
        return parser

    def take_action(self, parsed_args):
        task = self.app.todoapp.task_done(number=parsed_args.number)
        print(task, "marked as done.")


class Remove(Done):
    """Remove task from the list."""

    def take_action(self, parsed_args):
        task = self.app.todoapp.remove_task(number=parsed_args.number)
        print(task, "removed from the list.")


class App(app.App):
    def __init__(self):
        manager = CommandManager("todo_cliff")
        manager.add_command("add", Add)
        manager.add_command("show", Show)
        manager.add_command("done", Done)
        manager.add_command("remove", Remove)
        super().__init__(
            description="Todo notes on cliff",
            version=__version__,
            command_manager=manager,
            deferred_help=True,
        )
        self.todoapp = None

    def initialize_app(self, argv):
        self.todoapp = TodoApp.fromenv()

    def clean_up(self, cmd, result, err):
        self.todoapp.save()


def main(args=sys.argv[1:]) -> int:
    app = App()
    return app.run(argv=args)


if __name__ == "__main__":
    main()
