#!/bin/bash

source venv/bin/activate

python scripts/inference/infer.py "$@"

video_filename=$(basename "$1")
fps="$2"

python scripts/clustering/converge.py

python scripts/clipping/clip.py "$video_filename"
