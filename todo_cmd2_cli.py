#!/usr/bin/env python3
import sys

import cmd2
import todolib
from todo_argparse import get_parser


parser = get_parser(progname="todo_cmd2_cli")


class App(cmd2.Cmd):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.todoapp = todolib.TodoApp.fromenv()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.todoapp.save()

    def do_add(self, args):
        """Add new task."""
        task = self.todoapp.add_task(args.title)
        self.poutput(f"{task} created with number {task.number}.")

    def do_show(self, args):
        """Show current tasks."""
        self.todoapp.print_tasks(args.show_done)

    def do_done(self, args):
        """Mark task as done."""
        task = self.todoapp.task_done(args.number)
        self.poutput(f"{task} marked as done.")

    def do_remove(self, args):
        """Remove task from the list."""
        task = self.todoapp.remove_task(args.number)
        self.poutput(f"{task} removed from the list.")

    parser.add.set_defaults(func=do_add)
    parser.show.set_defaults(func=do_show)
    parser.done.set_defaults(func=do_done)
    parser.remove.set_defaults(func=do_remove)

    @cmd2.with_argparser(parser)
    def do_base(self, args):
        func = getattr(args, "func", None)
        if func:
            func(self, args)
        else:
            print("No command provided.")
            print("Call with --help to get available commands.")


def main(argv=None):
    with App() as app:
        app.do_base(argv or sys.argv[1:])


if __name__ == "__main__":
    main()
