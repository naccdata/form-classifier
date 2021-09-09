"""Module to test parser.py"""
import logging
from unittest.mock import MagicMock

import pytest
from fw_classification.profiles import get_profile

from fw_gear_file_classifier.parser import parse_config


def test_parse_config_basic(mocker):
    profile_mock = mocker.patch("fw_gear_file_classifier.parser.Profile")
    gc = MagicMock()
    gc.get_input.return_value = None
    gc.get_input_path.return_value = None
    file_input, profile = parse_config(gc)
    get_input_args = gc.get_input.call_args_list
    assert get_input_args[0].args == ("file-input",)
    assert get_input_args[1].args == ("classifications",)
    profile_mock.assert_called_once_with(get_profile("main.yml"))
    assert file_input is None
    assert profile == profile_mock.return_value


def test_parse_config_custom_profile(mocker):
    profile_mock = mocker.patch("fw_gear_file_classifier.parser.Profile")
    gc = MagicMock()
    gc.get_input.return_value = None
    _ = parse_config(gc)
    profile_mock.assert_called_once_with(gc.get_input_path.return_value)


@pytest.mark.parametrize(
    "block_raw, err",
    [
        (
            [
                {
                    "match": [
                        {
                            "key": "file.info.header.dicom.SeriesDescription",
                            "is": "my-test-series-description",
                        }
                    ],
                    "action": [
                        {"key": "file.classification.Intent", "set": "Structural"},
                        {"key": "file.classification.Measurement", "set": "In-Plane"},
                    ],
                }
            ],
            False,
        ),
        (
            [
                {
                    "match": [
                        {
                            "key": "file.info.header.dicom.SeriesDescription",
                        }
                    ],
                }
            ],
            True,
        ),
        ("random test", True),
    ],
)
def test_parse_config_custom_block(mocker, block_raw, err, caplog):
    caplog.set_level(logging.WARNING)
    profile_mock = mocker.patch("fw_gear_file_classifier.parser.Profile")
    gc = MagicMock()
    gc.get_input.return_value = {"value": block_raw}
    _ = parse_config(gc)
    if err:
        assert caplog.record_tuples[-1][1] == 30
    else:
        profile_mock.return_value.handle_block.assert_called_once()
