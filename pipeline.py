import os
import subprocess
import shutil

def run_inference(video_filename, fps):
    project_root = os.path.abspath(os.path.dirname(__file__))
    input_video_path = os.path.join(project_root, 'input', video_filename)
    reduced_fps_video_path = os.path.join(project_root, 'data', 'raw', 'obj_train_data', 'videos', 'reduced_fps_video.mp4')
    output_video_path = os.path.join(project_root, 'output', 'processed_video.mp4')
    json_output_path = os.path.join(project_root, 'output', 'detection_timestamps.json')
    frames_output_path = os.path.join(project_root, 'output', 'detection_frames')

    print("Running inference...")
    subprocess.run(['python', 'scripts/inference/infer.py', video_filename, str(fps)], check=True)

def run_clustering():
    project_root = os.path.abspath(os.path.dirname(__file__))
    detection_timestamps_path = os.path.join(project_root, 'output', 'detection_timestamps.json')

    if not os.path.exists(detection_timestamps_path):
        raise FileNotFoundError(f"File not found: {detection_timestamps_path}")

    print("Running clustering...")
    subprocess.run(['python', 'scripts/clustering/converge.py'], check=True)

def run_clipping(video_filename):
    project_root = os.path.abspath(os.path.dirname(__file__))
    formatted_clusters_path = os.path.join(project_root, 'output', 'formatted_clusters.json')
    output_clips_dir = os.path.join(project_root, 'output', 'clips', 'output_clips')
    merged_output_path = os.path.join(project_root, 'output', 'merged', 'merged_video.mp4')

    if not os.path.exists(formatted_clusters_path):
        raise FileNotFoundError(f"File not found: {formatted_clusters_path}")

    print("Running clipping...")
    subprocess.run(['python', 'scripts/clipping/clip.py', video_filename], check=True)

def cleanup_temp_files():
    project_root = os.path.abspath(os.path.dirname(__file__))
    paths_to_remove = [
        os.path.join(project_root, 'data', 'raw', 'obj_train_data', 'videos', 'reduced_fps_video.mp4'),
        os.path.join(project_root, 'output', 'detection_timestamps.json'),
        os.path.join(project_root, 'output', 'detection_frames'),
        os.path.join(project_root, 'output', 'formatted_clusters.json')
    ]

    for path in paths_to_remove:
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)

    print("Temporary files cleaned up.")

def main():
    video_filename = input("Enter the video filename: ")
    fps = int(input("Enter the frames per second (FPS): "))

    run_inference(video_filename, fps)
    run_clustering()
    run_clipping(video_filename)
    cleanup_temp_files()

if __name__ == "__main__":
    main()
