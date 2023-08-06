from src.constants import ValidUserInput as UserInput
from src.Game import Game
from src.Match import Match


def test_Game_construction():
    game = Game()
    assert(isinstance(game.match, Match))


def test_Game_inputs():
    game = Game()
    game.process_input(UserInput.ARROW_LEFT)
    game.process_input(UserInput.ARROW_RIGHT)
    game.process_input(UserInput.ENTER)
    game.process_input(UserInput.ENTER)
    game.process_input(UserInput.ARROW_RIGHT)
    game.process_input(UserInput.ENTER)
    game.process_input(UserInput.ENTER)
    game.process_input(UserInput.ARROW_RIGHT)
    game.process_input(UserInput.ENTER)
    game.process_input(UserInput.ENTER)
    game.process_input(UserInput.ARROW_RIGHT)
    assert(game._is_match_ongoing())

    game.process_input(UserInput.ENTER)
    assert not(game._is_match_ongoing())

    game.process_input(UserInput.ENTER)
    assert not(game._is_match_ongoing())

    game.process_input(UserInput.KEY_R)
    assert(game._is_match_ongoing())
