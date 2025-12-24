import os

class Config:
    PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
    DATASET_DIR = os.path.join(PROJECT_PATH, "dataset")
    TRAINER_DIR = os.path.join(PROJECT_PATH, "trainer")
    CASCADE_PATH = os.path.join(PROJECT_PATH, "haarcascades", "haarcascade_frontalface_default.xml")
    
    TRAINER_MODEL_FILE = "trainer.yml"
    LABELS_PICKLE_FILE = "labels.pickle"
    
    DEFAULT_SAMPLES = 30
    FACE_SIZE = (200, 200)
    CONFIDENCE_THRESHOLD = 80
    
    DETECTION_SCALE_FACTOR = 1.3
    DETECTION_MIN_NEIGHBORS = 5
    
    CAMERA_INDEX = 0
    
    @classmethod
    def ensure_directories(cls):
        os.makedirs(cls.DATASET_DIR, exist_ok=True)
        os.makedirs(cls.TRAINER_DIR, exist_ok=True)
