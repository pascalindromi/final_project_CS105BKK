class PageNavigationError(Exception):
    """Raised when a requested page does not exist."""


class TestNotFoundError(Exception):
    """Raised when a requested typing test is not in the saved history."""


class InvalidMenuOptionError(Exception):
    """Raised when the main menu input is not a valid option."""


class PassageProviderError(Exception):
    """Raised when a passage source cannot provide a usable passage."""


class UnsupportedPassageError(PassageProviderError):
    """Raised when a passage contains characters unsupported by English text input."""