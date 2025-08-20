#!/usr/bin/env bash
set -euo pipefail

# Local build with basepath "/"
python3 src/main.py

# Serve the built site from docs/ on port 8888
cd docs
python3 -m http.server 8888
