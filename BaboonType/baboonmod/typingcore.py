"""Implement the interactive typing test and live performance display."""

from contextlib import contextmanager
from math import ceil
from time import perf_counter

from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl


@contextmanager
def hidden_cursor():
    """Hide the terminal cursor for a block and restore it on exit."""
    print("\033[?25l", end="")
    try:
        yield
    finally:
        print("\033[?25h", end="")


class TypingTest:
    """Track typing input, mistakes, timing, and test completion."""

    def __init__(self, target_text, case_sensitive=False):
        """Initialize a test for a passage with the selected case behavior."""
        self.passage = target_text
        self.target_text = target_text.content
        self.case_sensitive = case_sensitive
        self.typed_text = ""
        self.total_mistakes = 0
        self.start_time = None
        self.completed = False
        self.input_ready = False
        self.countdown_end = 0.0

    def calculate_wpm(self, elapsed):
        """Calculate words per minute from the typed text and elapsed seconds."""
        minutes = elapsed / 60
        if minutes == 0:
            return 0

        return len(self.typed_text.split()) / minutes

    def characters_match(self, typed_character, target_character):
        """Compare two characters using the configured case sensitivity."""
        if self.case_sensitive:
            return typed_character == target_character
        return typed_character.casefold() == target_character.casefold()

    def calculate_accuracy(self):
        """Calculate the percentage of typed characters without mistakes."""
        if len(self.typed_text) == 0:
            return 0

        accuracy = (
            (len(self.typed_text) - self.total_mistakes) / len(self.typed_text)
        ) * 100

        return max(accuracy, 0)

    def get_display(self):
        """Generate the passage with colours and a live timer."""

        if self.start_time is None:
            remaining = self.countdown_end - perf_counter()
            if remaining > 0:
                return [("", f"Get ready to type...\n{ceil(remaining)}")]
            self.start_time = perf_counter()

        formatted_text = []

        formatted_text.append(("", "Type the passage below. Press Ctrl+C to quit.\n"))

        for index, character in enumerate(self.target_text):
            if index >= len(self.typed_text):
                style = "fg:#888888"

            elif self.characters_match(self.typed_text[index], character):
                style = "fg:#00cc66"

            else:
                style = "fg:#ff4444"

            formatted_text.append((style, character))

        elapsed = perf_counter() - self.start_time

        formatted_text.append(("", "\n\n"))
        formatted_text.append(("", f"Time: {elapsed:.1f}s "))
        formatted_text.append(("", f"Mistakes: {self.total_mistakes}\n"))
        formatted_text.append(("", f"WPM: {self.calculate_wpm(elapsed):.1f} "))
        formatted_text.append(
            ("", f"Accuracy: {self.calculate_accuracy():.0f}%")
        )

        return formatted_text

    def enable_input_after_render(self, app):
        """Enable key handling once the countdown has completed."""
        if self.start_time is not None and app.is_running:
            self.input_ready = True

    def handle_backspace(self, event):
        """Remove the most recent typed character when input is enabled."""
        if not self.input_ready:
            return
        self.typed_text = self.typed_text[:-1]
        event.app.invalidate()

    def handle_character(self, event):
        """Record a printable key and update mistake and completion state."""
        if not self.input_ready:
            return

        character = event.data

        if not character.isprintable():
            return

        if len(self.typed_text) >= len(self.target_text):
            return

        expected = self.target_text[len(self.typed_text)]

        if not self.characters_match(character, expected):
            self.total_mistakes += 1

        self.typed_text += character

        if len(self.typed_text) == len(self.target_text):
            self.completed = True
            event.app.exit()

        else:
            event.app.invalidate()

    def exit_application(self, event):
        """Exit the prompt application when the user requests cancellation."""
        event.app.exit()

    def run(self):
        """Initialize and run the typing test."""

        self.start_time = None
        self.input_ready = False
        self.countdown_end = perf_counter() + 3

        text_control = FormattedTextControl(self.get_display)

        window = Window(
            content=text_control,
            wrap_lines=True,
            always_hide_cursor=True,
        )

        kb = KeyBindings()

        kb.add("backspace")(self.handle_backspace)
        kb.add(Keys.Any)(self.handle_character)
        kb.add("c-c")(self.exit_application)

        app = Application(
            layout=Layout(window),
            key_bindings=kb,
            full_screen=True,
            refresh_interval=0.1,
            after_render=self.enable_input_after_render,
        )

        with hidden_cursor():
            app.run()

        if not self.completed:
            return None

        return {
            "typed_text": self.typed_text,
            "total_mistakes": self.total_mistakes,
            "elapsed": perf_counter() - self.start_time,
            "WPM": self.calculate_wpm(perf_counter() - self.start_time),
            "accuracy": self.calculate_accuracy(),
        }
