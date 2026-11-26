"""Coordinate the BaboonType application and its interactive menus."""

from baboonmod import history, storage, typingcore, ui
from baboonmod.exceptions import (
    InvalidMenuOptionError,
    PassageProviderError,
    SettingsError,
    StorageError,
)
from baboonmod.settings import Settings
from provider.local_passages import LocalPassageProvider
from provider.wikipedia_fetch import WikipediaProvider

wikipedia_provider = WikipediaProvider()
local_passage_provider = LocalPassageProvider()


def get_menu_option():
    """Read and validate a main-menu option."""
    entered = input().strip()
    try:
        option = int(entered)
    except ValueError:
        raise InvalidMenuOptionError("Please enter a number from 1 to 5.")

    if option not in [1, 2, 3, 4, 5]:
        raise InvalidMenuOptionError("Please enter a number from 1 to 5.")

    return option


def run_test(current_storage, current_settings):
    """Load a passage, run a typing test, and save completed results."""
    if current_settings.passage_source == "local":
        try:
            passage = local_passage_provider.get_passage()
        except PassageProviderError as error:
            print(f"Could not load a local passage: {error}")
            input("Press Enter to return to the main menu...")
            return
    else:
        try:
            passage = wikipedia_provider.get_passage()
        except PassageProviderError as wikipedia_error:
            try:
                passage = local_passage_provider.get_passage()
            except PassageProviderError as local_error:
                print("Could not load a passage from Wikipedia ")
                print(f"({wikipedia_error}) or locally ({local_error}).")
                input("Press Enter to return to the main menu...")
                return

            print(f"Wikipedia unavailable: {wikipedia_error}")
            print("Using a local passage instead.")

    ui.display_passage_source(passage)
    input("Press Enter to start the typing test...")

    test = typingcore.TypingTest(
        passage,
        case_sensitive=current_settings.case_sensitive,
    )
    results = test.run()

    if results is None:
        print("\nTest ended.")
        input("Press Enter to return to the main menu...")

    else:
        results.update(
            {
                "passage_name": passage.title,
                "passage_title": passage.title,
                "passage_source_name": passage.source_name,
                "passage_source_url": passage.source_url,
                "passage_license_url": passage.license_url,
            }
        )

        current_storage.add_result(results)
        print("\nTest finished!")
        print(f"Your input: {results['typed_text']}")
        print(f"Total mistakes: {results['total_mistakes']} ")
        print(f"Elapsed time: {results['elapsed']:.2f}s")
        print(f"WPM: {results['WPM']:.0f} words per minute")
        print(f"Accuracy: {results['accuracy']:.0f}%")
        ui.display_passage_source(passage)
        input("Press Enter to return to the main menu...")


def run_settings(current_settings):
    """Show the settings menu and persist the chosen preference."""
    while True:
        choice = ui.display_settings(
            current_settings.passage_source,
            current_settings.case_sensitive,
        )

        if choice == "1":
            source = "wikipedia"
        elif choice == "2":
            source = "local"
        elif choice == "3":
            case_sensitive = not current_settings.case_sensitive
            current_settings.set_case_sensitive(case_sensitive)
            if case_sensitive:
                print("Case-sensitive typing enabled.")
            else:
                print("Case-sensitive typing disabled.")
            input("Press Enter to return to the main menu...")
            return
        elif choice == "4":
            return
        else:
            print("Please choose 1, 2, 3, or 4.")
            input("Press Enter to try again...")
            continue

        current_settings.set_passage_source(source)
        if source == "wikipedia":
            print("Passage source set to Wikipedia with local fallback.")
        else:
            print("Passage source set to local only.")
        input("Press Enter to return to the main menu...")
        return


def main():
    """Initialize dependencies and run the main application loop."""
    try:
        current_storage = storage.Storage()
        current_settings = Settings()

    except (SettingsError, StorageError) as error:
        print(f"Could not initialize application data: {error}")
        return

    try:
        while True:
            ui.display_menu()
            try:
                option = get_menu_option()
            except InvalidMenuOptionError as error:
                print(error)
                input("Press Enter to try again...")
                continue

            try:
                if option == 1:
                    run_test(current_storage, current_settings)
                elif option == 2:
                    history.show_stats(current_storage)
                elif option == 3:
                    run_settings(current_settings)
                elif option == 4:
                    ui.display_about()
                elif option == 5:
                    return
            except (SettingsError, StorageError) as error:
                print(f"Could not access saved application data: {error}")
                input("Press Enter to return to the main menu...")
    except (EOFError, KeyboardInterrupt):
        print("\nExiting BaboonType.")


if __name__ == "__main__":
    main()
