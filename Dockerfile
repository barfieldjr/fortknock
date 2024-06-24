FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    gcc \
    python3-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    && apt-get clean

# Clone YOLOv5
RUN git clone https://github.com/ultralytics/yolov5

COPY . /app

RUN pip install -r yolov5/requirements.txt
RUN pip install -r requirements.txt

RUN mkdir -p /app/output /app/target

ENTRYPOINT ["python", "saves/models/infer.py"]