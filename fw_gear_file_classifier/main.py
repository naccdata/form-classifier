"""Main module."""
from typing import Any, Dict, Optional
import logging
from pathlib import Path
import json

from flywheel_gear_toolkit import GearToolkitContext

from fw_classification.adapters import FWAdapter
from fw_classification.profiles import get_profile

log = logging.getLogger(__name__)


def run(
    file_input: Dict[str, Any],
    out_dir: Path,
    context: GearToolkitContext
) -> int:
    """Run classification."""
    # Needs context for update_*_metadata methods
    fw_adapter = FWAdapter(file_input, context)
    fw_adapter.classify(get_profile('main.yml'))

    return 0
