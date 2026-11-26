BaboonType
==========

BaboonType is a terminal typing-speed practice app. Users can choose Wikipedia
passages, which fall back to bundled local passages if Wikipedia is unavailable,
or select local-only mode for offline use. Case-sensitive typing can also be
enabled in Settings; it is off by default. The app measures typing speed and
accuracy, then saves completed test results for later review.

Requirements
------------

Use Python 3.12 or newer.

Windows (PowerShell)
--------------------

From the FINAL_PROJECT directory:

    py -3.12 -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    cd BaboonType
    ..\.venv\Scripts\python.exe main.py

macOS (Terminal)
----------------

From the FINAL_PROJECT directory:

    python3.12 -m venv .venv
    ./.venv/bin/python -m pip install -r requirements.txt
    cd BaboonType
    ../.venv/bin/python main.py

If you have a newer Python version, use its version-specific launcher instead
(for example, `py -3.13` on Windows or `python3.13` on macOS).

Tests and lint
--------------

From the FINAL_PROJECT directory, run:

    python -m pytest
    python -m ruff check .

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
    Displays and deletes saved history; choose a test by its number on the page.

baboonmod/ui.py
    Displays the main menu, About screen, and passage source information.

baboonmod/settings.py
    Loads and saves the passage source and case-sensitive typing preference.

baboonmod/exceptions.py
    Defines custom exceptions for invalid menu choices, page navigation, missing
    tests, passage-provider errors, and settings errors.

provider/wikipedia_fetch.py
    Fetches a random Wikipedia article extract, limits it to 25 words, and
    returns its title, source URL, and license information.

provider/local_passages.py
    Selects a random passage from the bundled local passage collection.

data/passages.json
    Stores named local passages used when local-only mode is selected or
    Wikipedia is unavailable.

data/default_settings.json
    Supplies initial settings; the current defaults use local passages and
    case-insensitive typing.

data/settings.json
    Created on first launch to store the user's passage-source and
    case-sensitivity preferences.

data/results.json
    Stores completed typing-test results and their passage attribution.