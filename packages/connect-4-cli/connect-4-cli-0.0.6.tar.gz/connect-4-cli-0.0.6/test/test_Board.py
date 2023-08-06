import src.Board as Board


def test_Board_construction():
    board = Board.Board()
    assert(board.columns_total == 7)
    assert(len(board.columns) == board.columns_total)


def test_add_checker_win_game_red():
    board = Board.Board()

    board.add_checker_red(0)
    board.add_checker_yellow(1)
    board.add_checker_red(0)
    board.add_checker_yellow(2)
    board.add_checker_red(0)
    board.add_checker_yellow(3)
    assert(not board.is_game_won())

    board.add_checker_red(0)
    assert(board.is_game_won())


def test_add_checker_win_game_yellow():
    board = Board.Board()

    board.add_checker_red(0)
    board.add_checker_yellow(1)
    board.add_checker_red(0)
    board.add_checker_yellow(2)
    board.add_checker_red(0)
    board.add_checker_yellow(3)
    board.add_checker_red(1)
    assert(not board.is_game_won())

    board.add_checker_yellow(4)
    assert(board.is_game_won())
