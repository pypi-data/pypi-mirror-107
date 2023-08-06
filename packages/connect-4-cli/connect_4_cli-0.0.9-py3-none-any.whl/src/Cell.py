import src.constants as const


class Cell():
    """Cell of a connect4 board, which can hold one checker."""

    def __init__(self) -> None:
        """Constructor."""
        self.current_state = const.CellState.EMPTY

    def is_empty(self):
        """Return if cell is empty."""
        return (self.current_state == const.CellState.EMPTY)

    def is_red(self):
        """Return if cell is occupied with a red checker."""
        return (self.current_state == const.CellState.RED)

    def is_yellow(self):
        """Return if cell is occupied with a yellow checker."""
        return (self.current_state == const.CellState.YELLOW)

    def make_red(self):
        """Add a red checker to this cell"""
        self.current_state = const.CellState.RED

    def make_yellow(self):
        """Add a yellow checker to this cell"""
        self.current_state = const.CellState.YELLOW
