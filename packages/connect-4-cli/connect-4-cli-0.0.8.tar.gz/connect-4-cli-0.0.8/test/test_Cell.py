import src.constants as const
import src.Cell as Cell


def test_Cell_construction():
    cell = Cell.Cell()
    assert (cell.current_state == const.CellState.EMPTY)
    assert (cell.is_empty())
    assert not (cell.is_red())
    assert not (cell.is_yellow())


def test_Cell_make_red():
    cell = Cell.Cell()
    cell.make_red()
    assert not (cell.is_empty())
    assert (cell.is_red())
    assert not (cell.is_yellow())


def test_Cell_make_yellow():
    cell = Cell.Cell()
    cell.make_yellow()
    assert not (cell.is_empty())
    assert not (cell.is_red())
    assert (cell.is_yellow())
