# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    python3-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    && apt-get clean

# Clone YOLOv5 repository
RUN git clone https://github.com/ultralytics/yolov5

# Copy the current directory contents into the container
COPY . /app

# Install Python dependencies
RUN pip install -r yolov5/requirements.txt
RUN pip install -r requirements.txt

# Ensure all shell scripts are executable
RUN chmod +x *.sh

# Create necessary directories
RUN mkdir -p /app/output /app/target /app/data/input /app/data/output

# Define the entry point for the container
ENTRYPOINT ["scripts/start.sh"]
