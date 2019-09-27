#!/usr/bin/env python3
import sys

from cliff import app
from cliff.commandmanager import CommandManager
from cliff import command
from cliff.lister import Lister

from todolib import TodoApp, __version__


class Command(command.Command):
    """Command with a parser shortcut."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        self.extend_parser(parser)
        return parser

    def extend_parser(self, parser):
        ...


class Add(Command):
    """Add new task."""

    def extend_parser(self, parser):
        parser.add_argument("title", help="Task title")

    def take_action(self, args):
        task = self.app.todoapp.add_task(args.title)
        print(task, "created with number", task.number, end=".\n")


class Show(Lister, Command):
    """Show current tasks."""

    def extend_parser(self, parser):
        parser.add_argument(
            "--show-done", action="store_true", help="Include done tasks"
        )

    def take_action(self, args):
        tasks = self.app.todoapp.list_tasks(show_done=args.show_done)
        # no 'there is no todos' message in order to support csv/etc
        # empty result formatting properly
        return (
            ("Number", "Title", "Status"),
            [[task.number, task.title, "✔" if task.done else "✘"] for task in tasks],
        )


class Done(Command):
    """Mark task as done."""

    def extend_parser(self, parser):
        parser.add_argument("number", type=int, help="Task number")

    def take_action(self, args):
        task = self.app.todoapp.task_done(number=args.number)
        print(task, "marked as done.")


# inherited from Done for argparser reuse
class Remove(Done):
    """Remove task from the list."""

    def take_action(self, args):
        task = self.app.todoapp.remove_task(number=args.number)
        print(task, "removed from the list.")


class App(app.App):
    def __init__(self):
        # besides that, CommandManager can extract commands list
        # from setuptools entrypoints
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


def main(argv=None) -> int:
    app = App()
    return app.run(argv=argv or sys.argv[1:])


if __name__ == "__main__":
    main()
