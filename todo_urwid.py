#!/usr/bin/env python3
import urwid
from urwid import Button
import todolib


class App(urwid.WidgetPlaceholder):
    max_box_levels = 4
    def __init__(self):
        super().__init__(urwid.SolidFill())
        self.todoapp = None
        self.box_level = 0

    def __enter__(self):
        self.todoapp = todolib.TodoApp.fromenv()
        self.new_menu(
            "Todo notes on urwid",
            # button has a label and handle, that should accept
            # one argument (button object itself)
            Button("New task", on_press=add),
            Button("List tasks", on_press=list_tasks),
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.todoapp.save()

    def new_menu(self, title, *items):
        self.new_box(menu(title, *items))

    def new_box(self, widget):
        self.box_level += 1
        # overlay allows to draw one widget on top of the other,
        # in this case - new LineBox on top of the previous current widget
        self.original_widget = urwid.Overlay(
            # LineBox draws a line around passed widget
            urwid.LineBox(widget),
            self.original_widget,
            align="center",
            width=30,
            valign="middle",
            height=10,
        )

    def popup(self, text):
        self.new_menu(text, Button("To menu", on_press=lambda _: self.pop(levels=2)))

    def keypress(self, size, key):
        if key != "esc":
            super().keypress(size, key=key)
        elif self.box_level > 0:
            self.pop()

    def pop(self, levels=1):
        for _ in range(levels):
            self.original_widget = self.original_widget[0]
        self.box_level -= levels
        if self.box_level == 0:
            raise urwid.ExitMainLoop()


app = App()


def menu(title, *items) -> urwid.ListBox:
    body = [urwid.Text(title), urwid.Divider()]
    body.extend(items)
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


def add(button):
    edit = urwid.Edit("Title: ")

    def handle(button):
        text = edit.edit_text
        app.todoapp.add_task(text)
        app.popup("Task added")

    app.new_menu("New task", edit, Button("Add", on_press=handle))


def list_tasks(button):
    tasks = app.todoapp.list_tasks(show_done=True)
    buttons = []
    for task in tasks:
        status = "done" if task.done else "not done"
        text = f"{task.title} [{status}]"
        # button can also pass additional data into callbacks
        button = Button(text, on_press=task_actions, user_data=task.number)
        buttons.append(button)
    app.new_menu("Task list", *buttons)


def task_actions(button, number):
    def done(button, number):
        app.todoapp.task_done(number)
        app.popup("Task marked as done.")

    def remove(button, number):
        app.todoapp.remove_task(number)
        app.popup("Task removed from the list.")

    btn_done = Button("Mark as done", on_press=done, user_data=number)
    btn_remove = Button("Remove from the list", on_press=remove, user_data=number)
    app.new_menu("Actions", btn_done, btn_remove)


if __name__ == "__main__":
    try:
        with app:
            urwid.MainLoop(app).run()
    except KeyboardInterrupt:
        pass
