import logging
import sys
import traceback

import click
from todolib import Task, TodoApp, AppError, __version__ as lib_version

levels = [logging.WARN, logging.INFO, logging.DEBUG]


@click.group()
@click.version_option(lib_version, prog_name="todo_click")
@click.option("-v", "--verbose", count=True)
def cli(verbose):
    """Todo notes - click version."""
    logging.basicConfig()
    logging.getLogger("todolib").setLevel(
        logging.DEBUG if verbose > 2 else levels[verbose]
    )


@cli.command()
@click.argument("task")
def add(task):
    """ Add new task. """
    with TodoApp.fromenv() as app:
        task = app.add_task(task)
    click.echo(f"Task {task.title!r} created with number {task.number}.")


@cli.command()
@click.option("--show-done", is_flag=True)
def show(show_done):
    """ Show current tasks. """
    with TodoApp.fromenv() as app:
        app.print_tasks(show_done)


@cli.command()
@click.argument("number", type=int)
def done(number):
    """ Mark task as done. """
    with TodoApp.fromenv() as app:
        task = app.task_done(number)
    click.echo(f"Task {task.title!r} marked as done.")


@cli.command()
@click.argument("number", type=int)
def remove(number):
    """ Removes task from the list. """
    with TodoApp.fromenv() as app:
        task = app.remove_task(number)
    click.echo(f"Task {task.title!r} removed from list.")


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@cli.command()
@click.option("--db")
@click.option(
    "--yes",
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt="Are you sure you want to drop the db?",
)
def wipe(db):
    with TodoApp.fromenv(db) as app:
        for task in app.list_tasks():
            task.remove()


if __name__ == "__main__":
    cli(auto_envvar_prefix="TODO")  # pylint:disable=all
