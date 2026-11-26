import pytest
from baboonmod.exceptions import UnsupportedPassageError
from baboonmod.passage import MAX_PASSAGE_WORDS, Passage


def test_normalizes_whitespace():
    passage = Passage("  A  short\n passage\t here. ", "title", "source")

    assert passage.content == "A short passage here."


def test_word_count_uses_normalized_content():
    passage = Passage("one   two\nthree", "title", "source")

    assert passage.word_count == 3


def test_optional_source_metadata_defaults_to_none():
    passage = Passage("Text.", "title", "source")

    assert passage.source_url is None
    assert passage.license_url is None


def test_preserves_supplied_source_metadata():
    passage = Passage("Text.", "title", "source", "https://example.test", "license")

    assert passage.source_url == "https://example.test"
    assert passage.license_url == "license"


@pytest.mark.parametrize("content", ["", " ", "\n\t"])
def test_rejects_empty_content(content):
    with pytest.raises(ValueError, match="cannot be empty"):
        Passage(content, "title", "source")


def test_rejects_non_string_content():
    with pytest.raises(TypeError, match="must be text"):
        Passage(None, "title", "source")


@pytest.mark.parametrize("content", ["caf\u00e9", "hello \u4e16\u754c"])
def test_rejects_non_ascii_content(content):
    with pytest.raises(UnsupportedPassageError):
        Passage(content, "title", "source")


def test_rejects_non_printable_content():
    with pytest.raises(UnsupportedPassageError):
        Passage("hello\x00world", "title", "source")


def test_accepts_passage_at_word_limit():
    passage = Passage("word " * (MAX_PASSAGE_WORDS - 1) + "word", "title", "source")

    assert passage.word_count == MAX_PASSAGE_WORDS


def test_rejects_passage_over_word_limit():
    content = "word " * MAX_PASSAGE_WORDS + "word"

    with pytest.raises(ValueError, match="cannot exceed"):
        Passage(content, "title", "source")
