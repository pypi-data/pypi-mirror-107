import src.Column as Column


def test_Column_construction():
    col = Column.Column()
    assert(col.rows_total == 6)
    assert(len(col.cells) == col.rows_total)
    assert(col.get_rows_empty() == col.rows_total)
    assert(col.get_rows_red() == 0)
    assert(col.get_rows_yellow() == 0)
    assert(not col.is_full())


def test_Column_add_checkers():
    col = Column.Column()
    assert(col.get_first_row_empty() == 0)
    assert(col.cells[0].is_empty())

    col.add_checker_red()
    assert(col.get_first_row_empty() == 1)
    assert(col.cells[0].is_red())

    col.add_checker_yellow()
    assert(col.get_first_row_empty() == 2)
    assert(col.cells[0].is_red())
    assert(col.cells[1].is_yellow())

    col.add_checker_red()
    assert(col.get_first_row_empty() == 3)
    assert(col.cells[0].is_red())
    assert(col.cells[1].is_yellow())
    assert(col.cells[2].is_red())


def test_Column_full_adding_checkers_ignored():
    col = Column.Column()
    assert(col.get_rows_empty() == 6)
    assert(not col.is_full())
    col.add_checker_yellow()
    col.add_checker_yellow()
    col.add_checker_yellow()
    col.add_checker_yellow()
    col.add_checker_yellow()
    col.add_checker_yellow()
    assert(col.is_full())
    assert(col.get_rows_empty() == 0)
    assert(col.get_rows_yellow() == 6)

    col.add_checker_yellow()
    assert(col.is_full())
    assert(col.get_rows_yellow() == 6)
    col.add_checker_red()
    assert(col.is_full())
    assert(col.get_rows_red() == 0)


def test_Column_indexes_rows():
    col = Column.Column()
    assert(col.indexes_rows_red() == [])
    col.add_checker_red()
    assert(col.indexes_rows_red() == [0])
    col.add_checker_red()
    assert(col.indexes_rows_red() == [0, 1])
    col.add_checker_yellow()
    assert(col.indexes_rows_yellow() == [2])
    col.add_checker_red()
    assert(col.indexes_rows_red() == [0, 1, 3])
