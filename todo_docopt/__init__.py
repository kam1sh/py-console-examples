"""Todo notes.

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
from todolib import Task, TodoApp, AppException, __version__ as lib_version

log = logging.getLogger("todo_docopt")

levels = [logging.WARNING, logging.INFO, logging.DEBUG]

def main():
    args = docopt(__doc__, version=lib_version)
    for name in ("todolib", "todo_docopt"):
        logging.getLogger(name).setLevel(levels[args["--verbose"]])
    logging.basicConfig()
    log.debug("Arguments: %s", args)

    app = TodoApp.fromenv()
    try:
        if args["add"]:
            task = app.add_task(args["<task>"])
            print(f"Task {task.title!r} created with number {task.number}.")
        elif args["show"]:
            app.print_tasks(args["--show-done"])
        elif args["done"]:
            task = app.task_done(args["<number>"])
            print(f"Task {task.title!r} marked as done.")
        elif args["remove"]:
            task = app.remove_task(args["<number>"])
            print(f"Task {task.title!r} removed from list.")
    except AppException as e:  # pylint:disable=invalid-name
        print("Error:", e)
        sys.exit(2)
    except:  # pylint:disable=bare-except
        traceback.print_exc()
        sys.exit(2)
    finally:
        pass
