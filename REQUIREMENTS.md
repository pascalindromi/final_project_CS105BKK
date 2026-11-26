# REQUIREMENTS STATUS

This project was made as a final project submission for the CS105BKK class at
Harbour.space@UTCC. Each item below describes how the current BaboonType
project addresses the requirement and notes any remaining gap.

1. **Runs (S5).** From a fresh clone with Python 3.12 or newer, `python main.py`
   or `python -m <package>` starts the app. The README explains how to run it
   on Windows and macOS.

   **Project integration:** Install dependencies from `FINAL_PROJECT` with
   `python -m pip install -r requirements.txt`, then run `python main.py` from
   `BaboonType`. `main.py` has an executable entry point.

   **Status: Met.** 

2. **Classes (S2-S4).** At least 3 classes, each with one clear job. Use a
   dataclass, `@property` or a dunder such as `__str__`. Use composition or
   inheritance where it fits.

   **Project integration:** `Passage` is a dataclass with a `word_count`
   property. `TypingTest` uses a `Passage`; `Storage`, `Settings`,
   `WikipediaProvider`, and `LocalPassageProvider` each handle a distinct part
   of the app.

   **Status: Met.**

3. **A package (S5).** A package folder with at least 2 modules and an
   `if __name__ == "__main__":` entry point.

   **Project integration:** `baboonmod` contains the app's modules, and
   `BaboonType/main.py` calls `main()` under the entry-point guard.

   **Status: Met.**

4. **Errors (S6).** Bad input or a missing or broken file should not crash the
   program with a traceback.

   **Project integration:** The app handles invalid menu/settings/history
   choices and EOF/Ctrl+C. Storage and settings convert expected file, JSON,
   and validation failures to readable errors. Passage providers report
   retrieval failures; invalid local passage records are skipped with a
   warning, and the app reports an error if no usable passage remains.

   **Status: Partially Met**
   Unexpected programming errors are still allowed to surface rather than
   being hidden by a broad exception handler.

5. **Files (S7).** Save data to CSV or JSON with `pathlib` and load it on the
   next run.

   **Project integration:** `Storage` reads and writes typing results in
   `data/results.json`; `Settings` persists passage-source and case-sensitivity
   preferences in `data/settings.json`; both use `pathlib`. Local passages and
   default settings are loaded from JSON files in `data`.

   **Status: Met.**

6. **Advanced Python (S9).** Write at least one generator, decorator, or
   context manager.

   **Project integration:** `typingcore.py` defines the custom `hidden_cursor`
   context manager. `TypingTest.run()` uses it around the typing application
   so the cursor is restored even if the application exits with an error.

   **Status: Met.**

7. **Tests (S10).** At least 8 pytest tests for normal cases, limits, and bad
   input; `python -m pytest` passes.

   **Project integration:** `test/` contains focused pytest modules for
   passages, settings, storage, typing behavior, and local passage loading.
   The suite has 72 tests total.

   **Status: Met.**

8. **Code quality and Git (S11).** PEP 8 names, docstrings, a `.gitignore`, and
   a clean `python -m ruff check .`. For an individual project, at least 5
   commits with clear messages. For a team, use branches, merge at least one
   pull request, and show each member's commits in the history.

   **Project integration:** The repository has a `.gitignore` and uses
   descriptive names, docstring coverage is complete, Ruff has
   been run and returns green. The current history has 7 commits.

   **Status: met**

9. **Bonus (S12).** Use one public API that needs no key and save a JSON copy
   of a reply so the program works offline.

   **Project integration:** `WikipediaProvider` retrieves article extracts
   from Wikipedia without an API key. If Wikipedia is unavailable, the app
   falls back to bundled `data/passages.json`; users can also select local-only
   mode. The app does not cache a JSON copy of a Wikipedia reply.

   **Status: Partially met.** 