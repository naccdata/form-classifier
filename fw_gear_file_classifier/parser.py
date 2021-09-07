"""Parser module to parse gear config.json."""
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from flywheel_gear_toolkit import GearToolkitContext
from fw_classification.classify import Profile
from fw_classification.profiles import get_profile
from fw_classification.profiles.builder.blocks import block_from_context_classifications

log = logging.getLogger(__name__)


def parse_config(
    gear_context: GearToolkitContext,
) -> Tuple[Dict[str, Any], Profile]:  # File input  # Profile to classify with
    """Parse file-input from gear context."""
    file_input: Dict[str, Any] = gear_context.get_input("file-input")  # type: ignore

    # Get optional custom profile from input
    profile_path: Optional[Path] = gear_context.get_input_path("profile")
    if profile_path:
        profile = Profile(profile_path)
    else:
        profile = Profile(get_profile("main.yml"))

    # Get optional custom classifications from project context
    classify_context = gear_context.get_input("classifications")
    custom_block = None
    if classify_context and classify_context.get("value", {}):
        log.debug(f"Context classification: {classify_context.get('value')}")
        try:
            custom_block = block_from_context_classifications(classify_context.get("value"))
            log.info(
                f"Found custom classification in project context, parsed as {custom_block}"
            )
            # Add custom block to the end of the profile if it's defined.
            profile.handle_block(custom_block, "custom")
        except:
            log.warning(f"Could not handle context classification {classify_context.get('value')}")

    return file_input, profile
