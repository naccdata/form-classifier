"""Main module."""

from typing import Any, Dict
import logging

log = logging.getLogger(__name__)
from fw_classification.adapters import FWObject


def run(file_input: Dict[str, Any]) -> int:
    fw_adapter = FWObject(file_input)
    fw_adapter.run(profile)
