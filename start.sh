#!/bin/bash

source venv/bin/activate

python -u scripts/inference/infer.py "$@"

video_filename=$(basename "$1")
fps="$2"

python -u scripts/clustering/converge.py

python -u scripts/clipping/clip.py "$video_filename"

python -u scripts/util/clean.py