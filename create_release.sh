#!/bin/bash

version=$(python -c "from src.version import version; print(version)")

echo Create release for version $version
rm -rf release
mkdir release
tar -cf release/cln_channel_acceptor_$version.tar.gz src/ LICENSE README.md requirements.txt channel_acceptor.py
cd release
shasum -a 256 cln_channel_acceptor_$version.tar.gz > SHA256SUMS