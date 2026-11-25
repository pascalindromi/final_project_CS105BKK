from baboonmod import typingcore
from baboonmod import storage
from baboonmod import history
from baboonmod import ui
from baboonmod.exceptions import InvalidMenuOptionError, PassageProviderError
from provider.local_passages import LocalPassageProvider
from provider.wikipedia_fetch import WikipediaProvider
from sys import exit
import os

current_storage = storage.Storage()
wikipedia_provider = WikipediaProvider()
local_passage_provider = LocalPassageProvider()

def get_menu_option():
    entered = input().strip()
    try:
        option = int(entered)
    except ValueError:
        raise InvalidMenuOptionError("Please enter a number from 1 to 5.") 

    if option not in [1,2,3,4,5]:
        raise InvalidMenuOptionError("Please enter a number from 1 to 5.")

    return option


def run_test():
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

    test = typingcore.TypingTest(passage)
    results = test.run()
    
    if results == None:
        print("\nTest ended.")
        input("Press Enter to return to the main menu...")

    else:
        results.update({
            "passage_title": passage.title,
            "passage_source_name": passage.source_name,
            "passage_source_url": passage.source_url,
            "passage_license_url": passage.license_url,
        })

        current_storage.add_result(results)
        print("\nTest finished!")
        print(f"Your input: {results['typed_text']}")
        print(f"Total mistakes: {results['total_mistakes']} ")
        print(f"Elapsed time: {results['elapsed']:.2f}s")
        print(f"WPM: {results['WPM']:.0f} words per minute")
        print(f"Accuracy: {results['accuracy']:.0f}%")
        ui.display_passage_source(passage)
        input("Press Enter to return to the main menu...")


if __name__ == "__main__":

    while True:
        ui.display_menu()
        try:
            option = get_menu_option()
        except InvalidMenuOptionError as error:
            print(error)
            input("Press Enter to try again...")
            continue

        if option == 1:
           run_test()
        if option == 2:
           history.show_stats(current_storage)
        if option == 3:
           pass
        if option == 4:
           ui.display_about()
        if option == 5:
           exit()
            

            

    
    