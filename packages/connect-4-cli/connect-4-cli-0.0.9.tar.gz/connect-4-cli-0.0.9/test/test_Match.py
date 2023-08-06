import src.constants as const
import src.Match as Match
import utility_MakeBoards as BoardMaker


def test_Match_construction():
    match_default = Match.Match()
    assert(match_default.column_selected == 0)
    assert(match_default.state == const.MatchState.PLAYING)
    assert(match_default.player_turn == const.PlayerTurn.RED)

    match_other_player = Match.Match(const.PlayerTurn.YELLOW)
    assert(match_other_player.player_turn == const.PlayerTurn.YELLOW)


def test_column_changes_match_playing():
    match = Match.Match()
    match.board = BoardMaker.make_board_playing_with_full_columns()
    assert(match.column_selected == 0)

    match.column_next()
    assert(match.column_selected == 2)

    match.column_next()
    assert(match.column_selected == 3)

    match.column_next()
    assert(match.column_selected == 5)

    match.column_next()
    assert(match.column_selected == 6)

    match.column_next()
    assert(match.column_selected == 0)

    match.column_next()
    assert(match.column_selected == 2)

    match.column_previous()
    assert(match.column_selected == 0)

    match.column_previous()
    assert(match.column_selected == 6)

    match.column_previous()
    assert(match.column_selected == 5)

    match.column_previous()
    assert(match.column_selected == 3)

    match.column_previous()
    assert(match.column_selected == 2)

    match.column_previous()
    assert(match.column_selected == 0)


def test_add_checker_win_game_red():
    match = Match.Match()
    match.board = BoardMaker.make_board_almost_won_both()
    assert(match.state == const.MatchState.PLAYING)
    assert(match.is_being_played())
    assert(match.column_selected == 0)
    assert(match.player_turn == const.PlayerTurn.RED)

    match.add_checker()
    assert(match.state == const.MatchState.RED_WON)
    assert not(match.is_being_played())


def test_add_checker_win_game_yellow():
    match = Match.Match()
    match.board = BoardMaker.make_board_almost_won_both()
    assert(match.state == const.MatchState.PLAYING)
    assert(match.is_being_played())
    assert(match.column_selected == 0)
    assert(match.player_turn == const.PlayerTurn.RED)

    match.column_previous()
    assert(match.column_selected == 6)

    match.add_checker()
    assert(match.state == const.MatchState.PLAYING)
    assert(match.is_being_played())
    assert(match.player_turn == const.PlayerTurn.YELLOW)

    match.column_previous()
    assert(match.column_selected == 5)

    match.column_previous()
    assert(match.column_selected == 4)

    match.add_checker()
    assert(match.state == const.MatchState.YELLOW_WON)
    assert not(match.is_being_played())
