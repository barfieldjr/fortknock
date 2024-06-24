#!/bin/bash

IMAGE_NAME="fortknock"

VIDEO_FILENAME=$1
FPS=$2

if [ -z "$VIDEO_FILENAME" ] || [ -z "$FPS" ]; then
  echo "Usage: $0 <video_filename> <fps>"
  exit 1
fi

echo "Building Docker image..."
docker build -t $IMAGE_NAME .

echo "Running Docker container..."
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/data:/app/data \
  $IMAGE_NAME $VIDEO_FILENAME $FPS
