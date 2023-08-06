from src.constants import ValidUserInput as UserInput
from utility_InputKeyStrokes import simulate_key_press


def test_key_press_left():
    key = UserInput.ARROW_LEFT

    before, after, key_detected = simulate_key_press(key)
    assert not(before)
    assert(after)
    assert(key_detected == UserInput.ARROW_LEFT)


def test_key_press_right():
    key = UserInput.ARROW_RIGHT

    before, after, key_detected = simulate_key_press(key)
    assert not(before)
    assert(after)
    assert(key_detected == UserInput.ARROW_RIGHT)


def test_key_press_enter():
    key = UserInput.ENTER

    before, after, key_detected = simulate_key_press(key)
    assert not(before)
    assert(after)
    assert(key_detected == UserInput.ENTER)


def test_key_press_r():
    before, after, key_detected = simulate_key_press(UserInput.KEY_R)
    assert not(before)
    assert(after)
    assert(key_detected == UserInput.KEY_R)


def test_key_press_q():
    class key():
        char = "q"

    before, after, key_detected = simulate_key_press(UserInput.KEY_Q)
    assert not(before)
    assert(after)
    assert(key_detected == UserInput.KEY_Q)
