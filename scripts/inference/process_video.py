import cv2
import os

def process_video(video_path):
    print(f"Starting to process video: {video_path}")

    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"File does not exist at {video_path}")

    print("Opening video file...")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Video not found or cannot be opened at {video_path}")
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Video properties: width={frame_width}, height={frame_height}, fps={fps}, total_frames={total_frames}")

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print(f"End of video or can't read frame at frame {frame_count}.")
            break

        frame_count += 1
        if frame_count % 10 == 0:
            print(f"Processing frame {frame_count}/{total_frames}")

        print(f"Frame {frame_count}: Dimensions = {frame.shape}")

    cap.release()
    print("Video processing completed.")

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(project_root, 'input', 'test_video.mov')
    process_video(video_path)
