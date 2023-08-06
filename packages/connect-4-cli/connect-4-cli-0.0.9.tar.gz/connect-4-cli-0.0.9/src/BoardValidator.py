import src.BoardValidatorColumns as BVC
import src.BoardValidatorRows as BVR
import src.BoardValidatorDiagonals as BVD


class BoardValidator():
    """Validates if board has a connect4 combination."""

    def __init__(self) -> None:
        """Constructor."""
        self.validator_columns = BVC.BoardValidatorColumns()
        self.validator_rows = BVR.BoardValidatorRows()
        self.validator_diagonals = BVD.BoardValidatorDiagonals()

    def game_won(self, columns):
        """Return if game is finished due to connect4 happening
        either with 4 in a column, or a row, or in diagonal."""
        return (
            self.validator_columns.connected_4_in_column(columns) or
            self.validator_rows.connected_4_in_row(columns) or
            self.validator_diagonals.connected_4_in_diagonal(columns)
            )
