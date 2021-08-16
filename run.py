#!/usr/bin/env python
"""The run script."""
import logging
import sys
import typing as t

from flywheel_gear_toolkit import GearToolkitContext
from fw_gear_file_classifier.main import run
from fw_gear_file_classifier.parser import parse_config
from pathlib import Path


log = logging.getLogger(__name__)


def main(context: GearToolkitContext) -> None:  # pragma: no cover
    """Parse config and run."""
    # Parse config
    file_input: t.Dict[str, t.Any]
    output_dir: Path
    file_input, output_dir = parse_config(context)
    # Run main entry
    e_code = run(file_input, output_dir, context)
    sys.exit(e_code)


if __name__ == "__main__":  # pragma: no cover
    with GearToolkitContext() as gear_context:
        gear_context.init_logging()
        main(gear_context)
