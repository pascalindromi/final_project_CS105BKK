from dataclasses import dataclass

from baboonmod.exceptions import UnsupportedPassageError


MAX_PASSAGE_WORDS = 25


@dataclass
class Passage:
    content: str
    title: str
    source_name: str
    source_url: str | None = None
    license_url: str | None = None

    def __post_init__(self):
        '''i wanted to use dataclass here because passage is a simple object, but i needed to also add a way to verify
        the passage content, hence i use __post_init__ to do so, so i can raise any exceptions if needed.'''
        
        if not isinstance(self.content, str):
            raise ValueError("passage content must be text")

        self.content = " ".join(self.content.split())

        if not self.content:
            raise ValueError("passage content cannot be empty")

        if not self.content.isascii() or not self.content.isprintable():
            raise UnsupportedPassageError("passage contains characters outside basic English text")

        if len(self.content.split()) > MAX_PASSAGE_WORDS:
            raise ValueError(f"passage cannot exceed {MAX_PASSAGE_WORDS} words")

    @property
    def word_count(self):
        return len(self.content.split())