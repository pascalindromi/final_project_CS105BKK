from time import perf_counter

from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl


def run_typing_test(target_text):

    typed_text = ""
    total_mistakes = 0
    start_time = perf_counter()
    MAX_LENGTH = 80
    completed = False


    def get_display():
        """Generate the passage with colours and a live timer."""

        formatted_text = []

        for index, character in enumerate(target_text):

            if index > 0 and index % MAX_LENGTH == 0:
                formatted_text.append(("", "\n"))

            if index >= len(typed_text):
                style = "fg:#888888"

            elif typed_text[index].casefold() == character.casefold():
                style = "fg:#00cc66"

            else:
                style = "fg:#ff4444"

            formatted_text.append((style, character))

        elapsed = perf_counter() - start_time

        formatted_text.append(("", "\n\n"))
        formatted_text.append(("", f"Time: {elapsed:.1f}s"))
        formatted_text.append(("", f"   Mistakes: {total_mistakes}"))

        return formatted_text


    # Create the text display.
    text_control = FormattedTextControl(get_display)

    window = Window(content=text_control, wrap_lines=True)


    # Create keyboard bindings.
    kb = KeyBindings()


    @kb.add("backspace")
    def handle_backspace(event):
        """Remove the most recently typed character."""

        nonlocal typed_text

        typed_text = typed_text[:-1]
        event.app.invalidate()


    @kb.add(Keys.Any)
    def handle_character(event):
        """Process an individual character."""

        nonlocal typed_text, total_mistakes

        character = event.data

        if not character.isprintable():
            return

        if len(typed_text) >= len(target_text):
            return

        expected = target_text[len(typed_text)]

        if character.casefold() != expected.casefold():
            total_mistakes += 1

        typed_text += character

        if typed_text.casefold() == target_text.casefold():
            completed = True
            event.app.exit()

        else:
            event.app.invalidate()


    @kb.add("c-c")
    def exit_application(event):
        event.app.exit()
        

    app = Application(
        layout=Layout(window),
        key_bindings=kb,
        full_screen=True,
        refresh_interval=0.1,
    )

    print("Type the passage below. Press Ctrl+C to quit.")
    app.run()

    if not completed:
        return None

    return {
        "typed_text": typed_text,
        "total_mistakes": total_mistakes,
        "elapsed": perf_counter() - start_time,
    }