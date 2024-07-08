#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

echo "Current directory:"
pwd

echo "Listing files in the current directory:"
ls -la

echo "Checking environment variables:"
env

echo "Creating virtual environment..."
python3 -m venv venv || { echo "Failed to create virtual environment"; exit 1; }

echo "Checking virtual environment directory structure:"
if [ -d "venv" ]; then
    echo "venv directory exists:"
    ls -la venv
else
    echo "venv directory does not exist"
    exit 1
fi

if [ -d "venv/bin" ]; then
    echo "venv/bin directory exists:"
    ls -la venv/bin
else
    echo "venv/bin directory does not exist"
    exit 1
fi

if [ -f "venv/bin/python3" ]; then
    echo "venv/bin/python3 exists"
else
    echo "venv/bin/python3 does not exist"
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }

echo "Upgrading pip..."
pip install --upgrade pip || { echo "Failed to upgrade pip"; exit 1; }

if [ -d ".git" ]; then
    echo "Updating submodules..."
    git submodule update --init --recursive || { echo "Failed to update submodules"; exit 1; }
fi

if [ -f "yolov5/requirements.txt" ]; then
    echo "Installing yolov5 requirements..."
    pip install -r yolov5/requirements.txt || { echo "Failed to install yolov5 requirements"; exit 1; }
fi

echo "Installing project requirements..."
pip install -r requirements.txt || { echo "Failed to install project requirements"; exit 1; }

echo "Setup complete."
