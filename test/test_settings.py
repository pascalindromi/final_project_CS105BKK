import json

import pytest
from baboonmod.exceptions import SettingsError
from baboonmod.settings import Settings


def write_json(path, value):
    path.write_text(json.dumps(value), encoding="utf-8")


def make_defaults(path, **overrides):
    values = {"passage_source": "local", "case_sensitive": False}
    values.update(overrides)
    write_json(path, values)


def test_missing_saved_file_is_created_from_defaults(tmp_path):
    defaults = tmp_path / "defaults.json"
    saved = tmp_path / "settings.json"
    make_defaults(defaults)

    settings = Settings(saved, defaults)

    assert settings.passage_source == "local"
    assert settings.case_sensitive is False
    assert json.loads(saved.read_text(encoding="utf-8")) == {
        "passage_source": "local",
        "case_sensitive": False,
    }


def test_loads_saved_settings(tmp_path):
    defaults = tmp_path / "defaults.json"
    saved = tmp_path / "settings.json"
    make_defaults(defaults)
    write_json(saved, {"passage_source": "wikipedia", "case_sensitive": True})

    settings = Settings(saved, defaults)

    assert settings.passage_source == "wikipedia"
    assert settings.case_sensitive is True


def test_saved_settings_are_merged_with_new_defaults(tmp_path):
    defaults = tmp_path / "defaults.json"
    saved = tmp_path / "settings.json"
    make_defaults(defaults, new_option="enabled")
    write_json(saved, {"passage_source": "local", "case_sensitive": True})

    settings = Settings(saved, defaults)

    assert settings.case_sensitive is True
    assert json.loads(saved.read_text(encoding="utf-8"))["new_option"] == "enabled"


def test_missing_defaults_file_raises_settings_error(tmp_path):
    with pytest.raises(SettingsError, match="Default settings file was not found"):
        Settings(tmp_path / "settings.json", tmp_path / "missing.json")


def test_invalid_saved_json_raises_settings_error(tmp_path):
    defaults = tmp_path / "defaults.json"
    saved = tmp_path / "settings.json"
    make_defaults(defaults)
    saved.write_text("{", encoding="utf-8")

    with pytest.raises(SettingsError, match="Could not read settings"):
        Settings(saved, defaults)


@pytest.mark.parametrize("values", [[], None])
def test_rejects_non_object_saved_settings(tmp_path, values):
    defaults = tmp_path / "defaults.json"
    saved = tmp_path / "settings.json"
    make_defaults(defaults)
    write_json(saved, values)

    with pytest.raises(SettingsError, match="must be a JSON object"):
        Settings(saved, defaults)


@pytest.mark.parametrize("source", ["remote", None])
def test_rejects_unsupported_passage_source(tmp_path, source):
    defaults = tmp_path / "defaults.json"
    make_defaults(defaults, passage_source=source)

    with pytest.raises(SettingsError, match="passage_source"):
        Settings(tmp_path / "settings.json", defaults)


@pytest.mark.parametrize("case_sensitive", [1, None])
def test_rejects_non_boolean_case_setting(tmp_path, case_sensitive):
    defaults = tmp_path / "defaults.json"
    make_defaults(defaults, case_sensitive=case_sensitive)

    with pytest.raises(SettingsError, match="case_sensitive"):
        Settings(tmp_path / "settings.json", defaults)


def test_setters_persist_values_for_next_instance(tmp_path):
    defaults = tmp_path / "defaults.json"
    saved = tmp_path / "settings.json"
    make_defaults(defaults)
    settings = Settings(saved, defaults)

    settings.set_passage_source("wikipedia")
    settings.set_case_sensitive(True)
    reloaded = Settings(saved, defaults)

    assert reloaded.passage_source == "wikipedia"
    assert reloaded.case_sensitive is True


def test_invalid_setter_does_not_change_saved_or_in_memory_value(tmp_path):
    defaults = tmp_path / "defaults.json"
    saved = tmp_path / "settings.json"
    make_defaults(defaults)
    settings = Settings(saved, defaults)
    original = saved.read_text(encoding="utf-8")

    with pytest.raises(SettingsError):
        settings.set_passage_source("unsupported")

    assert settings.passage_source == "local"
    assert saved.read_text(encoding="utf-8") == original


def test_invalid_settings_path_raises_settings_error(tmp_path):
    defaults = tmp_path / "defaults.json"
    make_defaults(defaults)

    with pytest.raises(SettingsError, match="Invalid settings-file path"):
        Settings(42, defaults)
