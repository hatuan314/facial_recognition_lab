import cv2
import os
from config import Config

class FaceDetector:
    def __init__(self, cascade_path=None):
        self._cascade_path = cascade_path or Config.CASCADE_PATH
        self._cascade = None
        self._load_cascade()
    
    def _load_cascade(self):
        if not os.path.exists(self._cascade_path):
            raise FileNotFoundError(f"Không tìm thấy file cascade: {self._cascade_path}")
        self._cascade = cv2.CascadeClassifier(self._cascade_path)
    
    def detect_faces(self, gray_image, scale_factor=None, min_neighbors=None):
        scale_factor = scale_factor or Config.DETECTION_SCALE_FACTOR
        min_neighbors = min_neighbors or Config.DETECTION_MIN_NEIGHBORS
        
        faces = self._cascade.detectMultiScale(
            gray_image, 
            scale_factor, 
            min_neighbors
        )
        return faces
    
    def extract_face_roi(self, gray_image, face_rect, target_size=None):
        target_size = target_size or Config.FACE_SIZE
        x, y, w, h = face_rect
        roi = gray_image[y:y+h, x:x+w]
        roi_resized = cv2.resize(roi, target_size)
        return roi_resized
