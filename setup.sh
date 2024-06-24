#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Initialize and update the YOLOv5 submodule
git submodule update --init --recursive

# Install Python dependencies
pip install -r yolov5/requirements.txt
pip install -r requirements.txt
