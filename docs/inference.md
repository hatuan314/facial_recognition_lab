# Inference - Recognition API and Deployment

## Inference Overview

Inference is the process of using a trained LBPH model to recognize faces in real-time from webcam video. The system detects faces, extracts features, predicts identities, and displays results with bounding boxes and labels.

**Mode:** Real-time video recognition  
**Hardware:** CPU only (no GPU required)  
**Latency:** <50ms per face (typical)  
**Throughput:** 20+ FPS on modern CPU

---

## Inference Entrypoints

### CLI Entrypoint

**Command:**
```bash
python main.py
```

**Interactive menu:**
```
1. Thu ảnh training
2. Train model
3. Nhận diện realtime  ← Select this option
0. Thoát
```

**Process:**
1. Loads trained model from `trainer/trainer.yml`
2. Loads label mapping from `trainer/labels.pickle`
3. Opens webcam
4. Continuously detects and recognizes faces
5. Displays annotated video with names
6. Press 'q' to exit

---

### Programmatic Entrypoint

**File:** `src/controllers/face_recognition_controller.py`  
**Method:** `FaceRecognitionController.recognize_faces()`  
**Lines:** 72-115

**Usage:**
```python
from src.controllers.face_recognition_controller import FaceRecognitionController

controller = FaceRecognitionController()
controller.recognize_faces()
```

**Direct inference:**
```python
from src.models.face_recognizer import FaceRecognizer
from src.models.face_detector import FaceDetector
from src.models.data_manager import DataManager
import cv2

# Load model
data_manager = DataManager()
model_path, label_map = data_manager.load_model_and_labels()

recognizer = FaceRecognizer()
recognizer.load_model(model_path)

# Create reverse mapping
reverse_map = {v: k for k, v in label_map.items()}

# Detect and recognize
detector = FaceDetector()
frame = cv2.imread("test_image.jpg")
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
faces = detector.detect_faces(gray)

for (x, y, w, h) in faces:
    roi = detector.extract_face_roi(gray, (x, y, w, h))
    pred_id, confidence = recognizer.predict(roi)
    
    if recognizer.is_confident(confidence):
        name = reverse_map[pred_id]
    else:
        name = "Unknown"
    
    print(f"Detected: {name} (confidence: {confidence:.2f})")
```

---

## Inference Pipeline

### Step-by-Step Process

#### 1. Model Loading

**Module:** `src/models/data_manager.py`  
**Function:** `DataManager.load_model_and_labels()`

```python
def load_model_and_labels(self):
    model_path = os.path.join(self._trainer_dir, Config.TRAINER_MODEL_FILE)
    labels_path = os.path.join(self._trainer_dir, Config.LABELS_PICKLE_FILE)
    
    if not os.path.exists(model_path) or not os.path.exists(labels_path):
        raise FileNotFoundError("Model hoặc labels chưa được train.")
    
    with open(labels_path, "rb") as f:
        label_map = pickle.load(f)
    
    return model_path, label_map
```

**Module:** `src/models/face_recognizer.py`  
**Function:** `FaceRecognizer.load_model(model_path)`

```python
def load_model(self, model_path):
    self._model.read(model_path)
    self._is_trained = True
```

**Loaded artifacts:**
- LBPH model with trained histograms
- Label mapping: `{"john_doe": 0, "jane_smith": 1, ...}`

#### 2. Reverse Mapping Creation

**Controller (inline):**
```python
reverse_map = {v: k for k, v in label_map.items()}
# {0: "john_doe", 1: "jane_smith", ...}
```

**Purpose:** Convert numeric predictions back to person names

#### 3. Camera Initialization

**Module:** `src/models/camera_service.py`  
**Function:** `CameraService.open()`

```python
with self._camera_service as cam:
    # Camera automatically released on exit
```

#### 4. Frame Processing Loop

**Per frame:**

1. **Capture frame:**
   ```python
   ret, frame = cam.read()
   # frame: (H, W, 3) BGR uint8
   ```

2. **Convert to grayscale:**
   ```python
   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   # gray: (H, W) uint8
   ```

3. **Detect faces:**
   ```python
   faces = self._face_detector.detect_faces(gray)
   # faces: [(x, y, w, h), ...]
   ```

4. **For each detected face:**
   
   a. **Extract ROI:**
   ```python
   roi = self._face_detector.extract_face_roi(gray, face_rect)
   # roi: (200, 200) uint8
   ```
   
   b. **Predict identity:**
   ```python
   predicted_id, confidence = self._face_recognizer.predict(roi)
   # predicted_id: int (0, 1, 2, ...)
   # confidence: float (Chi-Square distance)
   ```
   
   c. **Apply threshold:**
   ```python
   if self._face_recognizer.is_confident(confidence):
       name = reverse_map[predicted_id]
       color = (0, 255, 0)  # Green
   else:
       name = "Unknown"
       color = (0, 0, 255)  # Red
   ```
   
   d. **Draw annotations:**
   ```python
   self._video_view.draw_face_rectangle(frame, face_rect, color)
   self._video_view.draw_text(frame, name, (x, y-10), color)
   ```

5. **Display frame:**
   ```python
   self._video_view.show_frame("Recognition", frame)
   ```

6. **Check exit condition:**
   ```python
   if self._video_view.wait_key() == ord('q'):
       break
   ```

---

## Inference API

### Core Functions

#### Predict Single Face

**Function:** `FaceRecognizer.predict(face_image)`

**Input contract:**
```python
face_image: np.ndarray
    - Shape: (200, 200)
    - Dtype: uint8
    - Range: [0, 255]
    - Color: Grayscale
```

**Output contract:**
```python
(predicted_id: int, confidence: float)

predicted_id:
    - Numeric label (0, 1, 2, ...)
    - Maps to person via label_map

confidence:
    - Chi-Square distance
    - Range: [0, ∞)
    - Lower = more confident
```

**Example:**
```python
roi = cv2.imread("face.jpg", cv2.IMREAD_GRAYSCALE)
roi = cv2.resize(roi, (200, 200))

pred_id, conf = recognizer.predict(roi)
print(f"Predicted ID: {pred_id}, Confidence: {conf:.2f}")
```

#### Confidence Thresholding

**Function:** `FaceRecognizer.is_confident(confidence, threshold=None)`

```python
def is_confident(self, confidence, threshold=None):
    threshold = threshold or Config.CONFIDENCE_THRESHOLD
    return confidence < threshold
```

**Usage:**
```python
if recognizer.is_confident(confidence):
    print("High confidence prediction")
else:
    print("Low confidence - reject as Unknown")
```

---

## Batch Inference

**KHÔNG XÁC MINH - Batch inference not currently implemented.**

**Proposed batch API:**

```python
def predict_batch(self, face_images):
    """Predict multiple faces at once"""
    results = []
    for face in face_images:
        pred_id, conf = self.predict(face)
        results.append((pred_id, conf))
    return results

# Usage
faces = [face1, face2, face3, ...]
results = recognizer.predict_batch(faces)

for i, (pred_id, conf) in enumerate(results):
    print(f"Face {i}: ID={pred_id}, Conf={conf:.2f}")
```

**Benefits:**
- Process multiple faces from single frame
- Potential for optimization (though LBPH doesn't parallelize well)

---

## Inference Latency

### Performance Characteristics

**KHÔNG XÁC MINH - No formal latency benchmarks.**

**Approximate timings (MacBook Pro M1):**

| Operation | Latency | Notes |
|-----------|---------|-------|
| Face detection | 10-20ms | Haar Cascade |
| ROI extraction | <1ms | Simple crop + resize |
| LBPH prediction | 5-10ms | Per face |
| Visualization | 2-5ms | Drawing + display |
| **Total per frame** | **20-40ms** | **25-50 FPS** |

**Factors affecting latency:**
- Frame resolution (higher = slower detection)
- Number of faces in frame
- CPU performance
- Detection parameters (scale_factor, min_neighbors)

### Latency Optimization

**Strategies:**

1. **Reduce frame resolution:**
   ```python
   ret, frame = cam.read()
   frame = cv2.resize(frame, (640, 480))  # Downscale
   ```

2. **Skip frames:**
   ```python
   frame_count = 0
   while True:
       ret, frame = cam.read()
       frame_count += 1
       
       if frame_count % 2 == 0:  # Process every 2nd frame
           continue
       
       # Process frame
   ```

3. **Adjust detection parameters:**
   ```python
   # Faster but less accurate
   Config.DETECTION_SCALE_FACTOR = 1.5  # Increase from 1.3
   Config.DETECTION_MIN_NEIGHBORS = 3   # Decrease from 5
   ```

4. **Multi-threading (advanced):**
   ```python
   import threading
   import queue
   
   frame_queue = queue.Queue(maxsize=2)
   result_queue = queue.Queue(maxsize=2)
   
   def capture_thread():
       while True:
           ret, frame = cam.read()
           frame_queue.put(frame)
   
   def process_thread():
       while True:
           frame = frame_queue.get()
           # Detect and recognize
           result_queue.put(annotated_frame)
   
   # Start threads
   threading.Thread(target=capture_thread, daemon=True).start()
   threading.Thread(target=process_thread, daemon=True).start()
   ```

---

## Postprocessing

### Confidence-Based Filtering

**Current implementation:**
```python
if confidence < Config.CONFIDENCE_THRESHOLD:
    name = reverse_map[predicted_id]
    color = (0, 255, 0)  # Green
else:
    name = "Unknown"
    color = (0, 0, 255)  # Red
```

**Threshold tuning:**
- Lower (60-70): Stricter, fewer false positives
- Higher (90-100): Lenient, more false positives
- Default (80): Balanced

### Temporal Smoothing

**KHÔNG XÁC MINH - Not currently implemented.**

**Proposed smoothing:**
```python
from collections import deque

class TemporalSmoother:
    def __init__(self, window_size=5):
        self.history = deque(maxlen=window_size)
    
    def smooth(self, pred_id, confidence):
        self.history.append((pred_id, confidence))
        
        # Majority voting
        from collections import Counter
        ids = [p[0] for p in self.history]
        most_common = Counter(ids).most_common(1)[0][0]
        
        return most_common

# Usage
smoother = TemporalSmoother(window_size=5)
smoothed_id = smoother.smooth(pred_id, confidence)
```

**Benefits:**
- Reduces flickering between predictions
- More stable recognition in video
- Filters out single-frame errors

### Multi-Face Handling

**Current behavior:**
- Processes all detected faces independently
- Each face gets separate prediction and annotation

**Example with multiple faces:**
```python
faces = detector.detect_faces(gray)  # [(x1,y1,w1,h1), (x2,y2,w2,h2)]

for (x, y, w, h) in faces:
    roi = detector.extract_face_roi(gray, (x, y, w, h))
    pred_id, conf = recognizer.predict(roi)
    
    # Each face annotated independently
    name = reverse_map[pred_id] if conf < 80 else "Unknown"
    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
    cv2.putText(frame, name, (x, y-10), ...)
```

---

## Deployment Considerations

### Local Deployment

**Current deployment:**
- Runs on local machine
- Requires webcam access
- Interactive GUI (OpenCV windows)

**Requirements:**
```bash
pip install opencv-contrib-python numpy
```

**Permissions:**
- Camera access (macOS: System Preferences → Security & Privacy)
- File system access for model loading

### Server Deployment

**KHÔNG XÁC MINH - Server deployment not currently supported.**

**Proposed REST API:**

```python
from flask import Flask, request, jsonify
import base64
import numpy as np

app = Flask(__name__)

# Load model once at startup
recognizer = FaceRecognizer()
recognizer.load_model("trainer/trainer.yml")

@app.route('/recognize', methods=['POST'])
def recognize():
    # Receive base64 encoded image
    image_data = request.json['image']
    image_bytes = base64.b64decode(image_data)
    
    # Decode image
    nparr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Process
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detect_faces(gray)
    
    results = []
    for face_rect in faces:
        roi = detector.extract_face_roi(gray, face_rect)
        pred_id, conf = recognizer.predict(roi)
        
        results.append({
            'bbox': face_rect.tolist(),
            'person_id': int(pred_id),
            'person_name': reverse_map.get(pred_id, "Unknown"),
            'confidence': float(conf)
        })
    
    return jsonify({'faces': results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Client usage:**
```python
import requests
import base64

with open("test_image.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

response = requests.post('http://localhost:5000/recognize', 
                        json={'image': image_data})
results = response.json()
print(results)
```

### Edge Deployment

**KHÔNG XÁC MINH - Edge deployment not tested.**

**Considerations:**
- LBPH is lightweight (good for edge)
- CPU-only (no GPU required)
- Small model size (~5MB)
- Fast inference (<50ms)

**Potential platforms:**
- Raspberry Pi 4
- NVIDIA Jetson Nano
- Intel NUC
- Mobile devices (with OpenCV Mobile)

### Docker Deployment

**KHÔNG XÁC MINH - Docker not currently provided.**

**Proposed Dockerfile:**

```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port (if running as server)
EXPOSE 5000

# Run application
CMD ["python", "main.py"]
```

**Build and run:**
```bash
docker build -t facial-recognition-lab .
docker run -it --rm \
    --device=/dev/video0 \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    facial-recognition-lab
```

---

## Inference Monitoring

**KHÔNG XÁC MINH - No monitoring currently implemented.**

**Proposed metrics:**

```python
import time
from collections import deque

class InferenceMonitor:
    def __init__(self):
        self.latencies = deque(maxlen=100)
        self.predictions = []
    
    def log_inference(self, latency, pred_id, confidence):
        self.latencies.append(latency)
        self.predictions.append({
            'timestamp': time.time(),
            'pred_id': pred_id,
            'confidence': confidence
        })
    
    def get_stats(self):
        return {
            'mean_latency': np.mean(self.latencies),
            'p95_latency': np.percentile(self.latencies, 95),
            'fps': 1000 / np.mean(self.latencies),
            'total_predictions': len(self.predictions)
        }

# Usage
monitor = InferenceMonitor()

start = time.time()
pred_id, conf = recognizer.predict(roi)
latency = (time.time() - start) * 1000  # ms

monitor.log_inference(latency, pred_id, conf)

# Periodic stats
if frame_count % 100 == 0:
    stats = monitor.get_stats()
    print(f"FPS: {stats['fps']:.1f}, Latency: {stats['mean_latency']:.1f}ms")
```

---

## Inference Errors

### Common Issues

#### Error: "Model hoặc labels chưa được train"
**Cause:** Model files not found  
**Solution:** Train model first (option 2 in menu)

#### Error: "Không mở được camera"
**Cause:** Camera unavailable or in use  
**Solution:**
- Close other applications using camera
- Check camera permissions
- Try different camera index

#### Issue: Always shows "Unknown"
**Cause:** Confidence threshold too low or poor training  
**Solution:**
- Increase `Config.CONFIDENCE_THRESHOLD` to 90-100
- Collect more training data
- Retrain model

#### Issue: Wrong person recognized
**Cause:** Confidence threshold too high or similar appearances  
**Solution:**
- Decrease `Config.CONFIDENCE_THRESHOLD` to 60-70
- Collect more diverse training data
- Check for similar-looking people in dataset

#### Issue: Low FPS / Laggy
**Cause:** High resolution or slow CPU  
**Solution:**
- Reduce frame resolution
- Skip frames (process every Nth frame)
- Increase `DETECTION_SCALE_FACTOR`

---

## Inference Best Practices

### DO:
- ✅ Test in conditions similar to training
- ✅ Ensure good lighting
- ✅ Keep face frontal (±15° angle)
- ✅ Maintain consistent distance from camera
- ✅ Monitor confidence scores
- ✅ Tune threshold based on use case

### DON'T:
- ❌ Use in drastically different lighting
- ❌ Expect recognition with extreme angles
- ❌ Rely on single-frame predictions (use temporal smoothing)
- ❌ Ignore "Unknown" predictions (they're important)
- ❌ Run inference without training first

---

## Related Documentation

- [Pipeline](pipeline.md) - Inference in full pipeline
- [Models](models.md) - LBPH prediction details
- [Training](training.md) - Model training
- [Configs](configs.md) - Inference configuration
- [Troubleshooting](troubleshooting.md) - Inference issues

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-15
