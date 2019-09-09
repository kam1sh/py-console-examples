import atexit
import logging

import click

from todolib import TodoApp, __version__ as lib_version

levels = [logging.WARN, logging.INFO, logging.DEBUG]

pass_app = click.make_pass_decorator(TodoApp)


@click.group()
@click.version_option(lib_version, prog_name="todo_click")
@click.option("-v", "--verbose", count=True)
@click.option("--db", help="Path to the database file")
@click.pass_context
def cli(ctx, verbose, db):
    """Todo notes - click version."""
    logging.basicConfig()
    level = levels[min(verbose, 2)]
    logging.getLogger("todolib").setLevel(level)
    ctx.obj = TodoApp.fromenv(db)
    atexit.register(ctx.obj.save)


@cli.command()
@click.argument("task")
@pass_app
def add(app, task):
    """ Add new task. """
    task = app.add_task(task)
    click.echo(f"{task} created with number {task.number}.")


@cli.command()
@click.option("--show-done", is_flag=True)
@pass_app
def show(app, show_done):
    """ Show current tasks. """
    app.print_tasks(show_done)


@cli.command()
@click.argument("number", type=int)
@pass_app
def done(app, number):
    """ Mark task as done. """
    task = app.task_done(number)
    click.echo(f"{task} marked as done.")


@cli.command()
@click.argument("number", type=int)
@pass_app
def remove(app, number):
    """ Removes task from the list. """
    task = app.remove_task(number)
    click.echo(f"{task} removed from list.")


@cli.command()
@click.confirmation_option(prompt="Are you sure you want to remove database")
@pass_app
def wipe(app):
    for task in app.list_tasks():
        task.remove()


if __name__ == "__main__":
    cli(auto_envvar_prefix="TODO")  # pylint:disable=all
