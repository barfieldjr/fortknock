#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status
python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

if [ -d ".git" ]; then
    git submodule update --init --recursive
fi

if [ -f "yolov5/requirements.txt" ]; then
    pip install -r yolov5/requirements.txt
fi

# Install project requirements
pip install -r requirements.txt

echo "Setup complete."
