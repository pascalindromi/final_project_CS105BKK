"""Application-specific exceptions for user input, data, and providers."""


class PageNavigationError(Exception):
    """Raised when a requested page does not exist."""


class TestNotFoundError(Exception):
    """Raised when a requested typing test is not in the saved history."""


class InvalidMenuOptionError(Exception):
    """Raised when the main menu input is not a valid option."""


class PassageProviderError(Exception):
    """Raised when a passage source cannot provide a usable passage."""


class StorageError(Exception):
    """Raised when saved typing-test data cannot be read or written."""


class SettingsError(Exception):
    """Raised when application settings cannot be read, validated, or saved."""


class UnsupportedPassageError(PassageProviderError):
    """Raised when a passage contains characters unsupported by English text input."""
