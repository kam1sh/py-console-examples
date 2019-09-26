#!/usr/bin/env python3
import argparse
import logging

from todolib import TodoApp, __version__ as lib_version


def get_parser(progname="todo_argparse"):
    parser = argparse.ArgumentParser(progname)
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose mode"
    )
    parser.add_argument("--version", "-V", action="store_true", help="Show version")
    subparsers = parser.add_subparsers(title="Commands", dest="cmd")

    parser.add = subparsers.add_parser("add", help="Add new task")
    parser.add.add_argument("title", help="Task title")

    parser.show = subparsers.add_parser("show", help="Show tasks")
    parser.show.add_argument(
        "--show-done", action="store_true", help="Include done tasks in the output"
    )

    parser.done = subparsers.add_parser("done", help="Mark task as done")
    parser.done.add_argument("number", type=int, help="Task number")

    parser.remove = subparsers.add_parser("remove", help="Remove task")
    parser.remove.add_argument("number", type=int, help="Task number")

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
        exit(0)
    cmd = args.cmd
    if not cmd:
        parser.print_help()
        exit(1)
    with TodoApp.fromenv() as app:
        if cmd == "add":
            task = app.add_task(args.title)
            print(task, "created with number", task.number, end=".\n")
        elif cmd == "show":
            app.print_tasks(args.show_done)
        elif cmd == "done":
            task = app.task_done(args.number)
            print(task, "marked as done.")
        elif cmd == "remove":
            task = app.remove_task(args.number)
            print(task, "removed from list.")


if __name__ == "__main__":
    main()
