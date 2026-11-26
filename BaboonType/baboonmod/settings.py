"""Load, validate, and persist user preferences."""

import json
from pathlib import Path

from baboonmod.exceptions import SettingsError

PASSAGE_SOURCES = ("wikipedia", "local")


class Settings:
    """Manage saved passage-source and typing preferences."""

    def __init__(self, path=None, default_path=None):
        """Load defaults and saved settings, creating or updating the file as needed."""
        self.data_dir = Path(__file__).resolve().parents[1] / "data"

        try:
            self.path = self.make_path(path, self.data_dir / "settings.json")
            self.default_path = self.make_path(
                default_path,
                self.data_dir / "default_settings.json",
            )
        except (TypeError, ValueError) as error:
            raise SettingsError(f"Invalid settings-file path: {error}")

        try:
            defaults = self.read_json(self.default_path)
        except FileNotFoundError:
            raise SettingsError(
                f"Default settings file was not found: {self.default_path}"
            )

        self.validate(defaults, self.default_path)

        try:
            saved_values = self.read_json(self.path)
        except FileNotFoundError:
            values = defaults.copy()
            self.write_json(values)
        else:
            if not isinstance(saved_values, dict):
                self.validate(saved_values, self.path)

            values = defaults.copy()
            values.update(saved_values)
            self.validate(values, self.path)

            if values != saved_values:
                self.write_json(values)

        self.validate(values, self.path)
        self._values = values

    def make_path(self, path, default_path):
        """Resolve a settings-file path relative to the data directory."""
        if path is None:
            return default_path

        path = Path(path)

        return (self.data_dir / path).resolve()

    def read_json(self, path):
        """Read a JSON settings file and report file or decoding errors."""
        try:
            with path.open("r", encoding="utf-8") as file:
                return json.load(file)

        except FileNotFoundError:
            raise

        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise SettingsError(f"Could not read settings from {path}: {error}")

    def validate(self, values, path):
        """Check that the required settings have supported values."""
        if not isinstance(values, dict):
            raise SettingsError(f"Settings in {path} must be a JSON object.")

        source = values.get("passage_source")
        if not isinstance(source, str) or source not in PASSAGE_SOURCES:
            raise SettingsError(
                f"Settings in {path} must set passage_source to 'wikipedia' or 'local'."
            )

        case_sensitive = values.get("case_sensitive")
        if not isinstance(case_sensitive, bool):
            raise SettingsError(
                f"Settings in {path} must set case_sensitive to true or false."
            )

    def write_json(self, values):
        """Persist settings as formatted JSON."""
        try:
            info = json.dumps(values, indent=4)
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("w", encoding="utf-8") as file:
                file.write(info)

        except (OSError, UnicodeError, TypeError, ValueError) as error:
            raise SettingsError(f"Could not save settings to {self.path}: {error}")

    @property
    def passage_source(self):
        """Return the configured passage source."""
        return self._values["passage_source"]

    def set_passage_source(self, source):
        """Validate and persist the selected passage source."""
        values = self._values.copy()
        values["passage_source"] = source
        self.validate(values, self.path)
        self.write_json(values)
        self._values = values

    @property
    def case_sensitive(self):
        """Return whether typing comparisons are case-sensitive."""
        return self._values["case_sensitive"]

    def set_case_sensitive(self, case_sensitive):
        """Validate and persist the case-sensitivity preference."""
        values = self._values.copy()
        values["case_sensitive"] = case_sensitive
        self.validate(values, self.path)
        self.write_json(values)
        self._values = values
