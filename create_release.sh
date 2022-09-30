#!/bin/bash

version=$(python -c "from src.version import version; print(version)")

echo Create release for version $version
rm -rf release
mkdir release
tar -cf release/cln_super_bitcoind_$version.tar.gz src/ LICENSE README.md requirements.txt super_bitcoind.py test_bitcoin_node_availability.py
cd release
shasum -a 256 cln_super_bitcoind_$version.tar.gz > SHA256SUMS