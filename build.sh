#!/usr/bin/env bash
set -euo pipefail

# Build for GitHub Pages with basepath "/static_generator/"
python3 src/main.py "/static_generator/"
