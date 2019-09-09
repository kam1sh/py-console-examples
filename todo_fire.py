#!/usr/bin/env python3
import atexit
import logging

import fire

import todolib


class Commands:
    def __init__(self, db=None, verbose=False):
        level = logging.INFO if verbose else logging.WARNING
        logging.basicConfig(level=level)
        logging.getLogger("todolib").setLevel(level)
        self._app = todolib.TodoApp.fromenv(db)
        atexit.register(self._app.save)

    def version(self):
        return todolib.__version__

    def add(self, task):
        """Add new task."""
        task = self._app.add_task(task)
        print(task, "created with number", task.number, end=".\n")

    def show(self, show_done=False):
        """ Show current tasks. """
        self._app.print_tasks(show_done)

    def done(self, number):
        """ Mark task as done. """
        task = self._app.task_done(number)
        print(task, "marked as done.")

    def remove(self, number):
        """ Removes task from the list. """
        task = self._app.remove_task(number)
        print(task, "removed from the list.")


def main(args=None):
    fire.Fire(Commands, command=args)


if __name__ == "__main__":
    main()
