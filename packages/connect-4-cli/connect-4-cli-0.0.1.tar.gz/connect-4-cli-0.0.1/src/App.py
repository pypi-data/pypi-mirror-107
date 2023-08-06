from src.PlayerInput import PlayerInput
from src.Game import Game
from src.ConsoleRenderer import ConsoleRenderer as Renderer
from src.constants import ValidUserInput as UserInput


class App():
    """Manage game loop of input -> process -> render."""

    def __init__(self) -> None:
        """Constructor."""

        self.input = PlayerInput()
        self.game = Game()
        self.renderer = Renderer()
        self.is_app_running = True

    def run(self):
        """Game loop."""

        while self.is_app_running:
            input_registered, key = self.input.wait_for_user_input()

            if input_registered:
                if self._is_user_quitting(key):
                    self._quit_game()
                else:
                    self.game.process_input(key)
                    self.renderer.render(self.game.match)

    def _is_user_quitting(self, key):
        return (key == UserInput.KEY_Q)

    def _quit_game(self):
        self.renderer.clear_console()
        self.is_app_running = False


if __name__ == "__main__":
    app = App()
    app.run()
