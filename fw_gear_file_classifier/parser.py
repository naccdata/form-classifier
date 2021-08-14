"""Parser module to parse gear config.json."""
from typing import Any, Dict, Tuple

from flywheel_gear_toolkit import GearToolkitContext


def parse_config(
    gear_context: GearToolkitContext,
) -> Tuple[bool, Dict[str, Any]]:
    """Parse file-input from gear context."""

    debug: bool = gear_context.config.get("debug")  # type: ignore
    file_input: Dict[str, Any] = gear_context.get_input("file-input")  # type: ignore

    return debug, file_input
