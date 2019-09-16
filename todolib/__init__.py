import dataclasses
import json
import logging
import os
import typing as ty
from pathlib import Path

__version__ = "1.0.3"

log = logging.getLogger(__name__)


class TodoApp:
    """ Todo Application definition. """

    def __init__(self, file: Path = None):
        self.file = file
        if not file:
            log.info(
                "File is not passed. Provide database dictionary"
                "manually via attribute 'db'."
            )
            return
        self.db = self.get_db()

    def get_db(self):
        if not self.file.exists():
            return {"tasks": []}
        else:
            with self.file.open() as fp:
                return json.load(fp=fp)

    def list_tasks(self, show_done=False) -> ty.List["Task"]:
        """ Shows existing tasks. """
        out = [
            Task(app=self, number=i, **t)
            for i, t in enumerate(self.db["tasks"])
            if t["done"] in {False, show_done}
        ]
        log.debug("Database tasks: %s", out)
        return out

    def get_task(self, number) -> "Task":
        try:
            raw = self.db["tasks"][number]
        except IndexError:
            raise AppError("No such task.") from None
        log.debug("Task raw: %s", raw)
        return Task(app=self, number=number, **raw)

    def add_task(self, title) -> "Task":
        task = Task(self, title)
        task.save()
        return task

    def print_tasks(self, show_done):
        tasks = self.list_tasks(show_done=show_done)
        if not tasks:
            print("There is no TODOs.")
            return
        print("Number\tTitle\tStatus")
        for task in tasks:
            status_char = "✔" if task.done else "✘"
            print(f"{task.number}\t{task.title}\t{status_char}")

    def task_done(self, number) -> "Task":
        task = self.get_task(number)
        task.done = True
        task.save()
        return task

    def remove_task(self, number) -> "Task":
        task = self.get_task(number)
        task.remove()
        return task

    def save(self):
        """ Saves database. """
        if not self.file:
            log.warning("Tried to call save() with no file provided.")
            return
        log.info("Saving database to a file %s", self.file)
        with self.file.open("w") as fd:
            log.debug("Database contents: %s", self.db)
            json.dump(self.db, fd)

    @classmethod
    def fromenv(cls, value=None):
        """
        Creates application with database
        from the environment variable 'TODO_DB'.
        """
        file = value or os.getenv("TODO_DB")
        log.debug("TODO_DB value: %s", file)
        if not file:
            folder = Path.home() / ".local" / "share" / "todoapp"
            folder.mkdir(parents=True, exist_ok=True)
            file = folder / "db.json"
        else:
            file = Path(file)
        log.info("Using database file %s", file)
        return cls(file=file)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.save()


@dataclasses.dataclass
class Task:
    app: TodoApp
    title: str
    number: int = None
    done: bool = False

    def create(self):
        """ Creates current task in the database. """
        self.number = len(self.app.db["tasks"])
        self.app.db["tasks"].append(self.asdict())

    def asdict(self) -> dict:
        """ Converts task to a dictionary. """
        return {
            k: v
            for k, v in dataclasses.asdict(self).items()
            if k not in {"app", "number"}
        }

    def update(self):
        """ Rewrites task in the database. """
        self.app.db["tasks"][self.number] = self.asdict()

    def save(self):
        """
        Creates new task if there is no number,
        otherwise updates current.
        """
        if self.number is None:
            return self.create()
        self.update()

    def remove(self):
        """ Removes task from the database. """
        del self.app.db["tasks"][self.number]

    def __str__(self):
        return f"Task '{self.title}'"


class AppError(Exception):
    pass
