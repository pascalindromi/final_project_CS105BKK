import json
import random
from pathlib import Path

from baboonmod.exceptions import PassageProviderError
from baboonmod.passage import Passage


class LocalPassageProvider:
    def __init__(self, path=None):
        if path is None:
            path = Path(__file__).resolve().parents[1] / "data" / "passages.json"
        self.path = path

    def get_passage(self):
        
        try:
            with self.path.open("r", encoding="utf-8") as file:
                records = json.load(file)

        except (OSError, UnicodeError, json.JSONDecodeError):
            raise PassageProviderError(f"Could not load local passages from {self.path}.")

        if not isinstance(records, list) or not records:
            raise PassageProviderError("The local passage file has no passages.")

        passages = []

        for index, record in enumerate(records, start=1):
            passage = Passage(
                content=record["content"],
                title=f"Local passage {index}",
                source_name="Local passage collection",
            )

            passages.append(passage)

        return random.choice(passages)
