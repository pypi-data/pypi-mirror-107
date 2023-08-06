from src.constants import ValidUserInput as UserInput
from src.Match import Match


class Game():
    """Logic of connect4 game."""

    def __init__(self) -> None:
        """Constructor."""
        self.match = Match()

    def process_input(self, input):
        """Process user keyboard input after it was read and identified."""
        if input == UserInput.KEY_R:
            self._reset_match()
        elif self._is_match_ongoing():
            self._process_input_match(input)

    def _reset_match(self):
        """Create a new match in default state."""
        self.match = Match()

    def _is_match_ongoing(self):
        """Return if match is ongoing or stopped (player won or they tied)."""
        return self.match.is_being_played()

    def _process_input_match(self, input):
        """Process user input with ongoing match."""
        switcher = {
            UserInput.ARROW_LEFT: self.match.column_previous,
            UserInput.ARROW_RIGHT: self.match.column_next,
            UserInput.ENTER: self.match.add_checker
        }
        switcher.get(input, lambda: None)()
