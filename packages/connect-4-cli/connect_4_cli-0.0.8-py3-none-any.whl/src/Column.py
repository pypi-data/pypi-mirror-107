import src.constants as const
from src.Cell import Cell


class Column():
    """Column of a connect4 board, which can hold several checkers."""

    rows_total = const.BOARD_TOTAL_ROWS_PER_COLUMN

    def __init__(self) -> None:
        """Constructor."""
        self.cells = [Cell() for r in range(self.rows_total)]

    def is_full(self):
        """Return if column is full."""
        index = self.get_first_row_empty()
        if index < self.rows_total:
            return False
        return True

    def add_checker_red(self):
        """Add red checker to first empty cell of column."""
        index = self.get_first_row_empty()
        if index < self.rows_total:
            self.cells[index].make_red()

    def add_checker_yellow(self):
        """Add yellow checker to first empty cell of column."""
        index = self.get_first_row_empty()
        if index < self.rows_total:
            self.cells[index].make_yellow()

    def get_rows_empty(self):
        """Return amount of empty rows (cells) in this column."""
        return len([c for c in self.cells if c.is_empty()])

    def get_rows_red(self):
        """Return amount of rows with red checkers in this column."""
        return len([c for c in self.cells if c.is_red()])

    def get_rows_yellow(self):
        """Return amount of rows with yellow checkers in this column."""
        return len([c for c in self.cells if c.is_yellow()])

    def get_first_row_empty(self):
        """Return first empty row (cell) in this column."""
        return self.rows_total - self.get_rows_empty()

    def indexes_rows_red(self):
        """Return reduced list of row indexes with a red checker."""
        return [x for x in range(len(self.cells)) if self.cells[x].is_red()]

    def indexes_rows_yellow(self):
        """Return reduced list of row indexes with a yellow checker."""
        return [x for x in range(len(self.cells)) if self.cells[x].is_yellow()]
