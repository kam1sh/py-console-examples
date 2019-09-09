#!/usr/bin/env python3
"""Todo notes - docopt version.

Usage:
  todonotes [-v | -vv ] add <task>
  todonotes [-v | -vv ] show --show-done
  todonotes [-v | -vv ] done <number>
  todonotes [-v | -vv ] remove <number>
  todonotes -h | --help
  todonotes --version

Options:
  -h --help     Show help.
  -v --verbose  Enable verbose mode.
"""
import logging
import sys
import traceback

from docopt import docopt

from todolib import TodoApp, AppError, __version__ as lib_version

log = logging.getLogger("todolib")

levels = [logging.WARNING, logging.INFO, logging.DEBUG]


def main(argv=None):
    args = docopt(__doc__, argv=argv, version=lib_version)
    log.setLevel(levels[args["--verbose"]])
    logging.basicConfig()
    log.debug("Arguments: %s", args)

    with TodoApp.fromenv() as app:
        try:
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
        except AppError as e:  # pylint:disable=invalid-name
            print("Error:", e)
            sys.exit(2)
        except:  # pylint:disable=bare-except
            traceback.print_exc()
            sys.exit(2)
