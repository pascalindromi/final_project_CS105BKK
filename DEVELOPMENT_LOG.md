
# Development Log

## 24 November 2026 

### Completed
- Implemented the core typing test functionality using `prompt_toolkit`.
- Converted `typingcore`'s functionality into a class.
- Integrated the terminal-based typing interface.
- Added real-time character highlighting to indicate correct and incorrect input.
- Implemented elapsed time and mistake tracking.
- Added WPM and accuracy calculations.
- Refactored the typing test logic into a `TypingTest` class.
- Implemented JSON-based result storage through a dedicated `Storage` class.
- Added automatic test identification (`test1`, `test2`, etc.) and date/time recording.
- Implemented functionality to save, load, and clear typing test records.
- Added a test history interface with pagination (10 records per page).
- Implemented individual test result viewing.
- Adjusted the storage file path to keep `data/results.json` alongside `main.py`.
- Tested the typing interface and adjusted text wrapping.

### Planned at the time
- Add automated tests using `pytest`.
- Create test fixtures to simulate different typing speeds and typing behaviour.
- Explore API integration for retrieving typing passages.
- Find a suitable way to retreive more sample target text / passages.
- Improve input validation and error handling.
- Complete project documentation.

## 26 November 2026

### Completed
- Added a `Passage` class that stores passage text and source information, limits passages to 25 words, and rejects text that cannot be typed with printable ASCII characters.
- Added a Wikipedia passage provider that requests a random article, limits the extract to 25 words, and keeps its title, source URL, and license information for attribution.
- Added retries when Wikipedia returns unsupported characters, plus a local passage provider that selects a passage from `data/passages.json` if the API is unavailable.
- Updated the typing test to use a `Passage` object, calculate WPM from whitespace-separated words, and finish after the full passage is typed even if mistakes were made.
- Moved history handling to `baboonmod/history.py` and menu, About, and passage-source displays to `baboonmod/ui.py`.
- Added custom exceptions for invalid menu choices, page navigation, missing tests, and passage-provider errors.
- Added a project `.gitignore` and `requirements.txt` for `prompt_toolkit` and `requests`.
- Updated `README.txt` with setup instructions and module descriptions.
- Deferred the automated test folder for now. Checked the local passage data and provider locally; no live Wikipedia API request was made.

### Comparison with the public GitHub version
Compared with the public repository at [pascalindromi/final_project_CS105BKK](https://github.com/pascalindromi/final_project_CS105BKK), HEAD `6d0910b` as checked on 26 November 2026, the hosted version is still the earlier implementation. It uses a fixed passage in `main.py`, keeps history and display functions there, and estimates WPM from character count. The local working version adds passage providers, local fallback passages, source attribution, the `Passage` class, separate history and UI modules, and word-based WPM. These local changes are not yet reflected in that GitHub version.

### Future work
- Consider adding automated tests if a custom typing input handler is developed.
- Test the Wikipedia provider against the live API before relying on it for a release.
