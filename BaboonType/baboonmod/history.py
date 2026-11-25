from baboonmod.exceptions import PageNavigationError, TestNotFoundError


def show_stats(current_storage):
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

        else:
            try:
                view_test(choice, current_storage)
            except TestNotFoundError as error:
                print(error)
                input("Press Enter to continue...")


def view_test(test_name, current_storage):
    results = current_storage.load_results()

    # Find the requested test.
    selected_test = None

    for result in results:
        if result["test_name"] == test_name:
            selected_test = result
            break

    if selected_test is None:
        raise TestNotFoundError(f"No test named {test_name!r} was found.")

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