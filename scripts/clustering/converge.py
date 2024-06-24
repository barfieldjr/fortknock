import json
import os
from typing import List, Dict, Any

def load_json(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def find_clusters(detections: List[Dict[str, Any]], time_threshold: float = 2.0, frame_gap: int = 3) -> List[List[Dict[str, Any]]]:
    clusters = []
    current_cluster = []

    for i, detection in enumerate(detections):
        if not current_cluster:
            current_cluster.append(detection)
        else:
            last_detection = current_cluster[-1]
            if (detection["timestamp"] - last_detection["timestamp"] <= time_threshold) and (detection["frame"] - last_detection["frame"] <= frame_gap):
                current_cluster.append(detection)
            else:
                clusters.append(current_cluster)
                current_cluster = [detection]
    
    if current_cluster:
        clusters.append(current_cluster)

    return clusters

def filter_clusters(clusters: List[List[Dict[str, Any]]], min_cluster_length: int = 3) -> List[List[Dict[str, Any]]]:
    filtered_clusters = []

    for cluster in clusters:
        if len(cluster) >= min_cluster_length:
            filtered_clusters.append(cluster)

    return filtered_clusters

def format_clusters(clusters: List[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    formatted_clusters = []

    for i, cluster in enumerate(clusters):
        cluster_data = {
            "cluster_id": i + 1,
            "start_frame": cluster[0]["frame"],
            "end_frame": cluster[-1]["frame"],
            "start_timestamp": cluster[0]["timestamp"],
            "end_timestamp": cluster[-1]["timestamp"],
            "detections": cluster
        }
        formatted_clusters.append(cluster_data)

    return formatted_clusters

def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    file_path = os.path.join(project_root , 'data', 'output', 'detection_timestamps.json')
    detections = load_json(file_path)

    clusters = find_clusters(detections)
    filtered_clusters = filter_clusters(clusters)
    formatted_clusters = format_clusters(filtered_clusters)

    output_path = os.path.join(project_root, 'data', 'output', 'formatted_clusters.json')
    with open(output_path, 'w') as outfile:
        json.dump(formatted_clusters, outfile, indent=4)

    for cluster in formatted_clusters:
        print(cluster)

if __name__ == "__main__":
    main()
