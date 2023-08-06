import re
from rich.console import Console
from src.ConsoleRenderer import ConsoleRenderer
from src.Match import Match
import src.constants as const
from utility_MakeBoards import make_board_almost_won_both as make_board


def test_ConsoleRenderer_construction():
    renderer = ConsoleRenderer()
    assert(isinstance(renderer.console, Console))
    assert(renderer.char_cell_empty)
    assert(renderer.char_cell_red)
    assert(renderer.char_cell_yellow)
    assert(renderer.board_for_print)
    assert(renderer.col_selection)
    assert not (renderer.print_buffer)


def test_update_board():
    renderer = ConsoleRenderer()
    match = Match()
    match.board = make_board()
    renderer._update_board_for_print(match.board.columns)
    assert(len(renderer.board_for_print[0]) == const.BOARD_TOTAL_COLUMNS)
    assert(
        len(renderer.board_for_print) == const.BOARD_TOTAL_ROWS_PER_COLUMN)
    assert(renderer.board_for_print[0][0] == renderer.char_cell_red)
    assert(
        renderer.board_for_print[0][1] == renderer.char_cell_yellow)
    assert(renderer.board_for_print[const.BOARD_TOTAL_ROWS_PER_COLUMN - 1][0]
           == renderer.char_cell_empty)


def test_update_column_selection():
    renderer = ConsoleRenderer()
    match = Match()
    renderer._update_column_selection_for_print(match)
    assert(len(renderer.col_selection) == const.BOARD_TOTAL_COLUMNS)
    assert(renderer.col_selection[0] == renderer.char_cell_red)
    for s in renderer.col_selection[1:]:
        assert(s == "  ")


def test_set_header():
    renderer = ConsoleRenderer()
    renderer._set_header()
    for i, line in enumerate(renderer.print_buffer):
        if i == 0 or 1 < i < 4 or i == len(renderer.print_buffer):
            assert(line == " ")
        else:
            assert(line)


def test_set_current_infos():
    renderer = ConsoleRenderer()
    match = Match()
    renderer._set_current_infos(match)
    assert(" " == renderer.print_buffer[0])
    assert("Turn for" in renderer.print_buffer[1])
    assert(" " == renderer.print_buffer[2])

    renderer._clear_buffer()
    match.state = const.MatchState.TIE
    renderer._set_current_infos(match)
    assert("tie" in renderer.print_buffer[1])

    renderer._clear_buffer()
    match.state = const.MatchState.RED_WON
    renderer._set_current_infos(match)
    assert("Victory" in renderer.print_buffer[1])

    renderer._clear_buffer()
    match.state = const.MatchState.YELLOW_WON
    renderer._set_current_infos(match)
    assert("Victory" in renderer.print_buffer[1])


def test_set_column_selector():
    renderer = ConsoleRenderer()
    match = Match()
    renderer._set_column_selector(match)
    assert(renderer.char_cell_red in renderer.print_buffer[0])
    assert(" " == renderer.print_buffer[-1])


def test_set_board():
    renderer = ConsoleRenderer()
    match = Match()
    renderer._set_board(match)
    assert(len(renderer.print_buffer) == const.BOARD_TOTAL_ROWS_PER_COLUMN)
    for i, row in enumerate(renderer.print_buffer):
        assert(renderer.char_cell_empty in row)
        assert not(renderer.char_cell_red in row)
        assert not(renderer.char_cell_yellow in row)


def test_set_tail():
    renderer = ConsoleRenderer()
    renderer._set_tail()
    assert(len(renderer.print_buffer) >= 3)


def test_print_buffer(capsys):
    renderer = ConsoleRenderer()
    renderer.print_buffer.append("This")
    renderer.print_buffer.append("is")
    renderer.print_buffer.append("a")
    renderer.print_buffer.append("test")
    renderer._print_buffer()

    # Capture stdout output
    captured = capsys.readouterr()
    assert(captured.out == "This\nis\na\ntest\n")


def test_render(capsys):
    renderer = ConsoleRenderer()
    match = Match()
    renderer.render(match)
    assert(len(renderer.print_buffer) >= 10)

    # Capture stdout output
    captured = capsys.readouterr()
    assert("\n" in captured.out)
    assert("Connect4" in captured.out)

    m = re.search(r"\](.)\[", renderer.char_cell_empty)
    found_string = m.group(1)
    assert(found_string in captured.out)
