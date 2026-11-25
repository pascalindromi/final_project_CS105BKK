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


def display_passage_source(passage):
    print(f"\nPassage: {passage.title} ({passage.word_count} words)")
    if passage.source_url:
        print(f"Source: {passage.source_url}")
        print(f"License: CC BY-SA 4.0 ({passage.license_url})")
        print("This excerpt has been shortened for the typing test.")
    else:
        print(f"Source: {passage.source_name}")
