"""Provide validated passages from the local JSON collection."""

import json
import random
from pathlib import Path

from baboonmod.exceptions import PassageProviderError, UnsupportedPassageError
from baboonmod.passage import Passage


class LocalPassageProvider:
    """Load and randomly select a usable local passage."""

    def __init__(self, path=None):
        """Set the path to the local passage collection."""
        if path is None:
            path = Path(__file__).resolve().parents[1] / "data" / "passages.json"
        try:
            self.path = Path(path)
        except (TypeError, ValueError) as error:
            raise PassageProviderError(f"Invalid local passage path: {error}")

    def get_passage(self):
        """Return a random valid passage or raise an informative provider error."""
        try:
            with self.path.open("r", encoding="utf-8") as file:
                records = json.load(file)

        except (OSError, UnicodeError, ValueError) as error:
            raise PassageProviderError(
                f"Could not load local passages from {self.path}: {error}"
            )

        if not isinstance(records, list) or not records:
            raise PassageProviderError("The local passage file has no passages.")

        passages = []
        invalid_records = []

        for index, record in enumerate(records, start=1):
            if not isinstance(record, dict):
                invalid_records.append(str(index))
                continue

            passage_name = record.get("passage_name")
            if not isinstance(passage_name, str) or not passage_name.strip():
                invalid_records.append(str(index))
                continue

            content = record.get("content")
            if not isinstance(content, str):
                invalid_records.append(str(index))
                continue

            try:
                passage = Passage(
                    content=content,
                    title=passage_name,
                    source_name="Local passage collection",
                )
            except (ValueError, UnsupportedPassageError):
                invalid_records.append(str(index))
                continue

            passages.append(passage)

        if invalid_records:
            print(
                f"Warning: skipped invalid local passage record(s) {', '.join(invalid_records)} in {self.path}."
            )

        if not passages:
            raise PassageProviderError(f"No usable passages were found in {self.path}.")

        return random.choice(passages)
