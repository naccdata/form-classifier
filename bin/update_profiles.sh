#!/bin/bash

set -euo pipefail

function update_submodules() {
    cd fw_gear_file_classifier/classification-profiles || exit
    git submodule update --init
    git fetch
    git fetch --tags
    git checkout "$1"
}

update_submodules "$1"
