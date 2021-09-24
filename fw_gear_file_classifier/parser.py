"""Parser module to parse gear config.json."""
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from flywheel_gear_toolkit import GearToolkitContext
from fw_classification.classify import Profile, includes
from fw_classification.classify.block import Block

log = logging.getLogger(__name__)

default_profiles = (
    Path(__file__).parents[0] / "classification-profiles/profiles"
).resolve()


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

    # Get optional custom profile from config
    profile_url: Optional[str] = gear_context.config.get("profile_url", "")
    config_profile: Optional[Path] = None
    if profile_url:
        profile = Profile(includes.get_git_profile(profile_url))
        log.info(f"Using profile from config {profile_url}")
    else:
        # Get optional custom profile from input
        profile_path: Optional[Path] = gear_context.get_input_path("profile")
        if profile_path:
            log.info(f"Using profile from input {profile_path}")
            profile = Profile(profile_path)
        else:
            # Default to the classification-toolkit's "main.yml" which
            #   should be a "catch-all" and is defined in the fw-classifcation
            #   repo under (fw_classification/profiles/main.yml)
            log.info("Using default profile 'main.yml'")
            profile = Profile(default_profiles / "main.yml")

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
