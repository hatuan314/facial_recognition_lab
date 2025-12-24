import os
import cv2
import pickle
from config import Config

class DataManager:
    def __init__(self, dataset_dir=None, trainer_dir=None):
        self._dataset_dir = dataset_dir or Config.DATASET_DIR
        self._trainer_dir = trainer_dir or Config.TRAINER_DIR
    
    def create_person_directory(self, person_name):
        person_dir = os.path.join(self._dataset_dir, person_name)
        os.makedirs(person_dir, exist_ok=True)
        return person_dir
    
    def save_face_image(self, person_name, image, count):
        person_dir = self.create_person_directory(person_name)
        filename = f"{person_name}_{count}.jpg"
        filepath = os.path.join(person_dir, filename)
        cv2.imwrite(filepath, image)
        return filepath
    
    def load_training_data(self):
        faces = []
        labels = []
        label_map = {}
        idx = 0
        
        for root, dirs, files in os.walk(self._dataset_dir):
            for file in files:
                if file.endswith((".jpg", ".png", ".jpeg")):
                    path = os.path.join(root, file)
                    person = os.path.basename(root)
                    
                    if person not in label_map:
                        label_map[person] = idx
                        idx += 1
                    
                    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                    img = cv2.resize(img, Config.FACE_SIZE)
                    faces.append(img)
                    labels.append(label_map[person])
        
        return faces, labels, label_map
    
    def save_model(self, model, label_map):
        model_path = os.path.join(self._trainer_dir, Config.TRAINER_MODEL_FILE)
        labels_path = os.path.join(self._trainer_dir, Config.LABELS_PICKLE_FILE)
        
        model.save(model_path)
        
        with open(labels_path, "wb") as f:
            pickle.dump(label_map, f)
    
    def load_model_and_labels(self):
        model_path = os.path.join(self._trainer_dir, Config.TRAINER_MODEL_FILE)
        labels_path = os.path.join(self._trainer_dir, Config.LABELS_PICKLE_FILE)
        
        if not os.path.exists(model_path) or not os.path.exists(labels_path):
            raise FileNotFoundError("Model hoặc labels chưa được train.")
        
        with open(labels_path, "rb") as f:
            label_map = pickle.load(f)
        
        return model_path, label_map
