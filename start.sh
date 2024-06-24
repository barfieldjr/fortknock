#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Run the inference script
python scripts/inference/infer.py "$@"

# Define the video filename and other necessary arguments
video_filename=$(basename "$1")
fps="$2"

# Run the clustering script
python scripts/clustering/converge.py

# Run the clipping script with the video filename
python scripts/clipping/clip.py "$video_filename"
