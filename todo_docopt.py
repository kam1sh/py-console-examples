#!/usr/bin/env python3
"""Todo notes - docopt version.

Usage:
  todo_docopt [-v | -vv ] add <task>
  todo_docopt [-v | -vv ] show --show-done
  todo_docopt [-v | -vv ] done <number>
  todo_docopt [-v | -vv ] remove <number>
  todo_docopt -h | --help
  todo_docopt --version

Options:
  -h --help     Show help.
  -v --verbose  Enable verbose mode.
"""
import logging

from docopt import docopt

from todolib import TodoApp, __version__ as lib_version

log = logging.getLogger("todolib")

levels = [logging.WARNING, logging.INFO, logging.DEBUG]


def main(argv=None):
    args = docopt(__doc__, argv=argv, version=lib_version)
    log.setLevel(levels[args["--verbose"]])
    logging.basicConfig()
    log.debug("Arguments: %s", args)

    with TodoApp.fromenv() as app:
        if args["add"]:
            task = app.add_task(args["<task>"])
            print(task, "created with number", task.number, end=".\n")
        elif args["show"]:
            app.print_tasks(args["--show-done"])
        elif args["done"]:
            task = app.task_done(args["<number>"])
            print(task, "marked as done.")
        elif args["remove"]:
            task = app.remove_task(args["<number>"])
            print(task, "removed from list.")
