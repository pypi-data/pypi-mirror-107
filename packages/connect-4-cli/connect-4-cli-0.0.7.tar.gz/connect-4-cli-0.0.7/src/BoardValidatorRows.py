import src.Column as Column
import src.BoardValidatorColumns as BVC


class BoardValidatorRows():
    """Validates if a board row has a connect4 combination."""

    def connected_4_in_row(self, columns):
        """Return if any row of "columns" has a connect4 combination."""
        rows_as_columns = self.columns_to_rows(columns)
        vali_columns = BVC.BoardValidatorColumns()
        return (vali_columns.connected_4_in_column(rows_as_columns))

    def columns_to_rows(self, columns):
        """Return rows as columns."""
        cols = []
        for r in range(len(columns[0].cells)):
            row = []
            for c in range(len(columns)):
                row.append(columns[c].cells[r])
            col = Column.Column()
            col.cells = row
            cols.append(col)
        return cols
