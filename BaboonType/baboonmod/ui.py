"""Render terminal menus, settings, and passage information."""

def display_menu():
    """Print the main menu."""
    print("\n\n\n")
    print("-------------------------------------------------------")
    print("--------------------BABOON-TYPE------------------------")
    print("-----------------1.run-typing-test---------------------")
    print("-----------------2.view-statistics---------------------")
    print("--------------------3.settings-------------------------")
    print("----------------------4.about--------------------------")
    print("----------------------5.exit---------------------------")
    print("-------------Enter-a-number-to-proceed-----------------")


def display_about():
    """Show application information and wait for the user to return."""
    print("\n\n\n")
    print("-------------------------------------------------------")
    print("----------------------ABOUT----------------------------")
    print("--------------------BABOON-TYPE------------------------")
    print("                                                       ")
    print("             A simple typing speed test                ")
    print("             application built with Python.             ")
    print("                                                       ")
    print("                  FEATURES                             ")
    print("             - Measure typing speed                    ")
    print("             - Track typing accuracy                   ")
    print("             - Review previous statistics              ")
    print("                                                       ")
    print("                  VERSION 0.67                          ")
    print("-------------------------------------------------------")
    input("Press Enter to return to the main menu...")


def display_passage_source(passage):
    """Display a passage and its source or license information."""
    print(f"\nPassage: {passage.title} ({passage.word_count} words)")
    if passage.source_url:
        print(f"Source: {passage.source_url}")
        print(f"License: CC BY-SA 4.0 ({passage.license_url})")
        print("This excerpt has been shortened for the typing test.")
    else:
        print(f"Source: {passage.source_name}")


def display_settings(passage_source, case_sensitive):
    """Display current preferences and return the user's menu choice."""
    print("\n\n\n")
    print("-------------------------------------------------------")
    print("----------------------SETTINGS-------------------------")
    if passage_source == "wikipedia":
        print("Current source: Wikipedia (uses local passages if unavailable)")
    else:
        print("Current source: Local passages only")
    if case_sensitive:
        print("Case-sensitive typing: On")
    else:
        print("Case-sensitive typing: Off")
    print("1. Use Wikipedia with local fallback")
    print("2. Use local passages only (offline)")
    print("3. Toggle case-sensitive typing")
    print("4. Return to the main menu")
    return input("Choose a setting: ").strip()
