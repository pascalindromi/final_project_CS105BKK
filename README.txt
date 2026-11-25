BaboonType
==========

BaboonType is a terminal typing-speed practice app. It presents a short passage
from Wikipedia, or a bundled local passage if Wikipedia cannot be reached. It
measures typing speed and accuracy, then saves completed test results for later
review. we're almost done! i just need to add some pytest, and actually make settings do something.
which is going to be even more modules! i think this project has too many modules but whatever.

Install the dependencies from the FINAL_PROJECT directory:

    python -m pip install -r requirements.txt

Then run the app from the BaboonType directory:

    python main.py

Modules | for the conveniece of those, who wants to look at the code of this project
=======

main.py
    Coordinates the menu, passage selection, typing test, and saving results.

baboonmod/typingcore.py
    Runs the interactive typing test and calculates WPM, mistakes, and accuracy.

baboonmod/passage.py
    Defines the Passage object and checks that its text is printable ASCII and
    no longer than 25 words.

baboonmod/storage.py
    Loads and saves typing-test results in data/results.json.

baboonmod/history.py
    Displays, handles pages, and deletes saved test history, and shows test details.

baboonmod/ui.py
    Displays the main menu, About screen, and passage source information.

baboonmod/exceptions.py
    Defines custom exceptions for invalid menu choices, page navigation, missing
    tests, and passage-provider errors.

provider/wikipedia_fetch.py
    Fetches a random Wikipedia article extract, limits it to 25 words, and
    returns its title, source URL, and license information.

provider/local_passages.py
    Selects a random passage from the bundled local passage collection.

data/passages.json
    Stores the local passages used when the Wikipedia source is unavailable.

data/results.json
    Stores completed typing-test results and their passage attribution.