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
    file_input = {"object": {"type": file_type}, "location": {"name": "test"}}
    gear_context = MagicMock()
    profile = MagicMock()
    _ = classify(file_input, gear_context, profile)
    adapt.assert_called_once_with(file_input, gear_context)
    adapt.return_value.classify.assert_called_once_with(profile)
    gear_context.metadata.add_qc_result.assert_called_once_with(
        file_input, "classification", "PASS"
    )
