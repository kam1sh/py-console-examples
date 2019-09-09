#!/usr/bin/env python3

from cement import App, CaughtSignal, Controller, ex

import todolib


class Base(Controller):
    class Meta:
        label = "base"

        arguments = [
            (
                ["-v", "--version"],
                {"action": "version", "version": f"todo_cement v{todolib.__version__}"},
            )
        ]

    def _default(self):
        """Default action if no sub-command is passed."""
        self.app.args.print_help()

    @ex(help="Add new task", arguments=[(["task"], {"help": "Task title"})])
    def add(self):
        """Example sub-command."""
        title = self.app.pargs.task
        self.app.log.debug(f"Task title: {title!r}")
        task = self.app.todoobj.add_task(title)
        print(task, "created with number", task.number, end=".\n")

    @ex(
        help="Show current tasks",
        arguments=[
            (["--show-done"], dict(action="store_true", help="Include done tasks"))
        ],
    )
    def show(self):
        self.app.todoobj.print_tasks(self.app.pargs.show_done)

    @ex(help="Mark task as done", arguments=[(["number"], {"type": int})])
    def done(self):
        task = self.app.todoobj.task_done(self.app.pargs.number)
        print(task, "marked as done.")

    @ex(help="Remove task from the list", arguments=[(["number"], {"type": int})])
    def remove(self):
        task = self.app.todoobj.remove_task(self.app.pargs.number)
        print(task, "removed from the list.")


def extend_db(app):
    app.todoobj = todolib.TodoApp.fromenv()


def close_db(app):
    app.todoobj.save()


class TodoApp(App):
    def __init__(self, argv=None):
        super().__init__(argv=argv)
        self.todoobj = None

    class Meta:
        # application label
        label = "todo_cement"
        # register handlers
        handlers = [Base]
        hooks = [("post_setup", extend_db), ("pre_close", close_db)]
        # call sys.exit() on close
        close_on_exit = True


def main():
    with TodoApp() as app:
        try:
            app.run()
        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print("\n%s" % e)
            app.exit_code = 0


if __name__ == "__main__":
    main()
