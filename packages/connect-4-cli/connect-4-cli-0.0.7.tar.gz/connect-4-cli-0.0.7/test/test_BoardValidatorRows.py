import utility_MakeBoards as BoardMaker
import src.BoardValidatorRows as BVR


def test_game_won_with_column_of_reds():
    board = BoardMaker.make_board_won_with_row_of_reds()
    validator = BVR.BoardValidatorRows()

    assert(validator.connected_4_in_row(board.columns))


def test_game_won_with_column_of_yellows():
    board = BoardMaker.make_board_won_with_row_of_yellows()
    validator = BVR.BoardValidatorRows()

    assert(validator.connected_4_in_row(board.columns))
