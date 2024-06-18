import torch
import cv2
import matplotlib.pyplot as plt
import random
from pathlib import Path
import os

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
    # Draw middle two-quarters horizontally
    x1, x2 = img_width // 4, 3 * img_width // 4
    y1, y2 = img_height // 2, img_height
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

def infer(image_path):
    print(f"Starting inference on image: {image_path}")
    
    # Load the model
    model_path = 'saves/models/knockdown_model_weights.pt'
    yolo_repo_path = './yolov5'
    
    if not os.path.exists(yolo_repo_path):
        raise FileNotFoundError(f"YOLOv5 directory not found at {yolo_repo_path}")
    if not os.path.exists(os.path.join(yolo_repo_path, 'hubconf.py')):
        raise FileNotFoundError(f"hubconf.py not found in {yolo_repo_path}")
    
    model = torch.hub.load(yolo_repo_path, 'custom', path=model_path, source='local')
    model.conf = 0.3  # Lower confidence threshold
    print("Model loaded successfully.")
    
    # Read and resize the image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
    img_resized = cv2.resize(img, (640, 640))
    img_height, img_width, _ = img_resized.shape
    print("Image loaded and resized successfully.")
    
    # Draw the specified region bounds
    draw_region_bounds(img_resized)
    
    # Run inference
    results = model(img_resized)
    print("Inference completed.")
    
    # Draw bounding boxes
    num_detections = results.xyxy[0].shape[0]
    print(f"Number of detections: {num_detections}")
    for *box, conf, cls in results.xyxy[0]:
        print(f"Detection: Class={model.names[int(cls)]}, Confidence={conf:.2f}")
        if is_within_region(box, img_width, img_height):
            label = f'{model.names[int(cls)]} {conf:.2f}'
            plot_one_box(box, img_resized, label=label, color=(255, 0, 0), line_thickness=2)
            print(f"Location (within region): {box}")
        else:
            print("Detection outside specified region, ignoring.")
    
    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(10, 10))
    plt.imshow(img_rgb)
    plt.axis('off')
    plt.savefig("/app/inference_output.png")  # Save the output image
    plt.show()

def get_random_image_path(directory):
    image_extensions = ['.jpg', '.jpeg', '.png']
    image_paths = [p for p in Path(directory).glob('*') if p.suffix.lower() in image_extensions]
    if not image_paths:
        raise FileNotFoundError(f"No images found in directory {directory}")
    return random.choice(image_paths)

if __name__ == "__main__":
    test_image_directory = 'data/raw/obj_train_data/images/test'
    image_path = get_random_image_path(test_image_directory)
    print(f"Selected image for inference: {image_path}")
    infer(image_path)
