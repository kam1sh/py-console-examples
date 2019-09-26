#!/usr/bin/env python3

import cmd2
import todolib


class App(cmd2.Cmd):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.todoapp = todolib.TodoApp.fromenv()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.todoapp.save()

    def do_add(self, title):
        """Add new task."""
        task = self.todoapp.add_task(str(title))
        self.poutput(f"{task} created with number {task.number}.")

    def do_show(self, show_done):
        """Show current tasks."""
        self.todoapp.print_tasks(bool(show_done))

    def do_done(self, number):
        """Mark task as done."""
        task = self.todoapp.task_done(int(number))
        self.poutput(f"{task} marked as done.")

    def do_remove(self, number):
        """Remove task from the list."""
        task = self.todoapp.remove_task(int(number))
        self.poutput(f"{task} removed from the list.")


def main(**kwargs):
    with App(**kwargs) as app:
        app.cmdloop()


if __name__ == "__main__":
    main()
