from types import SimpleNamespace

import pytest
from baboonmod.passage import Passage
from baboonmod.typingcore import TypingTest, hidden_cursor


class FakeApp:
    def __init__(self):
        self.invalidations = 0
        self.exits = 0

    def invalidate(self):
        self.invalidations += 1

    def exit(self):
        self.exits += 1


def make_test(text="Hello world", case_sensitive=False):
    passage = Passage(text, "title", "source")
    return TypingTest(passage, case_sensitive=case_sensitive)


def event(data="x"):
    app = FakeApp()
    return SimpleNamespace(data=data, app=app)


def test_wpm_is_zero_for_zero_elapsed_time():
    typing_test = make_test()
    typing_test.typed_text = "one two"

    assert typing_test.calculate_wpm(0) == 0


def test_wpm_counts_typed_words_per_minute():
    typing_test = make_test()
    typing_test.typed_text = "one two three"

    assert typing_test.calculate_wpm(30) == 6


def test_accuracy_is_zero_when_no_characters_are_typed():
    assert make_test().calculate_accuracy() == 0


def test_accuracy_reflects_mistakes():
    typing_test = make_test()
    typing_test.typed_text = "abcd"
    typing_test.total_mistakes = 1

    assert typing_test.calculate_accuracy() == 75


def test_accuracy_does_not_go_below_zero_after_retries():
    typing_test = make_test("a")
    typing_test.typed_text = "a"
    typing_test.total_mistakes = 2

    assert typing_test.calculate_accuracy() == 0


def test_character_matching_ignores_case_by_default():
    assert make_test().characters_match("h", "H") is True


def test_character_matching_can_be_case_sensitive():
    assert make_test(case_sensitive=True).characters_match("h", "H") is False


def test_handle_character_does_nothing_before_input_is_ready():
    typing_test = make_test()
    input_event = event("A")

    typing_test.handle_character(input_event)

    assert typing_test.typed_text == ""
    assert typing_test.total_mistakes == 0
    assert input_event.app.invalidations == 0


def test_correct_character_is_recorded_and_refreshes_display():
    typing_test = make_test()
    typing_test.input_ready = True
    input_event = event("h")

    typing_test.handle_character(input_event)

    assert typing_test.typed_text == "h"
    assert typing_test.total_mistakes == 0
    assert input_event.app.invalidations == 1


def test_incorrect_character_increments_mistake_count():
    typing_test = make_test()
    typing_test.input_ready = True

    typing_test.handle_character(event("X"))

    assert typing_test.typed_text == "X"
    assert typing_test.total_mistakes == 1


def test_non_printable_character_is_ignored():
    typing_test = make_test()
    typing_test.input_ready = True

    typing_test.handle_character(event("\n"))

    assert typing_test.typed_text == ""
    assert typing_test.total_mistakes == 0


def test_backspace_removes_last_character_when_input_is_ready():
    typing_test = make_test()
    typing_test.input_ready = True
    typing_test.typed_text = "Hel"
    input_event = event()

    typing_test.handle_backspace(input_event)

    assert typing_test.typed_text == "He"
    assert input_event.app.invalidations == 1


def test_backspace_is_ignored_before_input_is_ready():
    typing_test = make_test()
    typing_test.typed_text = "He"

    typing_test.handle_backspace(event())

    assert typing_test.typed_text == "He"


def test_completing_passage_exits_application_and_ignores_extra_input():
    typing_test = make_test("Hi")
    typing_test.input_ready = True
    input_event = event("i")
    typing_test.typed_text = "H"

    typing_test.handle_character(input_event)
    typing_test.handle_character(event("!"))

    assert typing_test.completed is True
    assert typing_test.typed_text == "Hi"
    assert input_event.app.exits == 1


def test_hidden_cursor_is_restored_when_block_raises(capsys):
    with pytest.raises(RuntimeError, match="failure"), hidden_cursor():
        raise RuntimeError("failure")

    assert capsys.readouterr().out == "\033[?25l\033[?25h"
