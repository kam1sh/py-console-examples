import dataclasses
import json
import logging
import os
import typing as ty
from pathlib import Path

__version__ = "0.2.0"

log = logging.getLogger(__name__)


class TodoApp:
    """ Todo Application definition. """
    def __init__(self, file: Path = None):
        self.file = file
        if not file:
            return
        if not file.exists():
            file.write_text(json.dumps({"tasks": [], "seq": 0}))
        with file.open() as fp:
            self.db = json.load(fp=fp)

    def list_tasks(self, show_done=False) -> ty.Iterable["Task"]:
        """ Shows existing tasks. """
        return [
            Task(app=self, number=i, **t)
            for i, t in enumerate(self.db["tasks"])
            if t["done"] in {False, show_done}
        ]

    def get_task(self, number) -> "Task":
        raw = self.db["tasks"][number]
        return Task(app=self, number=number, **raw)

    def save(self):
        """ Saves database. """
        with self.file.open("w") as fd:
            json.dump(self.db, fd)

    @classmethod
    def fromenv(cls):
        """
        Creates application with database
        from the environment variable 'TODO_DB'.
        """
        file = os.getenv("TODO_DB")
        if not file:
            folder = Path.home() / ".local" / "share" / "todoapp"
            folder.mkdir(parents=True, exist_ok=True)
            file = folder / "db.json"
        else:
            file = Path(file)
        return cls(file=file)


@dataclasses.dataclass
class Task:
    app: TodoApp
    title: str
    number: int = None
    done: bool = False

    def create(self):
        """ Creates current task in the database. """
        self.number = len(self.app.db["tasks"]) + 1
        self.app.db["tasks"].append(self.asdict())
        self.app.db["seq"] += 1

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
