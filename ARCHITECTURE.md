# Kiến Trúc MVC và SOLID Principles

## 📐 Tổng Quan Kiến Trúc

Project đã được refactor theo mô hình **MVC (Model-View-Controller)** và tuân thủ các nguyên tắc **SOLID**.

### Cấu Trúc Thư Mục

```
facial_recognition_lab/
├── main.py                          # Entry point (8 dòng code)
├── config.py                        # Configuration và constants
│
├── src/                             # Source code package
│   ├── __init__.py
│   │
│   ├── models/                      # Business Logic & Data
│   │   ├── __init__.py
│   │   ├── camera_service.py       # Quản lý camera (SRP)
│   │   ├── face_detector.py        # Phát hiện khuôn mặt (SRP)
│   │   ├── face_recognizer.py      # Nhận diện khuôn mặt (SRP)
│   │   └── data_manager.py         # Quản lý dữ liệu (SRP)
│   │
│   ├── views/                       # Presentation Layer
│   │   ├── __init__.py
│   │   └── console_view.py         # Console & Video UI
│   │
│   └── controllers/                 # Application Logic
│       ├── __init__.py
│       └── face_recognition_controller.py
│
├── dataset/                         # Training data
├── trainer/                         # Trained models
└── haarcascades/                    # Cascade files
```

---

## 🎯 SOLID Principles Implementation

### 1. **S - Single Responsibility Principle (SRP)**

Mỗi class chỉ có **một lý do để thay đổi**.

#### **Before (main.py cũ)**: ❌
```python
# 1 file làm mọi thứ: camera, detection, recognition, UI, data
def capture_faces():  # camera + detection + UI + data
def train_model():    # data + training + saving
def recognize():      # camera + detection + recognition + UI
```

#### **After**: ✅

| Class | Trách Nhiệm Duy Nhất |
|-------|---------------------|
| `CameraService` | Quản lý camera (open, read, release) |
| `FaceDetector` | Phát hiện khuôn mặt bằng Haar Cascade |
| `FaceRecognizer` | Train và predict với LBPH |
| `DataManager` | Lưu/đọc dữ liệu (ảnh, model, labels) |
| `ConsoleView` | Hiển thị text trên console |
| `VideoView` | Hiển thị video và annotations |
| `FaceRecognitionController` | Điều phối workflow |

**Lợi ích**:
- Dễ maintain: Sửa camera logic → chỉ sửa `CameraService`
- Dễ test: Test riêng từng component
- Code rõ ràng: Tên class = chức năng

---

### 2. **O - Open/Closed Principle (OCP)**

**Mở cho mở rộng, đóng cho sửa đổi**.

#### Example 1: Camera Service

```python
# Có thể extend để hỗ trợ video file
class VideoFileService(CameraService):
    def __init__(self, video_path):
        super().__init__(camera_index=video_path)
    
    # Không cần sửa code CameraService gốc
```

#### Example 2: Face Detector

```python
# Có thể thay thế bằng detector khác
class DNNFaceDetector(FaceDetector):
    def __init__(self):
        # Dùng DNN thay vì Haar Cascade
        self.net = cv2.dnn.readNetFromCaffe(...)
    
    def detect_faces(self, image):
        # Override với DNN detection
        pass
```

**Lợi ích**:
- Thêm tính năng mới không phá code cũ
- Dễ dàng swap implementations

---

### 3. **L - Liskov Substitution Principle (LSP)**

**Subclass có thể thay thế base class mà không làm hỏng chương trình**.

#### Implementation:

```python
# Base behavior trong CameraService
class CameraService:
    def open(self): ...
    def read(self): ...
    def release(self): ...

# Subclass có thể thay thế
class WebcamService(CameraService):
    pass  # Hoạt động y hệt

class IPCameraService(CameraService):
    def open(self):
        # Kết nối qua IP, nhưng vẫn trả về camera object
        return cv2.VideoCapture(self.ip_url)
    # read() và release() vẫn hoạt động đúng

# Controller không cần biết loại camera nào
controller._camera_service = IPCameraService("http://...")
controller.capture_faces("john")  # Vẫn hoạt động!
```

**Lợi ích**:
- Polymorphism hoạt động đúng
- Code linh hoạt, dễ thay thế

---

### 4. **I - Interface Segregation Principle (ISP)**

**Không ép client implement methods không dùng đến**.

#### Implementation:

```python
# ❌ BAD: Fat interface
class FaceProcessor:
    def detect(self): ...
    def recognize(self): ...
    def train(self): ...
    def save_data(self): ...
    # Nếu chỉ cần detect, phải implement tất cả!

# ✅ GOOD: Tách thành interfaces nhỏ
class IFaceDetector:
    def detect_faces(self, image): pass

class IFaceRecognizer:
    def predict(self, face): pass
    def train(self, faces, labels): pass

class IDataPersistence:
    def save_model(self, model): pass
    def load_model(self): pass
```

**Trong project**:
- `FaceDetector`: Chỉ có detection methods
- `FaceRecognizer`: Chỉ có recognition methods
- `DataManager`: Chỉ có data persistence methods

**Lợi ích**:
- Class nhỏ gọn, focused
- Không implement code thừa

---

### 5. **D - Dependency Inversion Principle (DIP)**

**Depend on abstractions, not concretions**.

#### Before: ❌
```python
def capture_faces():
    cam = cv2.VideoCapture(0)  # Hardcoded dependency
    cascade = cv2.CascadeClassifier(path)  # Hardcoded
    # Không thể test, không thể thay thế
```

#### After: ✅
```python
class FaceRecognitionController:
    def __init__(self, 
                 camera_service=None,      # Dependency Injection
                 face_detector=None,
                 face_recognizer=None,
                 data_manager=None):
        
        # Dùng default hoặc inject custom
        self._camera_service = camera_service or CameraService()
        self._face_detector = face_detector or FaceDetector()
        self._face_recognizer = face_recognizer or FaceRecognizer()
        self._data_manager = data_manager or DataManager()
```

**Lợi ích cho Testing**:
```python
# Mock cho unit test
class MockCamera:
    def read(self):
        return True, fake_image

# Inject mock
controller = FaceRecognitionController(camera_service=MockCamera())
controller.capture_faces("test")  # Test mà không cần camera thật!
```

---

## 🏛️ MVC Pattern Breakdown

### **Model Layer** (Business Logic)

Chứa **business logic** và **data operations**.

#### `src/models/camera_service.py`
- Quản lý vòng đời camera (open, read, release)
- Context manager support (`with` statement)
```python
with CameraService() as cam:
    ret, frame = cam.read()
# Tự động release
```

#### `src/models/face_detector.py`
- Load Haar Cascade
- Detect faces từ grayscale image
- Extract và resize ROI
```python
detector = FaceDetector()
faces = detector.detect_faces(gray_image)
roi = detector.extract_face_roi(gray_image, face_rect)
```

#### `src/models/face_recognizer.py`
- Train LBPH model
- Predict faces
- Confidence thresholding
```python
recognizer = FaceRecognizer()
recognizer.train(faces, labels)
id, conf = recognizer.predict(face_image)
is_confident = recognizer.is_confident(conf)
```

#### `src/models/data_manager.py`
- Tạo thư mục cho người mới
- Lưu ảnh training
- Load training dataset
- Save/load model và labels
```python
manager = DataManager()
manager.save_face_image("john", image, 0)
faces, labels, map = manager.load_training_data()
manager.save_model(model, label_map)
```

---

### **View Layer** (Presentation)

Chỉ chứa **UI logic**, không có business logic.

#### `src/views/console_view.py`

**ConsoleView**: Text-based UI
```python
view = ConsoleView()
view.show_menu()
choice = view.get_menu_choice()
view.show_success("Training hoàn tất!")
view.show_error("Không tìm thấy camera")
```

**VideoView**: OpenCV window UI
```python
video = VideoView()
video.show_frame("Window", frame)
video.draw_face_rectangle(frame, (x,y,w,h), color)
video.draw_text(frame, "John", (x, y-10))
key = video.wait_key()
```

**Tách biệt rõ ràng**:
- Console: stdin/stdout
- Video: OpenCV windows
- Dễ thay thế (GUI toolkit khác)

---

### **Controller Layer** (Application Logic)

Điều phối **Models** và **Views**, chứa workflow logic.

#### `src/controllers/face_recognition_controller.py`

```python
class FaceRecognitionController:
    def __init__(self):
        # Khởi tạo tất cả dependencies
        self._camera_service = CameraService()
        self._face_detector = FaceDetector()
        self._face_recognizer = FaceRecognizer()
        self._data_manager = DataManager()
        self._console_view = ConsoleView()
        self._video_view = VideoView()
    
    def capture_faces(self, name, samples):
        # Workflow: Camera → Detect → Save → UI
        with self._camera_service as cam:
            while ...:
                ret, frame = cam.read()
                faces = self._face_detector.detect_faces(gray)
                
                for face in faces:
                    roi = self._face_detector.extract_face_roi(...)
                    self._data_manager.save_face_image(...)
                    self._video_view.draw_face_rectangle(...)
                
                self._video_view.show_frame(...)
    
    def train_model(self):
        # Workflow: Load Data → Train → Save → UI
        faces, labels, map = self._data_manager.load_training_data()
        self._face_recognizer.train(faces, labels)
        self._data_manager.save_model(...)
        self._console_view.show_success(...)
    
    def recognize_faces(self):
        # Workflow: Load Model → Camera → Detect → Predict → UI
        model_path, map = self._data_manager.load_model_and_labels()
        self._face_recognizer.load_model(model_path)
        
        with self._camera_service as cam:
            while ...:
                faces = self._face_detector.detect_faces(...)
                id, conf = self._face_recognizer.predict(roi)
                self._video_view.draw_text(...)
```

**Controller là "dây dẫn"** nối Models và Views.

---

## 📦 Configuration Management

### `config.py`

Centralized configuration, tuân thủ **Don't Repeat Yourself (DRY)**.

```python
class Config:
    # Paths (động, cross-platform)
    PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
    DATASET_DIR = os.path.join(PROJECT_PATH, "dataset")
    TRAINER_DIR = os.path.join(PROJECT_PATH, "trainer")
    CASCADE_PATH = os.path.join(PROJECT_PATH, "haarcascades", ...)
    
    # File names
    TRAINER_MODEL_FILE = "trainer.yml"
    LABELS_PICKLE_FILE = "labels.pickle"
    
    # Algorithm parameters
    DEFAULT_SAMPLES = 30
    FACE_SIZE = (200, 200)
    CONFIDENCE_THRESHOLD = 80
    DETECTION_SCALE_FACTOR = 1.3
    DETECTION_MIN_NEIGHBORS = 5
    
    # Hardware
    CAMERA_INDEX = 0
```

**Lợi ích**:
- ✅ Single source of truth
- ✅ Dễ thay đổi (ví dụ: threshold từ 80 → 70)
- ✅ Không hardcode magic numbers
- ✅ Có thể override dễ dàng

---

## 🔄 Data Flow

### 1. Capture Faces Flow

```
User Input (name)
    ↓
Controller.capture_faces()
    ↓
CameraService.open() → Camera stream
    ↓
FaceDetector.detect_faces() → Face locations
    ↓
FaceDetector.extract_face_roi() → Face image (200×200)
    ↓
DataManager.save_face_image() → Disk
    ↓
VideoView.draw_rectangle() → Visual feedback
    ↓
VideoView.show_frame() → Display
```

### 2. Train Model Flow

```
Controller.train_model()
    ↓
DataManager.load_training_data() → (faces[], labels[], map{})
    ↓
FaceRecognizer.train() → LBPH model
    ↓
DataManager.save_model() → trainer.yml, labels.pickle
    ↓
ConsoleView.show_success() → User feedback
```

### 3. Recognition Flow

```
Controller.recognize_faces()
    ↓
DataManager.load_model_and_labels() → Model + mapping
    ↓
FaceRecognizer.load_model()
    ↓
CameraService.read() → Frame
    ↓
FaceDetector.detect_faces() → Face locations
    ↓
FaceRecognizer.predict() → (id, confidence)
    ↓
if confident → Get name from reverse_map
    ↓
VideoView.draw_text() → Display name
```

---

## 🧪 Testability

Kiến trúc mới **dễ test** gấp nhiều lần.

### Unit Test Examples

#### Test FaceDetector
```python
def test_face_detector():
    detector = FaceDetector(cascade_path="test_cascade.xml")
    test_image = cv2.imread("test_face.jpg", cv2.IMREAD_GRAYSCALE)
    
    faces = detector.detect_faces(test_image)
    
    assert len(faces) > 0
    assert faces[0][2] > 50  # width > 50px
```

#### Test DataManager với Mock
```python
def test_save_face_image(tmp_path):
    manager = DataManager(dataset_dir=tmp_path)
    test_image = np.zeros((200, 200), dtype=np.uint8)
    
    filepath = manager.save_face_image("john", test_image, 0)
    
    assert os.path.exists(filepath)
    assert filepath.endswith("john_0.jpg")
```

#### Test Controller với Mocks
```python
def test_capture_faces():
    mock_camera = MockCameraService()
    mock_detector = MockFaceDetector()
    mock_data = MockDataManager()
    
    controller = FaceRecognitionController(
        camera_service=mock_camera,
        face_detector=mock_detector,
        data_manager=mock_data
    )
    
    controller.capture_faces("test", samples=5)
    
    assert mock_data.save_count == 5
```

---

## 🚀 Extensibility

### Thêm Tính Năng Mới Dễ Dàng

#### 1. Thêm Face Recognition Algorithm Mới

```python
# src/models/facenet_recognizer.py
class FaceNetRecognizer:
    def train(self, faces, labels):
        # Sử dụng FaceNet thay vì LBPH
        pass
    
    def predict(self, face):
        # Deep learning prediction
        pass

# Trong controller
controller._face_recognizer = FaceNetRecognizer()
# Code khác không đổi!
```

#### 2. Thêm GUI View

```python
# src/views/gui_view.py
import tkinter as tk

class GUIView:
    def show_menu(self):
        # Tkinter menu thay vì console
        pass
    
    def get_person_name(self):
        # Dialog box
        return simpledialog.askstring(...)

# Trong controller
controller._console_view = GUIView()
```

#### 3. Thêm Database Storage

```python
# src/models/database_manager.py
class DatabaseManager(DataManager):
    def save_face_image(self, name, image, count):
        # Lưu vào PostgreSQL thay vì file
        blob = cv2.imencode('.jpg', image)[1].tobytes()
        db.execute("INSERT INTO faces ...")
```

---

## 📊 So Sánh Before/After

| Tiêu Chí | Before (main.py cũ) | After (MVC + SOLID) |
|----------|-------------------|-------------------|
| **Số dòng main.py** | 129 | 8 |
| **Số files** | 1 | 11 |
| **Testability** | Rất khó | Rất dễ |
| **Maintainability** | Khó (mọi thứ lộn xộn) | Dễ (tách biệt rõ ràng) |
| **Extensibility** | Phải sửa code cũ | Thêm class mới |
| **Reusability** | Không thể reuse | Có thể reuse từng component |
| **Coupling** | Cao (tightly coupled) | Thấp (loosely coupled) |
| **Cohesion** | Thấp (làm nhiều việc) | Cao (focused) |
| **SOLID** | Không tuân thủ | Tuân thủ đầy đủ |

---

## 🎓 Best Practices Applied

### 1. **Context Managers**
```python
with CameraService() as cam:
    frame = cam.read()
# Tự động cleanup
```

### 2. **Dependency Injection**
```python
controller = FaceRecognitionController(
    camera_service=CustomCamera(),
    face_detector=DNNDetector()
)
```

### 3. **Configuration Over Code**
```python
# Thay đổi threshold không cần sửa code
Config.CONFIDENCE_THRESHOLD = 70
```

### 4. **Error Handling**
```python
try:
    controller.train_model()
except ValueError as e:
    view.show_error(str(e))
```

### 5. **Type Hints** (có thể thêm)
```python
def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
    ...
```

---

## 🔧 Migration Guide

### Chạy Code Mới

```bash
# Giống hệt như trước
python3 main.py

# Hoặc
python main.py
```

### Import Modules Mới

```python
# Trong code của bạn
from src.models.face_detector import FaceDetector
from src.models.data_manager import DataManager

detector = FaceDetector()
faces = detector.detect_faces(image)
```

### Tùy Chỉnh Configuration

```python
# custom_config.py
from config import Config

Config.CONFIDENCE_THRESHOLD = 70
Config.DEFAULT_SAMPLES = 50

# Chạy với custom config
from src.controllers.face_recognition_controller import FaceRecognitionController
controller = FaceRecognitionController()
controller.run()
```

---

## 📝 Summary

### SOLID Principles Checklist

- ✅ **S**: Mỗi class một trách nhiệm
- ✅ **O**: Mở rộng dễ, không sửa code cũ
- ✅ **L**: Subclass thay thế được base class
- ✅ **I**: Interfaces nhỏ, tập trung
- ✅ **D**: Depend on abstractions

### MVC Pattern Checklist

- ✅ **Model**: Business logic & data
- ✅ **View**: Presentation chỉ
- ✅ **Controller**: Điều phối workflow

### Code Quality

- ✅ Clean code, dễ đọc
- ✅ Testable
- ✅ Maintainable
- ✅ Extensible
- ✅ Reusable
- ✅ Cross-platform

---

**Refactored by**: MVC Architecture Team  
**Date**: 2024  
**Principles**: SOLID, DRY, KISS, YAGNI
