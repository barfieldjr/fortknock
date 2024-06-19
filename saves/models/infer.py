import torch
import cv2
import numpy as np
import random
import os
import subprocess

def reduce_fps(input_video_path, output_video_path, fps):
    command = [
        'ffmpeg',
        '-i', input_video_path,
        '-r', str(fps),
        output_video_path
    ]
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
    x_center = (x[0] + x[2]) / 2
    y_center = (x[1] + x[3]) / 2
    within_horizontal_bounds = img_width / 4 <= x_center <= 3 * img_width / 4
    within_vertical_bounds = y_center >= img_height / 2
    return within_horizontal_bounds and within_vertical_bounds

def draw_region_bounds(img):
    img_height, img_width, _ = img.shape
    x1, x2 = img_width // 4, 3 * img_width // 4
    y1, y2 = img_height // 2, img_height
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

def process_video(video_path, output_path):
    print(f"Starting inference on video: {video_path}")
    
    # Load the model
    model_path = './knockdown_model_weights.pt'
    yolo_repo_path = '../../yolov5'
    
    if not os.path.exists(yolo_repo_path):
        raise FileNotFoundError(f"YOLOv5 directory not found at {yolo_repo_path}")
    if not os.path.exists(os.path.join(yolo_repo_path, 'hubconf.py')):
        raise FileNotFoundError(f"hubconf.py not found in {yolo_repo_path}")
    
    print("Loading model...")
    model = torch.hub.load(yolo_repo_path, 'custom', path=model_path, source='local')
    model.conf = 0.3  # Lower confidence threshold
    print("Model loaded successfully.")
    
    # Open the video file
    print("Opening video file...")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Video not found at {video_path}")
    
    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Video properties: width={frame_width}, height={frame_height}, fps={fps}, total_frames={total_frames}")
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (640, 640))
    
    frame_count = 0
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
            
            # Draw the specified region bounds
            draw_region_bounds(img_resized)
            
            # Run inference
            print(f"Running inference on frame {frame_count}...")
            results = model(img_resized)
            
            # Draw bounding boxes
            for *box, conf, cls in results.xyxy[0]:
                if is_within_region(box, img_width, img_height):
                    label = f'{model.names[int(cls)]} {conf:.2f}'
                    plot_one_box(box, img_resized, label=label, color=(255, 0, 0), line_thickness=2)
            
            # Write the frame with bounding boxes to the output video
            out.write(img_resized)
        except Exception as e:
            print(f"Error processing frame {frame_count}: {e}")
            break
    
    cap.release()
    out.release()
    print(f"Processed video saved to {output_path}")
    print("Processing completed.")

if __name__ == "__main__":
    input_video_path = '/Users/chrisbarfield/fortknock/data/raw/obj_train_data/videos/test_video.mov'  # Use absolute path
    reduced_fps_video_path = '/Users/chrisbarfield/fortknock/data/raw/obj_train_data/videos/reduced_fps_video.mov'
    output_path = '/Users/chrisbarfield/fortknock/output/processed_video.mp4'
    
    # Reduce the FPS of the video
    print("Reducing FPS of the video...")
    reduce_fps(input_video_path, reduced_fps_video_path, 15)  # Change FPS as needed
    
    # Process the video with reduced FPS
    process_video(reduced_fps_video_path, output_path)
