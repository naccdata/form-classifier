"""Module to test main.py"""
from unittest.mock import MagicMock

import pytest

from fw_gear_file_classifier.main import classify


@pytest.mark.parametrize(
    "to_mock, file_type",
    [
        ("fw_gear_file_classifier.main.NiftiFWAdapter", "nifti"),
        ("fw_gear_file_classifier.main.FWAdapter", "dicom"),
    ],
)
def test_classify_nifti(mocker, to_mock, file_type):
    adapt = mocker.patch(to_mock)
    add_qc = mocker.patch("fw_gear_file_classifier.main.add_qc_info")
    file_input = {"object": {"type": file_type}, "location": {"name": "test"}}
    gear_context = MagicMock()
    profile = MagicMock()
    _ = classify(file_input, gear_context, profile)
    adapt.assert_called_once_with(file_input, gear_context)
    adapt.return_value.classify.assert_called_once_with(profile)
    assert (gear_context, file_input) in add_qc.call_args
    gear_context.update_file_metadata.assert_called_once_with(
        "test", info=add_qc.return_value
    )
