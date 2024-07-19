import torch
import cv2
import numpy as np
import os
import subprocess
import json
import argparse

def get_total_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Video not found at {video_path}")
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return total_frames

def reduce_fps(input_video_path, output_video_path, fps):
    os.makedirs(os.path.dirname(output_video_path), exist_ok=True)
    command = [
        'ffmpeg',
        '-y',
        '-i', input_video_path,
        '-r', str(fps),
        output_video_path
    ]
    print(f"Running command: {' '.join(command)}")
    subprocess.run(command, check=True)

def is_within_region(x, img_width, img_height):
    x_start = 260
    x_end = 380
    y_start = 400
    y_end = 450
    x_center = (x[0] + x[2]) / 2
    y_center = (x[1] + x[3]) / 2
    within_horizontal_bounds = x_start <= x_center <= x_end
    within_vertical_bounds = y_start <= y_center <= y_end
    return within_horizontal_bounds and within_vertical_bounds

def process_video(video_path, output_path, json_output_path, codec, total_frames):
    print(f"Starting inference on video: {video_path}")

    project_root = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(project_root, '..', '..', 'models', 'weights', 'knockdown_model_weights.pt')
    yolo_repo_path = os.path.join(project_root, '..', '..', 'yolov5')

    if not os.path.exists(yolo_repo_path):
        raise FileNotFoundError(f"YOLOv5 directory not found at {yolo_repo_path}")
    if not os.path.exists(os.path.join(yolo_repo_path, 'hubconf.py')):
        raise FileNotFoundError(f"hubconf.py not found in {yolo_repo_path}")

    print("Loading model...")
    model = torch.hub.load(yolo_repo_path, 'custom', path=model_path, source='local')
    model.conf = 0.2

    print("Model loaded successfully.")

    print("Opening video file...")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Video not found at {video_path}")

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print(f"Video properties: width={frame_width}, height={frame_height}, fps={fps}, total_frames={total_frames}")

    out = cv2.VideoWriter(output_path, codec, fps, (640, 640))

    frame_count = 0
    detection_timestamps = []

    batch_size = fps  # Process one second of video frames at a time
    frames_batch = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print(f"End of video or can't read frame at frame {frame_count}.")
            break

        frame_count += 1
        frames_batch.append(frame)

        if len(frames_batch) == batch_size:
            process_frames(frames_batch, frame_count, model, fps, detection_timestamps, out)
            frames_batch = []
        
        progress = (frame_count / total_frames) * 100
        yield frame_count, progress

    # Process any remaining frames in the batch
    if frames_batch:
        process_frames(frames_batch, frame_count, model, fps, detection_timestamps, out)

    cap.release()
    out.release()

    with open(json_output_path, 'w') as json_file:
        json.dump(detection_timestamps, json_file, indent=4)

    print(f"Processed video saved to {output_path}")
    print(f"Detection timestamps saved to {json_output_path}")
    print("Processing completed.")

def process_frames(frames_batch, frame_count, model, fps, detection_timestamps, out):
    for frame in frames_batch:
        try:
            img_resized = cv2.resize(frame, (640, 640))
            img_height, img_width, _ = img_resized.shape

            print(f"Running inference on frame {frame_count}...", flush=True)
            results = model(img_resized)

            for *box, conf, cls in results.xyxy[0]:
                if is_within_region(box, img_width, img_height):
                    timestamp = frame_count / fps
                    detection_timestamps.append({
                        "frame": frame_count,
                        "timestamp": timestamp,
                        "label": model.names[int(cls)],
                        "confidence": float(conf),
                        "box": [int(x) for x in box]
                    })

            out.write(img_resized)
        except Exception as e:
            print(f"Error processing frame {frame_count}: {e}")
            break

def run_inference(filename, fps):
    project_root = os.path.dirname(os.path.abspath(__file__))

    input_video_path = os.path.join(project_root, '..', '..', 'data', 'input', filename)
    reduced_fps_video_path = os.path.join(project_root, '..', '..', 'data', 'raw', 'videos', 'reduced_fps_video.mp4')
    output_video_path = os.path.join(project_root, '..', '..', 'data', 'output', 'processed_video.mp4')
    json_output_path = os.path.join(project_root, '..', '..', 'data', 'output', 'detection_timestamps.json')

    print("Reducing FPS of the video...")
    reduce_fps(input_video_path, reduced_fps_video_path, fps)
    yield 0, 10  # 10% progress after reducing FPS

    total_frames = get_total_frames(reduced_fps_video_path)
    for frame, progress in process_video(reduced_fps_video_path, output_video_path, json_output_path, cv2.VideoWriter_fourcc(*'mp4v'), total_frames):
        yield frame, 10 + (progress * 0.9)  # Scale progress to 10-100%

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process video for object detection.')
    parser.add_argument('filename', type=str, help='Filename of the input video file')
    parser.add_argument('fps', type=int, help='Frames per second for the reduced FPS video')
    args = parser.parse_args()

    for frame, progress in run_inference(args.filename, args.fps):
        print(f"Progress: {progress:.2f}%, Frame: {frame}")