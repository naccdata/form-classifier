"""Main module."""
from typing import Any, Dict, Optional
import logging
from pathlib import Path
import json

from fw_classification.adapters import FWAdapter
from fw_classification.profiles import get_profile

log = logging.getLogger(__name__)


def run(
    api_key: Optional[str],
    file_input: Dict[str, Any],
    out_dir: Path
) -> int:
    """Run classification."""
    fw_adapter = FWAdapter(file_input, api=(api_key or ""))
    metadata = fw_adapter.classify(get_profile('main.yml'))
    log.info('Writing metadata:\n {json.dumps(metadata, indent=2)}')
    with open(out_dir / '.metadata.json', 'w') as fp:
        json.dump(metadata, fp, indent=2)

    return 0
