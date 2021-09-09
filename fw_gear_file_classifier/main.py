"""Main module."""
import logging
from typing import Any, Dict

from flywheel_gear_toolkit import GearToolkitContext
from flywheel_gear_toolkit.utils.qc import add_qc_info
from fw_classification import Profile
from fw_classification.adapters import FWAdapter, NiftiFWAdapter

from . import PKG_NAME, __version__

log = logging.getLogger(__name__)


def classify(
    file_input: Dict[str, Any], context: GearToolkitContext, profile: Profile
) -> int:
    """Run classification."""
    # Needs context for update_*_metadata methods
    log.info("Starting classification.")
    if file_input["object"]["type"] == "nifti":
        fw_adapter = NiftiFWAdapter(file_input, context)
    else:
        fw_adapter = FWAdapter(file_input, context)
    result = fw_adapter.classify(profile)
    log.info(f"Finished classification. Result: {result}")
    if not result:
        log.warning("Unsuccessful classification")
    log.info("Adding gear qc info.")
    info = add_qc_info(context, file_input, name=PKG_NAME, version=__version__)
    context.update_file_metadata(file_input["location"]["name"], info=info)

    return int(not result)
