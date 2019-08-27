import argparse
import logging
import sys
import traceback

from todolib import Task, TodoApp, AppException, __version__ as lib_version

log = logging.getLogger(__name__)


def get_parser():
    parser = argparse.ArgumentParser("Todo notes")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose mode"
    )
    parser.add_argument("--version", "-V", action="store_true", help="Show version")
    subparsers = parser.add_subparsers(title="Commands", dest="cmd")

    add = subparsers.add_parser("add", help="Add new task")
    add.add_argument("title", help="Todo title")

    show = subparsers.add_parser("show", help="Show tasks")
    show.add_argument(
        "--show-done", action="store_true", help="Include done tasks in the output"
    )

    done = subparsers.add_parser("done", help="Mark task as done")
    done.add_argument("number", type=int, help="Task number")

    remove = subparsers.add_parser("remove", help="Remove task")
    remove.add_argument("number", type=int, help="Task number")

    return parser


def main(raw_args=None):
    """ Argparse example entrypoint """
    parser = get_parser()
    args = parser.parse_args(raw_args)
    logging.basicConfig()

    if args.verbose:
        logging.getLogger("todolib").setLevel(logging.INFO)
    if args.version:
        print(lib_version)
        sys.exit(0)
    cmd = args.cmd
    if not cmd:
        parser.print_help()
        sys.exit(1)
    app = TodoApp.fromenv()
    try:
        if cmd == "add":
            task = app.add_task(args.title)
            print(f"Task {task.title!r} created with number {task.number}.")
        elif cmd == "show":
            app.print_tasks(args.show_done)
        elif cmd == "done":
            task = app.task_done(args.number)
            print(f"Task {task.title!r} marked as done.")
        elif cmd == "remove":
            task = app.remove_task(args.number)
            print(f"Task {task.title!r} removed from list.")
    except AppException as e:  # pylint:disable=invalid-name
        print("Error:", e)
        sys.exit(2)
    except:  # pylint:disable=bare-except
        traceback.print_exc()
        sys.exit(2)
    finally:
        app.save()
