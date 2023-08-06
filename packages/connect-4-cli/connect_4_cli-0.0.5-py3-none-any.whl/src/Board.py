import src.constants as const
from src.Column import Column
from src.BoardValidator import BoardValidator


class Board():
    """Logic of connect4 board."""

    columns_total = const.BOARD_TOTAL_COLUMNS

    def __init__(self) -> None:
        """Constructor."""
        self.columns = [Column() for c in range(self.columns_total)]
        self.validator = BoardValidator()

    def is_game_won(self):
        """Return if game has already been won by a player."""
        return (self.validator.game_won(self.columns))

    def add_checker_red(self, column):
        """Add red checker to selected column by index."""
        self.columns[column].add_checker_red()

    def add_checker_yellow(self, column):
        """Add yellow checker to selected column by index."""
        self.columns[column].add_checker_yellow()
