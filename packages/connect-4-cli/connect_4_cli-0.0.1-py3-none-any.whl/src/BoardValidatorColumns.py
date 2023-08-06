class BoardValidatorColumns():
    """Validates if a board column has a connect4 combination."""

    def connected_4_in_column(self, columns):
        """Return if any column of "columns" has a connect4 combination."""
        for col in columns:
            if self.column_has_4_consecutive_reds(col):
                return True
            if self.column_has_4_consecutive_yellows(col):
                return True
        return False

    def column_has_4_consecutive_reds(self, col):
        """Return if selected column has a connect4 combination
        with red checkers."""
        reds = col.indexes_rows_red()
        return self.column_has_4_consecutive_checkers(reds)

    def column_has_4_consecutive_yellows(self, col):
        """Return if selected column has a connect4 combination
        with yellow checkers."""
        yellows = col.indexes_rows_yellow()
        return self.column_has_4_consecutive_checkers(yellows)

    def column_has_4_consecutive_checkers(self, col):
        """Return if selected reduced column has a connect4 combination."""
        if len(col) >= 4:
            diffs = [(col[x+1] - col[x]) for x in range(len(col)-1)]
            for x in range(len(diffs)-2):
                if [diffs[x], diffs[x+1], diffs[x+2]] == [1, 1, 1]:
                    return True
        return False
