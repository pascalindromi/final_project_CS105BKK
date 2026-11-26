"""Validate and persist typing-test result records."""

import json
from datetime import datetime
from pathlib import Path

from baboonmod.exceptions import StorageError


class Storage:
    """Read, update, and clear the saved typing-test results."""

    def __init__(self, filename="data/results.json"):
        """Set the results-file location and ensure its parent directory exists."""
        try:
            self.filename = Path(filename)
        except (TypeError, ValueError) as error:
            raise StorageError(f"Invalid results-file path: {error}")

        if not self.filename.is_absolute():
            base_dir = Path(__file__).resolve().parents[1]
            self.filename = base_dir / self.filename

        try:
            self.filename.parent.mkdir(parents=True, exist_ok=True)
        except (OSError, ValueError) as error:
            raise StorageError(
                f"Could not create results directory {self.filename.parent}: {error}"
            )

    def load_results(self):
        """Load and validate saved results, returning an empty list if absent."""
        try:
            with self.filename.open("r", encoding="utf-8") as file:
                results = json.load(file)
        except FileNotFoundError:
            return []
        except (OSError, UnicodeError, ValueError) as error:
            raise StorageError(f"Could not read results from {self.filename}: {error}")

        self._validate_results(results)
        return results

    def _validate_results(self, results):
        """Raise an error if results do not match the supported record format."""
        if not isinstance(results, list):
            raise StorageError("The results file must contain a list of test records.")

        required_fields = {
            "test_name": str,
            "date": str,
            "time": str,
            "typed_text": str,
            "total_mistakes": int,
            "elapsed": (int, float),
            "WPM": (int, float),
            "accuracy": (int, float),
        }

        optional_fields = (
            "passage_name",
            "passage_title",
            "passage_source_name",
            "passage_source_url",
            "passage_license_url",
        )

        for index, result in enumerate(results, start=1):
            if not isinstance(result, dict):
                raise StorageError(f"Results record {index} must be a JSON object.")

            for field, expected_type in required_fields.items():
                if field not in result:
                    raise StorageError(f"Results record {index} is missing {field}.")

                value = result[field]
                if isinstance(value, bool) or not isinstance(value, expected_type):
                    raise StorageError(
                        f"Results record {index} has an invalid {field} value."
                    )

            for field in optional_fields:
                value = result.get(field)

                if value is not None and not isinstance(value, str):
                    raise StorageError(
                        f"Results record {index} has an invalid {field} value."
                    )

    def save_results(self, results):
        """Validate and write all result records to disk."""
        self._validate_results(results)
        try:
            with self.filename.open("w", encoding="utf-8") as file:
                json.dump(results, file, indent=4)

        except (OSError, UnicodeError, TypeError, ValueError) as error:
            raise StorageError(f"Could not write results to {self.filename}: {error}")

    def add_result(self, result):
        """Add a result with its passage name and current date and time."""
        if not isinstance(result, dict):
            raise StorageError("A typing-test result must be a JSON object.")

        passage_name = result.get("passage_name")
        if not isinstance(passage_name, str) or not passage_name.strip():
            raise StorageError("A typing-test result must include a passage name.")

        results = self.load_results()

        timestamp = datetime.now()

        result["test_name"] = passage_name
        result["date"] = timestamp.strftime("%Y-%m-%d")
        result["time"] = timestamp.strftime("%H:%M:%S")

        results.append(result)

        self.save_results(results)

    def clear_results(self):
        """Remove all saved test records."""
        self.save_results([])
