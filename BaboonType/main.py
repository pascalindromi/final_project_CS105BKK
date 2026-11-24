from baboonmod import typingcore
from baboonmod import storage
from sys import exit
import os

target_text = "The quick brown fox jumps over the lazy dog."

current_storage = storage.Storage()

def display_menu():
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

def run_test(text):
    test = typingcore.TypingTest(text)

    results = test.run()
    
    if results == None:
        print("\nTest ended.")
        input("Press Enter to return to the main menu...")

    else:
        current_storage.add_result(results)
        print("\nTest finished!")
        print(f"Your input: {results['typed_text']}")
        print(f"Total mistakes: {results['total_mistakes']} ")
        print(f"Elapsed time: {results['elapsed']:.2f}s")
        print(f"WPM: {results['WPM']:.0f} words per minute")
        print(f"Accuracy: {results['accuracy']:.0f}%")
        input("Press Enter to return to the main menu...")


def show_stats():
    tests_per_page = 10
    current_page = 0

    while True:
        results = current_storage.load_results()
        total_pages = max(1, (len(results) + tests_per_page - 1) // tests_per_page)
        start_index = current_page * tests_per_page
        end_index = start_index + tests_per_page

        page_results = results[start_index:end_index]

        print("\n\n\n-------------------------------------------------------")
        print("-------------------TEST HISTORY------------------------")
        print("-------------------------------------------------------")

        if not results:
            print("             No typing tests recorded yet.")

        else:
            for result in page_results:
                print(
                    f"{result['test_name']:<20} | "
                    f"{result['date']} {result['time']}"
                )

        print("-------------------------------------------------------")
        print(f"                           Page {current_page + 1}/{total_pages}")
        print("-------------------------------------------------------")
        print("[N] Next page    [P] Previous page    [Q] Quit")
        print("Type the name of the test to view the test information")
        print("        Type 'DEL' to delete all test data")

        choice = input("Enter your choice: ").strip().lower()

        if choice == "n" and current_page < total_pages - 1:
            current_page += 1

        elif choice == "p" and current_page > 0:
            current_page -= 1 #IMPLEMENT EXCEPTION HERE LATER.

        elif choice == "del":
            current_storage.clear_results()
            print("data deleted")

        elif choice in [result["test_name"] for result in results]:
            view_test(choice)

        elif choice == "q":
            break


def view_test(test_name):
    results = current_storage.load_results()

    # Find the requested test.
    selected_test = None

    for result in results:
        if result["test_name"] == test_name:
            selected_test = result
            break

    if selected_test is None:
        print("Test not found.")
        input("Press Enter to continue...")
        return

    # Display test information.
    print("-------------------------------------------------------")
    print("---------------------TEST DETAILS----------------------")
    print("-------------------------------------------------------")

    print(f"Test name:       {selected_test['test_name']}")
    print(f"Date:            {selected_test['date']}")
    print(f"Time:            {selected_test['time']}")
    print("-------------------------------------------------------")

    print(f"Your input:      {selected_test['typed_text']}")
    print(f"Total mistakes:  {selected_test['total_mistakes']}")
    print(f"Elapsed time:    {selected_test['elapsed']:.2f}s")
    print(f"WPM:             {selected_test['WPM']:.0f} words per minute")
    print(f"Accuracy:        {selected_test['accuracy']:.0f}%")

    print("-------------------------------------------------------")
    input("Press Enter to return to test records...")


if __name__ == "__main__":

    while True:
        display_menu()
        option = int(input())
        if option == 1:
           run_test(target_text)
        if option == 2:
           show_stats()
        if option == 3:
           pass
        if option == 4:
           display_about()
        if option == 5:
           exit()
            

            

    
    