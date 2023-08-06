from src.constants import ValidUserInput as UserInput
try:
    from pynput import keyboard
except ImportError:  # pragma: no cover
    class pyinput():  # pragma: no cover
        keyboard = 0  # pragma: no cover


class PlayerInput():
    """Detect and process player input from keyboard"""

    def __init__(self) -> None:
        """Constructor."""
        self._reset_object_vars()

    def wait_for_user_input(self, key_overwrite=None):
        """Wait for user input. Return tuple with key and flag
        to make other modules update"""

        self._reset_object_vars()

        # Collect events until released
        if key_overwrite:
            self._on_press(key_overwrite, key_overwrite)
        else:
            with keyboard.Listener(
                    on_press=self._on_press) as listener:  # pragma: no cover
                listener.join()  # pragma: no cover

        return (self.key_press_detected, self.key_pressed)

    def _on_press(self, key, key_override=None):
        """Process user input and update object variables accordingly."""

        self.key_press_detected = True

        if key_override:
            self.key_pressed = key_override
            return False

        if "char" in dir(key):  # pragma: no cover
            # handle alphanumeric keys
            switcher = {
                "r": UserInput.KEY_R,
                "q": UserInput.KEY_Q
            }
            self.key_pressed = switcher.get(key.char, UserInput.OTHER)
        else:  # pragma: no cover
            # handle special keys
            switcher = {
                keyboard.Key.left: UserInput.ARROW_LEFT,
                keyboard.Key.right: UserInput.ARROW_RIGHT,
                keyboard.Key.enter: UserInput.ENTER,
            }
            self.key_pressed = switcher.get(key, UserInput.OTHER)

        # stop listener and exit loop
        return False  # pragma: no cover

    def _reset_object_vars(self):
        """Reset object variables back to default values"""

        self.key_press_detected = False
        self.key_pressed = UserInput.OTHER
