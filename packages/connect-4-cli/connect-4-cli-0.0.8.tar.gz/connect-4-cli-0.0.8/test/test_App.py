import unittest.mock as mock
from time import sleep
from threading import Thread
from src.App import App
from src.ConsoleRenderer import ConsoleRenderer
from src.Game import Game
from src.PlayerInput import PlayerInput
from src.constants import ValidUserInput as UserInput


def test_App_construction():
    app = App()
    assert isinstance(app.input, PlayerInput)
    assert isinstance(app.game, Game)
    assert isinstance(app.renderer, ConsoleRenderer)
    assert (app.is_app_running)


def test_App_run():
    runs = 0
    keys = [UserInput.ARROW_LEFT, UserInput.KEY_Q]

    def mock_wait_user_input(self):
        return (True, keys[runs])

    patcher = mock.patch(
            'src.PlayerInput.PlayerInput.wait_for_user_input',
            mock_wait_user_input)
    patcher.start()

    app = App()
    assert app.is_app_running

    def force_stop_app_run(app):
        sleep(0.01)
        app.is_app_running = False
    x = Thread(target=force_stop_app_run, args=(app,))
    x.start()
    app.run()
    x.join()
    assert not app._is_user_quitting(keys[runs])

    runs += 1

    app.is_app_running = True
    app.run()
    assert app._is_user_quitting(keys[runs])
    assert not app.is_app_running

    patcher.stop()
