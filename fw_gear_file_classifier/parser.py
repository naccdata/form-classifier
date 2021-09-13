"""Parser module to parse gear config.json."""
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from flywheel_gear_toolkit import GearToolkitContext
from fw_classification.classify import Profile
from fw_classification.classify.block import Block
from fw_classification.profiles import get_profile

log = logging.getLogger(__name__)


def parse_config(
    gear_context: GearToolkitContext,
) -> Tuple[Dict[str, Any], Profile]:  # File input  # Profile to classify with
    """Parse options from gear config.

    Args:
        gear_context (GearToolkitContext): Gear toolkit context.

    Returns:
        tuple:
            - File input as a dictionary
            - Profile to use for classification, defaults to the
                classification-toolkits "main.yml"
    """
    file_input: Dict[str, Any] = gear_context.get_input("file-input")

    # Get optional custom profile from input
    profile_path: Optional[Path] = gear_context.get_input_path("profile")
    if profile_path:
        profile = Profile(profile_path)
    else:
        # Default to the classification-toolkit's "main.yml" which
        #   should be a "catch-all" and is defined in the fw-classifcation
        #   repo under (fw_classification/profiles/main.yml)
        profile = Profile(get_profile("main.yml"))

    # Get optional custom classifications from project context
    classify_context = gear_context.get_input("classifications")
    custom_block = None
    if classify_context and classify_context.get("value", {}):
        log.debug(f"Context classification: {classify_context.get('value')}")
        try:
            block = {"name": "custom", "rules": classify_context.get("value")}
            custom_block, err = Block.from_dict(block)
            if err:
                log.error("\n".join([str(e) for e in err]))
                raise RuntimeError()
            log.info(
                "Found custom classification in project context, parsed as: \n"
                f"{custom_block}"
            )
            # Add custom block to the end of the profile if it's defined.
            profile.handle_block(custom_block, "custom")  # type: ignore
        except:  # pylint: disable=bare-except
            log.warning(
                "Could not handle context classification "
                f"{classify_context.get('value')}"
            )

    return file_input, profile
