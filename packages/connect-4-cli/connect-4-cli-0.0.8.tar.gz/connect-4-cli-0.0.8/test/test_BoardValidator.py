import utility_MakeBoards as BoardMaker
import src.BoardValidator as BoardValidator
import src.Board as Board


def test_BoardValidator_construction():
    validator = BoardValidator.BoardValidator()

    board_empty = Board.Board()
    assert(not validator.game_won(board_empty.columns))


def test_BoardValidator_game_won_with_columns():
    validator = BoardValidator.BoardValidator()

    board_won_reds = BoardMaker.make_board_won_with_column_of_reds()
    assert(validator.game_won(board_won_reds.columns))

    board_won_yellows = BoardMaker.make_board_won_with_column_of_yellows()
    assert(validator.game_won(board_won_yellows.columns))


def test_BoardValidator_game_won_with_rows():
    validator = BoardValidator.BoardValidator()

    board_won_reds = BoardMaker.make_board_won_with_row_of_reds()
    assert(validator.game_won(board_won_reds.columns))

    board_won_yellows = BoardMaker.make_board_won_with_row_of_yellows()
    assert(validator.game_won(board_won_yellows.columns))


def test_BoardValidator_game_won_with_diagonals():
    validator = BoardValidator.BoardValidator()

    board_won_reds = (
        BoardMaker.make_board_won_with_diagonal_downwards_of_reds())
    assert(validator.game_won(board_won_reds.columns))

    board_won_yellows = (
        BoardMaker.make_board_won_with_diagonal_upwards_of_yellows())
    assert(validator.game_won(board_won_yellows.columns))
