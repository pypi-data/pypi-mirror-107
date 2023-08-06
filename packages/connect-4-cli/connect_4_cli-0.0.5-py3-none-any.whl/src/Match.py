import src.constants as const
from src.Board import Board


class Match():
    """Logic of connect4 ongoing match"""

    def __init__(self, first_player=const.PlayerTurn.RED) -> None:
        """Constructor"""
        self.board = Board()
        self.column_selected = 0
        self.state = const.MatchState.PLAYING
        self.player_turn = first_player

    def add_checker(self):
        """Add checker of current player to currently selected column"""
        if self.player_turn == const.PlayerTurn.RED:
            self.board.add_checker_red(self.column_selected)
        else:
            self.board.add_checker_yellow(self.column_selected)

        if self.board.is_game_won():
            self.state = (
                const.MatchState.RED_WON
                if self.player_turn == const.PlayerTurn.RED else
                const.MatchState.YELLOW_WON)
        else:
            self._toggle_player()

    def column_next(self):
        """Change column selection to column immediately right"""
        increment = 1
        self._column_change(increment)

    def column_previous(self):
        """Change column selection to column immediately left"""
        increment = -1
        self._column_change(increment)

    def is_being_played(self):
        """Return if match is still ongoing"""
        return self.state == const.MatchState.PLAYING

    def _column_change(self, increment):
        """Change current column according to increment/offset"""
        self.column_selected += increment

        if self.column_selected == const.BOARD_TOTAL_COLUMNS:
            self.column_selected = 0
        elif self.column_selected < 0:
            self.column_selected = const.BOARD_TOTAL_COLUMNS - 1

        if self.board.columns[self.column_selected].is_full():
            self._column_change(increment)

    def _toggle_player(self):
        """Toggle current player"""
        self.player_turn = (
                const.PlayerTurn.RED
                if self.player_turn == const.PlayerTurn.YELLOW else
                const.PlayerTurn.YELLOW)
