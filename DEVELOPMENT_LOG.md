
# Development Log

- the purpose of this md, is to show the gradual development progress for the baboontype program.

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

### Future work
- Consider adding automated tests if a custom typing input handler is developed.
- Test the Wikipedia provider against the live API before relying on it for a release.

### QUICK FIX BEFORE FINAL COMMIT
- Added `StorageError` and translated expected directory, read, write, decoding,
  and JSON-serialization failures into user-facing storage errors.
- Results JSON is checked for a list of records with the fields and value types
  used by history; invalid JSON is no longer silently treated as empty history.
- Results and local passage paths use `Path`; malformed local passage records
  are skipped with a warning, and the provider reports an error if no usable
  records remain.
- The main loop now catches storage failures and handles EOF/Ctrl+C at ordinary
  prompts without a traceback.
- Added a default passage-source setting and a persisted user setting; the
  Settings menu can select Wikipedia with local fallback or local-only mode.
- Added a persisted capitalization-matching setting, off by default, that can
  be toggled in Settings and controls both typing input and display feedback.
- Typing-test names now use passage names, and history uses 1–10 selections
  for the entries currently displayed. For a more intuitive approach.
- Added a custom `hidden_cursor` context manager so the terminal cursor is
  restored even when the typing application exits unexpectedly.
- Added docstrings across the whole project.

### FINAL DEVELOPMENT LOG

## 27 November 2026

### Completed
- Added five pytest modules under `test/` covering passages, settings, storage,
  typing behavior, and local passage loading, with 72 passing test cases.
- Added `pytest.ini` to configure test discovery and make the application
  modules importable when pytest runs from `FINAL_PROJECT`.
- Added `pytest` and `ruff` to `requirements.txt` alongside the existing
  runtime dependencies, and updated the test status in `REQUIREMENTS.md`.
- Removed previously tracked `.pyc` files from Git's index; existing
  `.gitignore` rules already exclude Python bytecode, while local copies remain.
- Removed the tracked local typing-results file from Git's index while
  preserving its local copy, and added Ruff's cache to `.gitignore`.
- Fixed accuracy reporting so repeated errors and backspaces cannot produce a
  negative score; added regression coverage and documented test/lint commands.
- Verified with `python -m pytest` (72 passed) and `python -m ruff check .`
  (passed).

