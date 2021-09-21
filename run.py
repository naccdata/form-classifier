#!/usr/bin/env python
"""The run script."""
import logging
import sys

from flywheel_gear_toolkit import GearToolkitContext

from fw_gear_file_classifier.main import classify
from fw_gear_file_classifier.parser import parse_config

log = logging.getLogger(__name__)


def main(context: GearToolkitContext) -> None:  # pragma: no cover
    """Parse config and run."""
    # Parse config
    file_input, profile = parse_config(context)
    # Run main entry
    e_code = classify(file_input, context, profile)
    tags = context.get_input("file-input")["object"]["tags"][:]  # copy
    tag = context.config.get("tag")
    if tag:
        tags.append(tag)
    context.update_file_metadata(
        context.get_input("file-input")["location"]["name"], tags=tags
    )
    sys.exit(e_code)


if __name__ == "__main__":  # pragma: no cover
    with GearToolkitContext(fail_on_validation=False) as gear_context:
        gear_context.init_logging()
        main(gear_context)
