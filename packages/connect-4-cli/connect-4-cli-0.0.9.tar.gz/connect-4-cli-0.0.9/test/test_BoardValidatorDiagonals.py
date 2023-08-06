import utility_MakeBoards as BoardMaker
import src.Board as Board
import src.BoardValidatorDiagonals as BVD


def test_game_won_with_downwards_diagonal_of_reds():
    validator = BVD.BoardValidatorDiagonals()

    board_empty = Board.Board()
    assert not(validator.connected_4_in_diagonal(board_empty.columns))

    board_won = BoardMaker.make_board_won_with_diagonal_downwards_of_reds()
    assert(validator.connected_4_in_diagonal(board_won.columns))


def test_game_won_with_upwards_diagonal_of_yellows():
    validator = BVD.BoardValidatorDiagonals()

    board_empty = Board.Board()
    assert not(validator.connected_4_in_diagonal(board_empty.columns))

    board_won = BoardMaker.make_board_won_with_diagonal_upwards_of_yellows()
    assert(validator.connected_4_in_diagonal(board_won.columns))
