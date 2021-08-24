"""Parser module to parse gear config.json."""
from typing import Any, Dict, Optional, Tuple
from pathlib import Path

from flywheel_gear_toolkit import GearToolkitContext
from fw_classification.profiles.builder.blocks import block_from_context_classifications
from fw_classification.classify import Profile
from fw_classification.profiles import get_profile


def parse_config(
    gear_context: GearToolkitContext,
) -> Tuple[
        Dict[str, Any],     # File input
        Profile             # Profile to classify with
]:
    """Parse file-input from gear context."""
    file_input: Dict[str, Any] = gear_context.get_input("file-input")  # type: ignore

    # Get optional custom profile from input
    profile_path: Optional[Path] = gear_context.get_input_path('profile')
    if profile_path:
        profile = Profile(profile_path)
    else:
        profile = get_profile('main.yml')

    # Get optional custom classifications from project context
    classify_context = gear_context.get_input('classifications')
    custom_block = None
#    if classify_context and classify_context.get('value', {}):
#        custom_block = block_from_context_classifications(
#            classify_context.get('value')
#        )
#        # Add custom block to the end of the profile if it's defined.
#        profile.handle_block(custom_block, 'custom')

    return file_input, profile
