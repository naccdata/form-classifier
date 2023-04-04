"""Module to test parser.py"""
import logging
from pathlib import Path

import pytest

from nacc_gear_form_classifier.parser import parse_config


@pytest.fixture
def default_response(api, context_with_key):
    context_with_key.get_input.return_value = {
        "hierarchy": {"type": "acquisition", "id": 1}
    }
    api.add_response("/api/acquisitions/1", {"parents": {"project": 1}})
    api.add_response("/api/projects/1", {"info": {}, "label": "test"})
    return context_with_key, api


def test_parse_config_basic(mocker, default_response):
    profile_mock = mocker.patch("nacc_gear_form_classifier.parser.Profile")
    gc, _ = default_response
    gc.get_input_path.return_value = None
    _, profile = parse_config(gc)
    get_input_args = gc.get_input.call_args_list
    assert get_input_args[0].args == ("file-input",)
    profile_mock.assert_called_once_with(
        Path(__file__).parents[1]
        / "nacc_gear_form_classifier/classification_profiles/main.yml"
    )
    assert profile == profile_mock.return_value


def test_parse_config_custom_profile(mocker, default_response):
    profile_mock = mocker.patch("nacc_gear_form_classifier.parser.Profile")
    gc, _ = default_response
    _ = parse_config(gc)
    path = (
        Path(__file__).parents[1] / "nacc_gear_form_classifier/classification_profiles"
    )
    profile_mock.assert_called_once_with(
        gc.get_input_path.return_value, include_search_dirs=[path]
    )


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
def test_parse_config_custom_block(
    mocker, context_with_key, api, block_raw, err, caplog
):
    caplog.set_level(logging.WARNING)
    context_with_key.get_input.return_value = {
        "hierarchy": {"type": "acquisition", "id": 1}
    }
    api.add_response("/api/acquisitions/1", {"parents": {"project": 1}})
    api.add_response(
        "/api/projects/1", {"label": "test", "info": {"classifications": block_raw}}
    )
    profile_mock = mocker.patch("nacc_gear_form_classifier.parser.Profile")
    _ = parse_config(context_with_key)
    if err:
        assert caplog.record_tuples[-1][1] == 30
    else:
        profile_mock.return_value.handle_block.assert_called_once()
