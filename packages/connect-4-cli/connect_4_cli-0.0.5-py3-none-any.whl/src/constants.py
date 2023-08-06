from enum import Enum


BOARD_TOTAL_COLUMNS = 7
BOARD_TOTAL_ROWS_PER_COLUMN = 6


class PlayerTurn(Enum):
    """Type of player turn."""
    RED = 0
    YELLOW = 1


class MatchState(Enum):
    """States of a connect4 match."""
    PLAYING = 0
    RED_WON = 1
    YELLOW_WON = 2
    TIE = 3


class CellState(Enum):
    """State of a cell."""
    EMPTY = 0
    RED = 1
    YELLOW = 2


class ValidUserInput(Enum):
    """Accepted keyboard inputs from user."""
    ARROW_LEFT = 0
    ARROW_RIGHT = 1
    ENTER = 2
    KEY_R = 3
    KEY_Q = 4
    OTHER = 5
