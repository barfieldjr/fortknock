#!/bin/bash

# Ensure conda is initialized
export PATH="$HOME/opt/anaconda3/bin:$PATH"
CONDA_BASE=$(conda info --base)
source "$CONDA_BASE/etc/profile.d/conda.sh"

ENV_NAME="clean_env"

# Remove the existing environment if it exists
if conda env list | grep -q "^$ENV_NAME "; then
    echo "Removing existing Conda environment '$ENV_NAME'..."
    conda env remove -n $ENV_NAME
fi

# Create a new environment
echo "Creating Conda environment '$ENV_NAME'..."
conda create -n $ENV_NAME python=3.9 -y

# Activate the Conda environment and install dependencies
echo "Activating Conda environment '$ENV_NAME'..."
source "$CONDA_BASE/etc/profile.d/conda.sh"
conda activate $ENV_NAME

echo "Installing dependencies..."
pip install -r requirements.txt

# Check if the environment is activated
if [ "$CONDA_DEFAULT_ENV" = "$ENV_NAME" ]; then
    echo "Conda environment '$ENV_NAME' is activated."
else
    echo "Failed to activate Conda environment '$ENV_NAME'."
    exit 1
fi

# Run the pipeline script
python pipeline.py
