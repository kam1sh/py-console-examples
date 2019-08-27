import argparse
import logging
import sys
import traceback

from todolib import Task, TodoApp

log = logging.getLogger(__name__)


def get_parser():
    parser = argparse.ArgumentParser("Todo notes")
    subparsers = parser.add_subparsers(title="Commands", dest="cmd")

    add = subparsers.add_parser("add", help="Add new task")
    add.add_argument("title", help="Todo title")

    show = subparsers.add_parser("show", help="Show tasks")
    show.add_argument("--show-done", action="store_true", help="Include done tasks in the output")

    done = subparsers.add_parser("done", help="Mark task as done")
    done.add_argument("number", type=int, help="Task number")

    remove = subparsers.add_parser("remove", help="Remove task")
    remove.add_argument("number", type=int, help="Task number")

    return parser


class Commands:
    """ Collection of todo CLI commands. """
    def __init__(self, app: TodoApp, args: argparse.Namespace):
        self.app = app
        self.args = args

    def add(self):
        task = Task(self.app, self.args.title)
        task.save()
        print(f"Task {task.title!r} created with number {task.number}.")

    def show(self):
        tasks = self.app.list_tasks(show_done=self.args.show_done)
        if not tasks:
            print("There is no TODOs.")
            return
        print("Number\tTitle\tStatus")
        for task in tasks:
            status_char = "✔" if task.done else "✘"
            print(f"{task.number}\t{task.title}\t{status_char}")

    def done(self):
        task = self.app.get_task(self.args.number)
        task.done = True
        task.save()

    def remove(self):
        task = self.app.get_task(self.args.number)
        task.remove()

def main(raw_args=None):
    """ Argparse example entrypoint """
    parser = get_parser()
    args = parser.parse_args(raw_args)

    if not args.cmd or not hasattr(Commands, args.cmd):
        parser.print_help()
        sys.exit(1)
    try:
        app = TodoApp.fromenv()
        cmds = Commands(app, args)
        # execute handler
        getattr(cmds, args.cmd)()
    except:  # pylint:disable=bare-except
        traceback.print_exc()
        sys.exit(2)
    finally:
        app.save()
