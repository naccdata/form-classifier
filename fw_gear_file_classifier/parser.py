"""Parser module to parse gear config.json."""
from typing import Any, Dict, Optional, Tuple
from pathlib import Path

from flywheel_gear_toolkit import GearToolkitContext


def parse_config(
    gear_context: GearToolkitContext,
) -> Tuple[Optional[str], Dict[str, Any], Path]:
    """Parse file-input from gear context."""
    try:
        api_key = gear_context.config_json['inputs']['api-key']['key']
    except KeyError:
        api_key = None
    file_input: Dict[str, Any] = gear_context.get_input("file-input")  # type: ignore

    return api_key, file_input, gear_context.output_dir
