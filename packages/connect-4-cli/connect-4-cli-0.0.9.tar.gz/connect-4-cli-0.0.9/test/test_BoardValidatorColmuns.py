import utility_MakeBoards as BoardMaker
import src.BoardValidatorColumns as BVC


def test_game_won_with_column_of_reds():
    board = BoardMaker.make_board_won_with_column_of_reds()
    validator = BVC.BoardValidatorColumns()
    for x in range(len(board.columns)):
        assert(
            not validator.column_has_4_consecutive_yellows(board.columns[x]))

    reds = board.columns[5].indexes_rows_red()
    assert(validator.column_has_4_consecutive_checkers(reds))

    assert(not validator.column_has_4_consecutive_reds(board.columns[0]))
    assert(not validator.column_has_4_consecutive_reds(board.columns[1]))
    assert(not validator.column_has_4_consecutive_reds(board.columns[2]))
    assert(not validator.column_has_4_consecutive_reds(board.columns[3]))
    assert(not validator.column_has_4_consecutive_reds(board.columns[4]))
    assert(validator.column_has_4_consecutive_reds(board.columns[5]))

    assert(validator.connected_4_in_column(board.columns))


def test_game_won_with_column_of_yellows():
    board = BoardMaker.make_board_won_with_column_of_yellows()
    validator = BVC.BoardValidatorColumns()
    for x in range(len(board.columns)):
        assert(not(validator.column_has_4_consecutive_reds(board.columns[x])))

    yellows = board.columns[3].indexes_rows_yellow()
    assert(validator.column_has_4_consecutive_checkers(yellows))

    assert(not validator.column_has_4_consecutive_yellows(board.columns[0]))
    assert(not validator.column_has_4_consecutive_yellows(board.columns[1]))
    assert(not validator.column_has_4_consecutive_yellows(board.columns[2]))
    assert(validator.column_has_4_consecutive_yellows(board.columns[3]))
    assert(not validator.column_has_4_consecutive_yellows(board.columns[4]))
    assert(not validator.column_has_4_consecutive_yellows(board.columns[5]))

    assert(validator.connected_4_in_column(board.columns))
