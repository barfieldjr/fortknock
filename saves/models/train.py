import os
import subprocess
from pathlib import Path

def list_dataset_directories():
    print("Listing dataset directories:")
    subprocess.run(['ls', 'data/images/train'])
    subprocess.run(['ls', 'data/images/val'])
    subprocess.run(['ls', 'data/images/test'])

def display_dataset_yaml():
    print("Displaying dataset.yaml:")
    subprocess.run(['cat', 'data/dataset.yaml'])

def clone_yolov5_repo():
    if not Path('yolov5').exists():
        print("Cloning YOLOv5 repository:")
        subprocess.run(['git', 'clone', 'https://github.com/ultralytics/yolov5'])
    os.chdir('yolov5')

def install_requirements():
    print("Installing requirements:")
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'])

def train_model():
    print("Training the model:")
    subprocess.run([
        'python', 'train.py',
        '--img', '640',
        '--batch', '16',
        '--epochs', '60',
        '--data', '../data/dataset.yaml',
        '--weights', 'yolov5s.pt'
    ])

def save_model_weights():
    print("Saving model weights:")
    Path('../model').mkdir(parents=True, exist_ok=True)
    subprocess.run(['cp', 'runs/train/exp/weights/best.pt', '../model/knockdown_model_weights.pt'])

def evaluate_model():
    print("Evaluating the model:")
    subprocess.run([
        'python', 'val.py',
        '--weights', '../model/knockdown_model_weights.pt',
        '--data', '../data/dataset.yaml',
        '--task', 'test'
    ])

def main():
    os.makedirs('data/images/train', exist_ok=True)
    os.makedirs('data/images/val', exist_ok=True)
    os.makedirs('data/images/test', exist_ok=True)
    
    list_dataset_directories()
    display_dataset_yaml()
    clone_yolov5_repo()
    install_requirements()
    train_model()
    save_model_weights()
    evaluate_model()

if __name__ == "__main__":
    main()
