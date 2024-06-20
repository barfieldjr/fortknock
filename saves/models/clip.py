import json
import subprocess
import os
from typing import List, Dict, Any

# Function to load JSON data
def load_json(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to merge overlapping clusters
def merge_clusters(clusters: List[Dict[str, Any]], pre_duration: float = 10.0, post_duration: float = 3.0) -> List[Dict[str, Any]]:
    merged_clusters = []
    for cluster in clusters:
        start_time = max(0, cluster['start_timestamp'] - pre_duration)
        end_time = cluster['end_timestamp'] + post_duration
        if merged_clusters and start_time <= merged_clusters[-1]['end_time']:
            merged_clusters[-1]['end_time'] = end_time
        else:
            merged_clusters.append({'start_time': start_time, 'end_time': end_time})
    return merged_clusters

# Function to create directory if it doesn't exist
def create_directory(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to crop video based on merged clusters using ffmpeg
def crop_video(video_path: str, clusters: List[Dict[str, Any]], output_dir: str) -> List[str]:
    create_directory(output_dir)
    
    clip_paths = []
    for i, cluster in enumerate(clusters):
        start_time = cluster['start_time']
        duration = cluster['end_time'] - start_time
        output_path = os.path.join(output_dir, f"clip_{i+1}.mp4")
        clip_paths.append(output_path)
        
        # ffmpeg command to crop the video
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-ss', str(start_time),
            '-t', str(duration),
            '-c', 'copy',
            output_path
        ]
        subprocess.run(cmd, check=True)
    
    return clip_paths

# Function to merge clips into a single video using ffmpeg
def merge_clips(clip_paths: List[str], output_path: str):
    create_directory(os.path.dirname(output_path))
    
    with open('clip_list.txt', 'w') as f:
        for clip_path in clip_paths:
            f.write(f"file '{clip_path}'\n")
    
    cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', 'clip_list.txt',
        '-c', 'copy',
        output_path
    ]
    subprocess.run(cmd, check=True)
    os.remove('clip_list.txt')

# Main function to process the JSON data, crop the video, and merge the clips
def main():
    input_json = './formatted_clusters.json'  # Replace with your JSON file path
    video_path = '../../data/raw/obj_train_data/videos/test_video.mov'  # Replace with your video file path
    output_dir = '../../output/clips/output_clips'  # Directory to save cropped clips
    merged_output_path = '../../output/clips/merged/merged_video.mp4'  # Path to save the merged video
    
    clusters = load_json(input_json)
    
    # Merge overlapping clusters
    merged_clusters = merge_clusters(clusters)
    
    # Crop the video based on merged clusters
    clip_paths = crop_video(video_path, merged_clusters, output_dir)
    
    # Merge the clips into a single video
    merge_clips(clip_paths, merged_output_path)

if __name__ == "__main__":
    main()
