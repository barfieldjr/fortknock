import json
import subprocess
import os
from typing import List, Dict, Any
import argparse

def load_json(file_path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist, creating an empty file.")
        with open(file_path, 'w') as file:
            json.dump([], file)
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def merge_clusters(clusters: List[Dict[str, Any]], pre_duration: float = 6.0, post_duration: float = 2.0) -> List[Dict[str, Any]]:
    merged_clusters = []
    for cluster in clusters:
        start_time = max(0, cluster['start_timestamp'] - pre_duration)
        end_time = cluster['end_timestamp'] + post_duration
        if merged_clusters and start_time <= merged_clusters[-1]['end_time']:
            merged_clusters[-1]['end_time'] = end_time
        else:
            merged_clusters.append({'start_time': start_time, 'end_time': end_time})
    return merged_clusters

def create_directory(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)

def crop_video(video_path: str, clusters: List[Dict[str, Any]], output_dir: str):
    create_directory(output_dir)
    
    clip_paths = []
    total_clusters = len(clusters)
    for i, cluster in enumerate(clusters):
        start_time = cluster['start_time']
        duration = cluster['end_time'] - start_time
        output_path = os.path.join(output_dir, f"clip_{i+1}.mp4")
        clip_paths.append(output_path)
        
        cmd = [
            'ffmpeg',
            '-y',
            '-i', video_path,
            '-ss', str(start_time),
            '-t', str(duration),
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '18',
            '-pix_fmt', 'yuv420p',
            '-c:a', 'aac',
            '-b:a', '128k',
            output_path
        ]
        print(f"Running command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        
        if os.path.exists(output_path):
            print(f"Clip created: {output_path}")
        else:
            print(f"Failed to create clip: {output_path}")
        
        progress = ((i + 1) / total_clusters) * 100
        yield progress
    
    return clip_paths

def merge_clips(clip_paths: List[str], output_path: str):
    create_directory(os.path.dirname(output_path))
    
    with open('clip_list.txt', 'w') as f:
        for clip_path in clip_paths:
            if os.path.exists(clip_path):
                f.write(f"file '{clip_path}'\n")
            else:
                print(f"Clip not found: {clip_path}")

    with open('clip_list.txt', 'r') as f:
        print("Contents of clip_list.txt:")
        print(f.read())
    
    cmd = [
        'ffmpeg',
        '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', 'clip_list.txt',
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '18',
        '-pix_fmt', 'yuv420p',
        '-c:a', 'aac',
        '-b:a', '128k',
        output_path
    ]
    subprocess.run(cmd, check=True)
    os.remove('clip_list.txt')

def run_clip(video_filename: str):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    input_json = os.path.join(project_root, 'data', 'output', 'formatted_clusters.json')
    video_path = os.path.join(project_root, 'data', 'input', video_filename)
    output_dir = os.path.join(project_root, 'data', 'output', 'clips', 'output_clips')
    merged_output_path = os.path.join(project_root, 'data', 'output', 'merged', 'merged_video.mp4')
    
    clusters = load_json(input_json)
    merged_clusters = merge_clusters(clusters)
    yield 10  
    
    for progress in crop_video(video_path, merged_clusters, output_dir):
        yield 10 + (progress * 0.8) 
    
    clip_paths = [os.path.join(output_dir, f"clip_{i+1}.mp4") for i in range(len(merged_clusters))]
    merge_clips(clip_paths, merged_output_path)
    yield 100  

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process and clip video based on clusters.')
    parser.add_argument('video_filename', type=str, help='Filename of the input video file')
    args = parser.parse_args()

    for progress in run_clip(args.video_filename):
        print(f"Progress: {progress:.2f}%")