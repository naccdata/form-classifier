#!/bin/bash

set -euo pipefail

function update_submodules() {
    cd fw_gear_file_classifier/classification-profiles || exit
    git fetch
    git fetch --tags
    git checkout "$1"
}

update_submodules "$1"
git add fw_gear_file_classifier/classification-profiles
git commit --no-verify -m "MAIN: Update classification-profiles to version $1"




