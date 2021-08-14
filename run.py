#!/usr/bin/env python
"""The run script"""
import logging
import sys

from flywheel_gear_toolkit import GearToolkitContext

from fw_gear_file_classifier.main import run
from fw_gear_file_classifier.parser import parse_config
from pathlib import Path


log = logging.getLogger(__name__)


def main(context: GearToolkitContext) -> None:  # pragma: no cover
    """Parses config and run"""
    # Parse config
    debug: bool
    file_input: Path
    debug, file_input = parse_config(context)
    # Run main entry
    e_code = run(file_input)
    sys.exit(e_code)


if __name__ == "__main__":  # pragma: no cover
    with GearToolkitContext() as gear_context:
        gear_context.init_logging()
        main(gear_context)
