import dataclasses
import json
import os
import typing as ty
from pathlib import Path

__version__ = "0.1.0"

class TodoApp:
    """ Todo Application definition. """
    def __init__(self, file: Path = None):
        self.file = file
        if not file:
            return
        if not file.exists():
            file.write_text(json.dumps({"tasks": {}, "seq": 0}))
        with file.open() as fp:
            self.db = json.load(fp=fp)

    def get_tasks(self, show_done=False):
        """ Shows existing tasks. """
        yield from (
            Task(app=self, number=i, **t)
            for i, t in self.db["tasks"].items()
            if t["done"] == show_done
        )

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
        file = (
            Path(file) if file else Path().joinpath(".local", "share", "todoapp", "db")
        )
        return cls(file=file)


@dataclasses.dataclass
class Task:
    app: TodoApp
    name: str
    number: int = None
    done: bool = False

    def create(self):
        """ Creates current task in the database. """
        self.number = self.app.db["seq"]
        self.update()
        self.app.db["seq"] += 1

    def asdict(self) -> dict:
        """ Converts task to a dictionary. """
        return {
            k: v
            for k, v in dataclasses.asdict(self).items()
            if k not in {"app", "number"}
        }

    def update(self):
        self.app.db["tasks"][self.number] = self.asdict()

    def remove(self):
        del self.app.db["tasks"][self.number]
