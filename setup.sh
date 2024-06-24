#!/bin/bash

echo "Creating and activating the Conda environment..."
conda create -n clean_env python=3.9 -y
source $(conda info --base)/etc/profile.d/conda.sh
conda activate clean_env

echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Setup env and installed dependencies..."
