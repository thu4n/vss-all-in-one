#!/bin/bash

# Make sure you have the GitHub CLI installed (https://cli.github.com/) and logged in with `gh auth login` before running this script.

# For some reasons, v5.0 release json file name is just 'vss.json' so if this remains a thing in future releases,
# this script won't work due to files with the same name getting overwritten.

# https://github.com/COVESA/vehicle_signal_specification/releases/download/v5.0/vss.json
# https://github.com/COVESA/vehicle_signal_specification/releases/download/v4.2/vss_rel_4.2.json

REPO="COVESA/vehicle_signal_specification"
ASSET_PATTERN="*json"
VERSIONS=$(gh release list --repo COVESA/vehicle_signal_specification |  awk '{print $1}')
TARGET_DIR=$"vss_releases"
OLD_VERSIONS=("1.0" "2.0" "2.1" "2.2")

mkdir -p $TARGET_DIR

echo "1. Downloading COVESA-VSS JSON releases"

for VERSION in $VERSIONS;
do
    if [[ $VERSION == *rc0* ]]; then
        echo "-- Skipping Release Candidate version $VERSION"
        continue
    fi

    for OLD_VERSION in "${OLD_VERSIONS[@]}"; do
        if [[ $VERSION == *$OLD_VERSION* ]]; then
            echo "-- Skipping old VSS version $OLD_VERSION"
            OLD_VERSIONS=( "${OLD_VERSIONS[@]/$OLD_VERSION}" )
            continue 2
        fi
    done

    echo "-- Downloading VSS Version $VERSION"
    gh release download $VERSION --repo $REPO --pattern "$ASSET_PATTERN" --dir $TARGET_DIR
done

mv $TARGET_DIR/vss.json $TARGET_DIR/vss_rel_5.0.json

# We only need the latest version of units.yaml for the vehicle model generator to work.
echo "2. Downloading VSS 5.0 units.yaml ..."
gh release download v5.0 --repo $REPO --pattern "units.yaml" --dir .
mv units.yaml units_v5.0.yaml

echo "3. Cleaning up..."

for file in $TARGET_DIR/*; 
do
    filename="$(basename "$file")"
    if [[ $filename == *noexpand* ]]; then
        echo "-- Removing unused $(basename "$file")"
        rm $file
    fi
done

echo "All tasks done."