"""Display and navigate saved typing-test results."""

from baboonmod.exceptions import PageNavigationError, TestNotFoundError


def show_stats(current_storage):
    """Show paginated test history and handle history actions."""
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
            for selection, result in enumerate(page_results, start=1):
                print(
                    f"{selection}. {get_test_name(result):<35} | "
                    f"{result['date']} {result['time']}"
                )

        print("-------------------------------------------------------")
        print(f"                           Page {current_page + 1}/{total_pages}")
        print("-------------------------------------------------------")
        print("[N] Next page    [P] Previous page    [Q] Quit")
        print("Enter a number from 1 to 10 to view a test.")
        print("        Type 'DEL' to delete all test data")

        choice = input("Enter your choice: ").strip().lower()

        if choice == "n" or choice == "p":
            try:
                if choice == "n":
                    if current_page >= total_pages - 1:
                        raise PageNavigationError("There is no next page.")
                    current_page += 1
                else:
                    if current_page <= 0:
                        raise PageNavigationError("There is no previous page.")
                    current_page -= 1
            except PageNavigationError as error:
                print(error)
                input("Press Enter to continue...")

        elif choice == "del":
            current_storage.clear_results()
            print("          DATA DELETED")
            input("Press anything to return to the main menu...")

        elif choice == "q":
            break

        elif choice.isdigit():
            try:
                view_test(int(choice), page_results)
            except TestNotFoundError as error:
                print(error)
                input("Press Enter to continue...")

        else:
            print("Enter a number from 1 to 10, N, P, Q, or DEL.")
            input("Press Enter to continue...")


def get_test_name(result):
    """Return the most descriptive available name for a test result."""
    return (
        result.get("passage_name") or result.get("passage_title") or result["test_name"]
    )


def view_test(selection, page_results):
    """Display the selected result from the current history page."""
    if not page_results:
        raise TestNotFoundError("There are no tests to select on this page.")

    if selection < 1 or selection > len(page_results):
        raise TestNotFoundError(
            f"Choose a test number from 1 to {len(page_results)} on this page."
        )

    selected_test = page_results[selection - 1]

    # Display test information.
    print("-------------------------------------------------------")
    print("---------------------TEST DETAILS----------------------")
    print("-------------------------------------------------------")

    print(f"Test name:       {get_test_name(selected_test)}")
    print(f"Date:            {selected_test['date']}")
    print(f"Time:            {selected_test['time']}")
    print("-------------------------------------------------------")

    print(f"Your input:      {selected_test['typed_text']}")
    print(f"Total mistakes:  {selected_test['total_mistakes']}")
    print(f"Elapsed time:    {selected_test['elapsed']:.2f}s")
    print(f"WPM:             {selected_test['WPM']:.0f} words per minute")
    print(f"Accuracy:        {selected_test['accuracy']:.0f}%")

    passage_title = selected_test.get("passage_title")
    if passage_title:
        print(f"Passage:         {passage_title}")
        source_url = selected_test.get("passage_source_url")
        if source_url:
            print(f"Source:          {source_url}")
            license_url = selected_test.get("passage_license_url")
            if license_url:
                print(f"License:         CC BY-SA 4.0 ({license_url})")
            print("                 Excerpt shortened for the typing test.")
        else:
            print(
                f"Source:          {selected_test.get('passage_source_name', 'Local collection')}"
            )

    print("-------------------------------------------------------")
    input("Press Enter to return to test records...")
