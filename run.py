#!/usr/bin/env python
"""The run script."""
import logging
import typing as t

from flywheel_gear_toolkit import GearToolkitContext

from fw_gear_file_classifier.main import classify
from fw_gear_file_classifier.parser import parse_config
from fw_gear_file_classifier.utils import validate_modality_schema

log = logging.getLogger(__name__)


def main(context: GearToolkitContext) -> None:  # pragma: no cover
    """Parse config and run."""
    # Parse config
    file_input, profile, validate = parse_config(context)
    client = context.client

    if validate:
        validate_modality_schema(client, file_input["object"])

    # Run main entry
    _ = classify(file_input, context, profile)
    tag = context.config.get("tag")
    context.metadata.add_file_tags(file_input, t.cast(str, tag))


if __name__ == "__main__":  # pragma: no cover
    with GearToolkitContext(
        fail_on_validation=False,
    ) as gear_context:
        gear_context.init_logging()
        main(gear_context)
