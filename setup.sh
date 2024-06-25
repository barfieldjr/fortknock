#!/bin/bash

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

git submodule update --init --recursive

pip install -r yolov5/requirements.txt
pip install -r requirements.txt
