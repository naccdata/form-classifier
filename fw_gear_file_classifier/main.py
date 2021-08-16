"""Main module."""
from typing import Any, Dict
import logging
from pathlib import Path
import json

from fw_classification.adapters import FWAdapter
from fw_classification.profiles import get_profile

log = logging.getLogger(__name__)

def run(file_input: Dict[str, Any], out_dir: Path) -> int:
    """Main run function."""
    fw_adapter = FWAdapter(file_input)
    metadata = fw_adapter.run(get_profile('main.yml'))
    log.info('Writing metadata:\n {json.dumps(metadata, indent=2)}')
    with open(out_dir / '.metadata.json', 'w') as fp:
        json.dump(metadata, fp, indent=2)

    return 0
