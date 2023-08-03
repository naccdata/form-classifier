"""Module to test utils.py"""

from unittest.mock import MagicMock

import pytest
import yaml

from fw_gear_file_classifier.utils import (
    compare_dict,
    get_schema_definition,
    is_modality_defined,
    validate_modality_schema,
)


@pytest.fixture
def sample_profile(tmp_path):
    profile_data = {"key1": "value1", "key2": "value2", "key3": "value3"}
    profile_path = tmp_path / "sample_profile.yaml"
    with open(profile_path, "w", encoding="utf8") as file:
        yaml.dump(profile_data, file)

    return profile_path


def test_read_profile(sample_profile):
    yaml_dict = get_schema_definition(sample_profile)
    assert yaml_dict == {"key1": "value1", "key2": "value2", "key3": "value3"}


@pytest.mark.parametrize(
    "dict1, dict2, expected",
    [
        ({"a": [1], "b": [2], "c": [3, 4]}, {"a": [1], "b": [2], "c": [3, 4]}, True),
        ({"a": [1], "b": [2], "c": [3, 4]}, {"a": [1], "b": [2], "c": [3]}, False),
    ],
)
def test_compare_dict(dict1, dict2, expected):
    assert compare_dict(dict1, dict2) is expected


def test_is_modality_defined():
    client = MagicMock()
    client.get_all_modalities.return_value = [
        MagicMock(id="modality1"),
        MagicMock(id="modality2"),
    ]
    assert is_modality_defined(client, "modality1") is True
    assert is_modality_defined(client, "modality3") is False


def test_validate_modality_schema_exits_if_modality_not_defined(mocker):
    client = MagicMock()
    file_obj = {"object": {"type": "dicom"}, "modality": "modality3"}
    mock_is_modality_defined = mocker.patch(
        "fw_gear_file_classifier.utils.is_modality_defined"
    )
    mock_is_modality_defined.return_value = False

    with pytest.raises(SystemExit):
        validate_modality_schema(client, file_obj)


def test_validate_modality_schema_exits_if_modality_is_not_defined_in_schema(mocker):
    client = MagicMock()
    file_obj = {"object": {"type": "dicom"}, "modality": "modality3"}
    mock_is_modality_defined = mocker.patch(
        "fw_gear_file_classifier.utils.is_modality_defined"
    )
    mock_is_modality_defined.return_value = True

    mock_get_schema_definition = mocker.patch(
        "fw_gear_file_classifier.utils.get_schema_definition"
    )
    mock_get_schema_definition.return_value = {}

    with pytest.raises(SystemExit):
        validate_modality_schema(client, file_obj)


def test_validate_modality_schema_exits_if_modality_schema_does_not_match(mocker):
    client = MagicMock()
    client.get_modality.return_value = {
        "id": "modality1",
        "classification": {"key1": "value1"},
    }
    file_obj = {"object": {"type": "dicom"}, "modality": "modality1"}
    mock_is_modality_defined = mocker.patch(
        "fw_gear_file_classifier.utils.is_modality_defined"
    )
    mock_is_modality_defined.return_value = True
    mock_get_schema_definition = mocker.patch(
        "fw_gear_file_classifier.utils.get_schema_definition"
    )
    mock_get_schema_definition.return_value = {"modality1": {"key1": "value2"}}

    with pytest.raises(SystemExit):
        validate_modality_schema(client, file_obj)


def test_validate_modality_schema_when_all_matches(mocker, caplog):
    client = MagicMock()
    caplog.set_level("INFO")
    client.get_modality.return_value = {
        "id": "modality1",
        "classification": {"key1": "value1"},
    }
    file_obj = {"object": {"type": "dicom"}, "modality": "modality1"}
    mock_is_modality_defined = mocker.patch(
        "fw_gear_file_classifier.utils.is_modality_defined"
    )
    mock_is_modality_defined.return_value = True
    mock_get_schema_definition = mocker.patch(
        "fw_gear_file_classifier.utils.get_schema_definition"
    )
    mock_get_schema_definition.return_value = {"modality1": {"key1": "value1"}}

    validate_modality_schema(client, file_obj)

    assert "Modality schema is valid" in caplog.text
