import torch
import cv2
import numpy as np
import random
import os
import subprocess
import json
import argparse

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

def plot_one_box(x, img, color=None, label=None, line_thickness=3):
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

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

def draw_region_bounds(img):
    x_start = 260
    x_end = 380
    y_start = 370
    y_end = 590
    cv2.rectangle(img, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)

def save_frame(frame, output_path, frame_count):
    cv2.imwrite(f"{output_path}/frame_{frame_count}.jpg", frame)

def process_video(video_path, output_path, json_output_path, frames_output_path, codec):
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
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Video properties: width={frame_width}, height={frame_height}, fps={fps}, total_frames={total_frames}")

    out = cv2.VideoWriter(output_path, codec, fps, (640, 640))

    frame_count = 0
    detection_timestamps = []

    if not os.path.exists(frames_output_path):
        os.makedirs(frames_output_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print(f"End of video or can't read frame at frame {frame_count}.")
            break

        frame_count += 1
        if frame_count % 10 == 0:
            print(f"Processing frame {frame_count}/{total_frames}")

        try:
            img_resized = cv2.resize(frame, (640, 640))
            img_height, img_width, _ = img_resized.shape

            draw_region_bounds(img_resized)

            print(f"Running inference on frame {frame_count}...", flush=True)
            results = model(img_resized)

            detection_made = False
            for *box, conf, cls in results.xyxy[0]:
                if is_within_region(box, img_width, img_height):
                    label = f'{model.names[int(cls)]} {conf:.2f}'
                    plot_one_box(box, img_resized, label=label, color=(255, 0, 0), line_thickness=2)
                    detection_made = True

                    timestamp = frame_count / fps
                    detection_timestamps.append({
                        "frame": frame_count,
                        "timestamp": timestamp,
                        "label": label,
                        "confidence": float(conf),
                        "box": [int(x) for x in box]
                    })

            if detection_made:
                save_frame(img_resized, frames_output_path, frame_count)

            out.write(img_resized)
        except Exception as e:
            print(f"Error processing frame {frame_count}: {e}")
            break

    cap.release()
    out.release()

    with open(json_output_path, 'w') as json_file:
        json.dump(detection_timestamps, json_file, indent=4)

    print(f"Processed video saved to {output_path}")
    print(f"Detection timestamps saved to {json_output_path}")
    print("Processing completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process video for object detection.')
    parser.add_argument('filename', type=str, help='Filename of the input video file')
    parser.add_argument('fps', type=int, help='Frames per second for the reduced FPS video')
    args = parser.parse_args()

    filename = args.filename
    fps = args.fps

    project_root = os.path.dirname(os.path.abspath(__file__))

    input_video_path = os.path.join(project_root, '..', '..', 'data', 'input', filename)
    reduced_fps_video_path = os.path.join(project_root, '..', '..', 'data', 'raw', 'videos', 'reduced_fps_video.mp4')
    output_video_path = os.path.join(project_root, '..', '..', 'data', 'output', 'processed_video.mp4')
    json_output_path = os.path.join(project_root, '..', '..', 'data', 'output', 'detection_timestamps.json')
    frames_output_path = os.path.join(project_root, '..', '..', 'data', 'output', 'detection_frames')

    print("Reducing FPS of the video...")
    reduce_fps(input_video_path, reduced_fps_video_path, fps)

    process_video(reduced_fps_video_path, output_video_path, json_output_path, frames_output_path, cv2.VideoWriter_fourcc(*'mp4v'))
