#!/bin/bash

# Make sure you have the GitHub CLI installed (https://cli.github.com/) and logged in with `gh auth login` before running this script.

# For some reasons, v5.0 release json file name is just 'vss.json' so if this remains a thing in future releases,
# this script won't work due to same overwriting files with the same name.

# https://github.com/COVESA/vehicle_signal_specification/releases/download/v5.0/vss.json
# https://github.com/COVESA/vehicle_signal_specification/releases/download/v4.2/vss_rel_4.2.json

REPO="COVESA/vehicle_signal_specification"
ASSET_PATTERN="*yaml"
VERSIONS=$(gh release list --repo COVESA/vehicle_signal_specification |  awk '{print $1}')
TARGET_DIR=$"vss_releases_qu"

mkdir -p $TARGET_DIR

echo "Downloading COVESA-VSS JSON releases"

for VERSION in $VERSIONS;
do
    echo $VERSION
    if [[ $VERSION == *rc0* ]]; then
        echo "Skipping Release Candidate version"
        continue
    fi
    gh release download $VERSION --repo $REPO --pattern $ASSET_PATTERN --dir $TARGET_DIR
    mv $TARGET_DIR/units.yaml $TARGET_DIR/$VERSION-units.yaml 
    mv $TARGET_DIR/quantities.yaml $TARGET_DIR/$VERSION-quantities.yaml 
done

echo "Cleaning up..."

OLD_VERSIONS=("1.0" "2.0" "2.1" "2.2")

for file in $TARGET_DIR/*; 
do
    filename="$(basename "$file")"

    if [[ $filename == *noexpand* ]]; then
        echo "Removing unused $(basename "$file")"
        rm $file
       
    fi

    for version in "${OLD_VERSIONS[@]}"; do
        if [[ $filename == *$version* ]]; then
            echo "Removing old VSS version $version: $filename"
            rm $file
            continue 2
        fi
    done
done