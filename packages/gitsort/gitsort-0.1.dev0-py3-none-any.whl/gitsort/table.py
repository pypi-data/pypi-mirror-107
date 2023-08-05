import json
from rich.table import Table
from rich.console import Console
from rich.style import Style


ALTERNATE = Style(bgcolor="rgb(62,71,86)")


class SortTable:
    def __init__(self, no_of_items, items):
        self._no_of_items = no_of_items
        self._table = Table(row_styles=[
            "none" if i % 2 == 0 else "on rgb(62,71,86)" for i in range(self._no_of_items)
        ])
        self._console = Console()

    def add_column(self, *args, **kwargs):
        self._table.add_column(*args, **kwargs)

    def add_row(self, *args, **kwargs):
        self._table.add_row(*args, **kwargs)

    def render(self, start, no_of_items):
        self._table = Table()
        self._console.print(self._table)


# rgb(62,71,86)
t = SortTable(43)
t.add_column("Link", no_wrap=True)
t.add_column("Author", no_wrap=True)
t.add_column("Created at", no_wrap=True)
t.add_column("Addition", no_wrap=True)
t.add_column("Deletions", no_wrap=True)
t.add_column("Changed files", no_wrap=True)
t.add_column("Comments", no_wrap=True)
t.add_column("State", no_wrap=True)
t.add_column("Updated at", no_wrap=True)
t.add_row("Link", "Ness01", "1 year ago", "1120", "235", "23", "489", "MERGED", "6 years ago")
t.add_row("Link", "Ness01", "1 year ago", "1120", "235", "23", "489", "MERGED", "6 years ago")
t.add_row("Link", "Ness01", "1 year ago", "1120", "235", "23", "489", "MERGED", "6 years ago")
t.add_row("Link", "Ness01", "1 year ago", "1120", "235", "23", "489", "MERGED", "6 years ago")

t.render(0, 5)