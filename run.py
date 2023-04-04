#!/usr/bin/env python
"""The run script."""
import logging
import typing as t

from flywheel_gear_toolkit import GearToolkitContext

from nacc_gear_form_classifier.main import classify
from nacc_gear_form_classifier.parser import parse_config

log = logging.getLogger(__name__)


def main(context: GearToolkitContext) -> None:  # pragma: no cover
    """Parse config and run."""
    # Parse config
    file_input, profile = parse_config(context)
    # Run main entry
    _ = classify(file_input, context, profile)
    tag = context.config.get("tag")
    context.metadata.add_file_tags(file_input, t.cast(str, tag))


if __name__ == "__main__":  # pragma: no cover
    with GearToolkitContext(fail_on_validation=False) as gear_context:
        gear_context.init_logging()
        main(gear_context)
