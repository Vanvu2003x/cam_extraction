# detect_fire.py
import cv2
from ultralytics import YOLO

# Load model 1 lần duy nhất khi import
model = YOLO("../models/train-2.pt")

def detect_fire(frame):
    """
    Input: frame (numpy array, BGR)
    Output: True nếu model phát hiện cháy, False nếu không
    """
    results = model.predict(source=frame, verbose=False)[0] 
    return len(results.boxes) > 0
