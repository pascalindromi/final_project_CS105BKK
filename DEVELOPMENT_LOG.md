
# Development Log

## 24 November 2026 

### Completed
- Implemented the core typing test functionality using `prompt_toolkit`.
- Converted typingcore's functionality into a class.
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

### Upcoming Work
- Add automated tests using `pytest`.
- Create test fixtures to simulate different typing speeds and typing behaviour.
- Explore API integration for retrieving typing passages.
- Find a suitable way to retreive more sample target text / passages.
- Improve input validation and error handling.
- Complete project documentation.
