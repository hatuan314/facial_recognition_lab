import cv2
from config import Config

class CameraService:
    def __init__(self, camera_index=None):
        self._camera_index = camera_index or Config.CAMERA_INDEX
        self._camera = None
    
    def open(self):
        self._camera = cv2.VideoCapture(self._camera_index)
        if not self._camera.isOpened():
            raise Exception("Không mở được camera.")
        return self._camera
    
    def read(self):
        if self._camera is None:
            raise Exception("Camera chưa được mở.")
        return self._camera.read()
    
    def release(self):
        if self._camera:
            self._camera.release()
            cv2.destroyAllWindows()
    
    def __enter__(self):
        return self.open()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
