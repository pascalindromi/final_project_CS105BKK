import pytest
from baboonmod.exceptions import StorageError
from baboonmod.storage import Storage


def valid_result(**overrides):
    result = {
        "test_name": "Sample",
        "date": "2026-01-02",
        "time": "03:04:05",
        "typed_text": "hello",
        "total_mistakes": 0,
        "elapsed": 2.5,
        "WPM": 24.0,
        "accuracy": 100.0,
    }
    result.update(overrides)
    return result


def test_missing_results_file_loads_as_empty_list(tmp_path):
    storage = Storage(tmp_path / "results.json")

    assert storage.load_results() == []


def test_saves_and_loads_results(tmp_path):
    storage = Storage(tmp_path / "results.json")
    results = [valid_result()]

    storage.save_results(results)

    assert storage.load_results() == results


def test_add_result_sets_timestamp_and_passage_name(tmp_path):
    storage = Storage(tmp_path / "results.json")
    result = {
        "passage_name": "Sample passage",
        "typed_text": "hello",
        "total_mistakes": 0,
        "elapsed": 2.5,
        "WPM": 24.0,
        "accuracy": 100.0,
    }

    storage.add_result(result)

    saved = storage.load_results()[0]
    assert saved["test_name"] == "Sample passage"
    assert saved["date"]
    assert saved["time"]
    assert saved["passage_name"] == "Sample passage"


def test_add_result_preserves_existing_history(tmp_path):
    storage = Storage(tmp_path / "results.json")
    previous = valid_result()
    storage.save_results([previous])
    new_result = {
        "passage_name": "Next",
        "typed_text": "next",
        "total_mistakes": 0,
        "elapsed": 1,
        "WPM": 60,
        "accuracy": 100,
    }

    storage.add_result(new_result)

    assert storage.load_results()[0] == previous
    assert len(storage.load_results()) == 2


def test_clear_results_removes_all_records(tmp_path):
    storage = Storage(tmp_path / "results.json")
    storage.save_results([valid_result()])

    storage.clear_results()

    assert storage.load_results() == []


def test_rejects_non_list_results_file(tmp_path):
    path = tmp_path / "results.json"
    path.write_text("{}", encoding="utf-8")
    storage = Storage(path)

    with pytest.raises(StorageError, match="must contain a list"):
        storage.load_results()


def test_rejects_non_object_result_record(tmp_path):
    storage = Storage(tmp_path / "results.json")

    with pytest.raises(StorageError, match="must be a JSON object"):
        storage.save_results(["not an object"])


def test_rejects_missing_required_field(tmp_path):
    storage = Storage(tmp_path / "results.json")
    result = valid_result()
    del result["accuracy"]

    with pytest.raises(StorageError, match="missing accuracy"):
        storage.save_results([result])


@pytest.mark.parametrize(
    ("field", "value"),
    [("total_mistakes", True), ("WPM", "fast")],
)
def test_rejects_invalid_required_field_values(tmp_path, field, value):
    storage = Storage(tmp_path / "results.json")

    with pytest.raises(StorageError, match=f"invalid {field}"):
        storage.save_results([valid_result(**{field: value})])


def test_rejects_non_string_optional_metadata(tmp_path):
    storage = Storage(tmp_path / "results.json")

    with pytest.raises(StorageError, match="invalid passage_title"):
        storage.save_results([valid_result(passage_title=12)])


def test_reports_corrupt_results_json(tmp_path):
    path = tmp_path / "results.json"
    path.write_text("{", encoding="utf-8")
    storage = Storage(path)

    with pytest.raises(StorageError, match="Could not read results"):
        storage.load_results()


@pytest.mark.parametrize("result", [None])
def test_add_result_requires_an_object(tmp_path, result):
    storage = Storage(tmp_path / "results.json")

    with pytest.raises(StorageError, match="must be a JSON object"):
        storage.add_result(result)


@pytest.mark.parametrize("passage_name", ["   ", 7])
def test_add_result_requires_nonblank_passage_name(tmp_path, passage_name):
    storage = Storage(tmp_path / "results.json")
    result = {"passage_name": passage_name}

    with pytest.raises(StorageError, match="must include a passage name"):
        storage.add_result(result)
