import torch
import cv2
import numpy as np

class ObjectDetector:
    def __init__(self):
        print("Loading NANO TFLite Model (High Speed)...")
        # 1. Load the NANO model
        self.model = torch.hub.load('yolov5', 'yolov5n', source='local')
        
        # 2. RESTORE NAMES (Nano TFLite sometimes forgets these)
        self.model.names = [
            'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
            'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
            'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
            'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
            'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
            'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
            'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
            'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
            'hair drier', 'toothbrush'
        ]

        # 3. LOWER CONFIDENCE (The Fix)
        # Standard was 0.5. We drop to 0.25 because Nano is less confident.
        # Configure settings
        # Increase this number to filter out fans/lamps
        self.model.conf = 0.25
        self.model.iou = 0.45   # Removes duplicate boxes
        
        # 4. DEFINE WHAT TO SEE
        # 0=Person (Vital for Face Rec), 56=Chair, 39=Bottle, 67=Cell Phone
        self.classes_to_detect = [0, 1, 2, 3, 5, 7, 39, 41, 56, 63, 67]

    def detect(self, frame):
        # Resize to square 640x640 for TFLite
        small_frame = cv2.resize(frame, (640, 640))
        
        # Run inference
        results = self.model(small_frame)
        
        # Get data
        detected_df = results.pandas().xyxy[0]
        
        # Filter for only the objects we want
        relevant_objects = detected_df[detected_df['class'].isin(self.classes_to_detect)]
        
        # Return results to main.py
        return results, relevant_objects