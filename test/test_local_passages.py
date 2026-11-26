import json

import pytest
from baboonmod.exceptions import PassageProviderError
from provider.local_passages import LocalPassageProvider


@pytest.fixture
def passage_path(tmp_path):
    return tmp_path / "passages.json"


@pytest.fixture
def write_passages(passage_path):
    def write(records):
        passage_path.write_text(json.dumps(records), encoding="utf-8")
        return passage_path

    return write


@pytest.fixture
def choose_first_passage(monkeypatch):
    monkeypatch.setattr("provider.local_passages.random.choice", lambda items: items[0])


def test_returns_valid_passage_from_collection(write_passages, choose_first_passage):
    path = write_passages(
        [{"passage_name": "Example", "content": "A short passage."}]
    )

    passage = LocalPassageProvider(path).get_passage()

    assert passage.title == "Example"
    assert passage.content == "A short passage."
    assert passage.source_name == "Local passage collection"


def test_normalizes_passage_content(write_passages, choose_first_passage):
    path = write_passages(
        [{"passage_name": "Example", "content": "One  two\nthree"}]
    )

    passage = LocalPassageProvider(path).get_passage()

    assert passage.content == "One two three"


def test_chooses_from_only_valid_records(write_passages, choose_first_passage):
    path = write_passages(
        [
            {"passage_name": "", "content": "Invalid"},
            {"passage_name": "Good", "content": "Valid text."},
        ],
    )

    passage = LocalPassageProvider(path).get_passage()

    assert passage.title == "Good"


def test_warns_when_invalid_records_are_skipped(
    write_passages, choose_first_passage, capsys
):
    path = write_passages(
        [
            None,
            {"passage_name": "Good", "content": "Valid text."},
        ],
    )

    LocalPassageProvider(path).get_passage()

    assert "skipped invalid local passage record(s) 1" in capsys.readouterr().out


@pytest.mark.parametrize("records", [[], {}, None])
def test_rejects_empty_or_non_list_collection(write_passages, records):
    path = write_passages(records)

    with pytest.raises(PassageProviderError, match="no passages"):
        LocalPassageProvider(path).get_passage()


def test_reports_missing_collection_file(passage_path):
    with pytest.raises(PassageProviderError, match="Could not load local passages"):
        LocalPassageProvider(passage_path).get_passage()


def test_reports_invalid_json(passage_path):
    passage_path.write_text("{", encoding="utf-8")

    with pytest.raises(PassageProviderError, match="Could not load local passages"):
        LocalPassageProvider(passage_path).get_passage()


@pytest.mark.parametrize(
    "record",
    [
        "not an object",
        {"content": "Missing a name"},
        {"passage_name": "Bad content", "content": 10},
        {"passage_name": "Blank", "content": "  "},
        {"passage_name": "Too long", "content": "word " * 26},
        {"passage_name": "Unsupported", "content": "caf\u00e9"},
    ],
)
def test_rejects_collection_with_no_usable_records(write_passages, record):
    path = write_passages([record])

    with pytest.raises(PassageProviderError, match="No usable passages"):
        LocalPassageProvider(path).get_passage()
