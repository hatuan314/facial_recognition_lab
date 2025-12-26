import cv2
from src.models.camera_service import CameraService
from src.models.face_detector import FaceDetector
from src.models.face_recognizer import FaceRecognizer
from src.models.data_manager import DataManager
from src.views.console_view import ConsoleView, VideoView
from config import Config

class FaceRecognitionController:
    def __init__(self):
        self._camera_service = CameraService()
        self._face_detector = FaceDetector()
        self._face_recognizer = FaceRecognizer()
        self._data_manager = DataManager()
        self._console_view = ConsoleView()
        self._video_view = VideoView()

    # Thêm vào face_recognition_controller.py

    def evaluate_model(self, use_cross_validation=False):
        """
        Đánh giá accuracy của model
        """
        try:
            from src.models.model_evaluator import ModelEvaluator
            
            evaluator = ModelEvaluator(test_split=0.2)
            
            if use_cross_validation:
                self._console_view.show_info("Đang chạy Cross-Validation...")
                results = evaluator.cross_validate(k_folds=5)
            else:
                self._console_view.show_info("Đang đánh giá model...")
                results = evaluator.evaluate()
                evaluator.print_report(results)
            
            return results
        
        except Exception as e:
            self._console_view.show_error(str(e))
            raise
    
    def capture_faces(self, person_name, samples=None):
        samples = samples or Config.DEFAULT_SAMPLES
        count = 0
        
        try:
            with self._camera_service as cam:
                while True:
                    ret, frame = cam.read()
                    if not ret:
                        break
                    
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = self._face_detector.detect_faces(gray)
                    
                    for face_rect in faces:
                        roi = self._face_detector.extract_face_roi(gray, face_rect)
                        self._data_manager.save_face_image(person_name, roi, count)
                        count += 1
                        
                        self._video_view.draw_face_rectangle(frame, face_rect)
                    
                    self._video_view.show_frame("Capture", frame)
                    
                    if self._video_view.wait_key() == ord('q') or count >= samples:
                        break
        
        except Exception as e:
            self._console_view.show_error(str(e))
            raise
        finally:
            self._video_view.close_all_windows()
        
        self._console_view.show_success(f"Đã thu thập {count} ảnh cho {person_name}")
    
    def train_model(self):
        try:
            self._console_view.show_info("Đang load dữ liệu training...")
            faces, labels, label_map = self._data_manager.load_training_data()
            
            if len(faces) == 0:
                raise ValueError("Không có dữ liệu trong dataset. Vui lòng thu ảnh trước.")
            
            self._console_view.show_info(f"Đang train model với {len(faces)} ảnh...")
            self._face_recognizer.train(faces, labels)
            
            self._console_view.show_info("Đang lưu model...")
            self._data_manager.save_model(self._face_recognizer._model, label_map)
            
            self._console_view.show_success(f"Training hoàn tất! Đã train {len(label_map)} người.")
        
        except Exception as e:
            self._console_view.show_error(str(e))
            raise
    
    def recognize_faces(self):
        try:
            self._console_view.show_info("Đang load model...")
            model_path, label_map = self._data_manager.load_model_and_labels()
            self._face_recognizer.load_model(model_path)
            
            reverse_map = {v: k for k, v in label_map.items()}
            
            self._console_view.show_success("Bắt đầu nhận diện. Nhấn 'q' để thoát.")
            
            with self._camera_service as cam:
                while True:
                    ret, frame = cam.read()
                    if not ret:
                        break
                    
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = self._face_detector.detect_faces(gray)
                    
                    for face_rect in faces:
                        roi = self._face_detector.extract_face_roi(gray, face_rect)
                        predicted_id, confidence = self._face_recognizer.predict(roi)
                        
                        if self._face_recognizer.is_confident(confidence):
                            name = reverse_map[predicted_id]
                            color = (0, 255, 0)
                        else:
                            name = "Unknown"
                            color = (0, 0, 255)
                        
                        x, y, w, h = face_rect
                        self._video_view.draw_face_rectangle(frame, face_rect, color)
                        self._video_view.draw_text(frame, name, (x, y - 10), color)
                    
                    self._video_view.show_frame("Recognition", frame)
                    
                    if self._video_view.wait_key() == ord('q'):
                        break
        
        except Exception as e:
            self._console_view.show_error(str(e))
            raise
        finally:
            self._video_view.close_all_windows()
    
    def run(self):
        Config.ensure_directories()
        
        while True:
            self._console_view.show_menu()
            choice = self._console_view.get_menu_choice()
            
            try:
                if choice == "1":
                    name = self._console_view.get_person_name()
                    if name:
                        self.capture_faces(name)
                    else:
                        self._console_view.show_error("Tên không được để trống.")
                
                elif choice == "2":
                    self.train_model()
                
                elif choice == "3":
                    self.recognize_faces()
                    
                elif choice == "4":
                    self.evaluate_model()
                else:
                    self._console_view.show_info("Thoát chương trình.")
                    break
            
            except Exception as e:
                self._console_view.show_error(f"Đã xảy ra lỗi: {str(e)}")
