# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install git, gcc, python3-dev, and additional dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    python3-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean

# Clone the YOLOv5 repository
RUN git clone https://github.com/ultralytics/yolov5

# Copy the current directory contents into the container at /app
COPY . /app

# Install YOLOv5 requirements
RUN cd yolov5 && pip install -r requirements.txt

# Install additional Python dependencies
RUN pip install torch opencv-python matplotlib

# Command to run the inference script
CMD ["python", "saves/models/infer.py"]
