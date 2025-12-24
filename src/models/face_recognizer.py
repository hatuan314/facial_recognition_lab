import cv2
import numpy as np
from config import Config

class FaceRecognizer:
    def __init__(self):
        self._model = cv2.face.LBPHFaceRecognizer_create()
        self._is_trained = False
    
    def train(self, faces, labels):
        if len(faces) == 0:
            raise ValueError("Không có dữ liệu để train.")
        
        self._model.train(faces, np.array(labels))
        self._is_trained = True
    
    def load_model(self, model_path):
        self._model.read(model_path)
        self._is_trained = True
    
    def predict(self, face_image):
        if not self._is_trained:
            raise Exception("Model chưa được train hoặc load.")
        
        predicted_id, confidence = self._model.predict(face_image)
        return predicted_id, confidence
    
    def is_confident(self, confidence, threshold=None):
        threshold = threshold or Config.CONFIDENCE_THRESHOLD
        return confidence < threshold
    
    def save(self, filepath):
        self._model.save(filepath)
