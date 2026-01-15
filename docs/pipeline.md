# Pipeline - CV Workflow

## End-to-End Pipeline Overview

The facial recognition system consists of three main phases:

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 1: DATA COLLECTION                                        │
└─────────────────────────────────────────────────────────────────┘
Camera Stream → Grayscale → Face Detection → ROI Extraction → 
Resize → Save to Disk

┌─────────────────────────────────────────────────────────────────┐
│ PHASE 2: TRAINING                                               │
└─────────────────────────────────────────────────────────────────┘
Load Images → Label Mapping → LBPH Training → Model Serialization

┌─────────────────────────────────────────────────────────────────┐
│ PHASE 3: INFERENCE                                              │
└─────────────────────────────────────────────────────────────────┘
Camera Stream → Grayscale → Face Detection → ROI Extraction → 
LBPH Prediction → Thresholding → Label Mapping → Visualization
```

---

## Phase 1: Data Collection Pipeline

### Entry Point
**File:** `src/controllers/face_recognition_controller.py`  
**Method:** `capture_faces(person_name, samples=30)`  
**Line:** 18-50

### Step-by-Step Flow

#### 1.1 Camera Initialization
**Module:** `src/models/camera_service.py`  
**Function:** `CameraService.open()`

```python
# Input: camera_index (default: 0)
# Output: cv2.VideoCapture object
# Shape: N/A
```

**Contract:**
- Opens camera device at specified index
- Raises exception if camera unavailable
- Supports context manager protocol

#### 1.2 Frame Capture
**Module:** `src/models/camera_service.py`  
**Function:** `CameraService.read()`

```python
# Input: None
# Output: (ret: bool, frame: np.ndarray)
# Shape: frame = (H, W, 3) BGR uint8
# Range: [0, 255]
```

**Typical dimensions:** 640×480 or 1280×720 (camera dependent)

#### 1.3 Grayscale Conversion
**Module:** Controller (inline)  
**Function:** `cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)`

```python
# Input: frame (H, W, 3) BGR
# Output: gray (H, W) grayscale
# Range: [0, 255] uint8
```

**Rationale:** Haar Cascade and LBPH work on grayscale images

#### 1.4 Face Detection
**Module:** `src/models/face_detector.py`  
**Function:** `FaceDetector.detect_faces(gray_image)`

```python
# Input: gray_image (H, W) uint8
# Output: faces = [(x, y, w, h), ...]
# Parameters:
#   - scale_factor: 1.3 (from Config)
#   - min_neighbors: 5 (from Config)
```

**Algorithm:** Haar Cascade (haarcascade_frontalface_default.xml)

**Output format:**
- `x, y`: Top-left corner coordinates
- `w, h`: Bounding box width and height
- Multiple faces can be detected per frame

#### 1.5 ROI Extraction
**Module:** `src/models/face_detector.py`  
**Function:** `FaceDetector.extract_face_roi(gray_image, face_rect)`

```python
# Input: 
#   - gray_image: (H, W) uint8
#   - face_rect: (x, y, w, h)
# Process:
#   - roi = gray_image[y:y+h, x:x+w]
#   - roi_resized = cv2.resize(roi, (200, 200))
# Output: roi_resized (200, 200) uint8
```

**Contract:**
- All ROIs normalized to 200×200 pixels
- Maintains aspect ratio through resize
- Grayscale single channel

#### 1.6 Data Persistence
**Module:** `src/models/data_manager.py`  
**Function:** `DataManager.save_face_image(person_name, image, count)`

```python
# Input:
#   - person_name: str (e.g., "john_doe")
#   - image: (200, 200) uint8 grayscale
#   - count: int (image index)
# Output: filepath (str)
# Storage: dataset/<person_name>/<person_name>_<count>.jpg
```

**File format:** JPEG (lossy compression)

#### 1.7 Visualization
**Module:** `src/views/console_view.py`  
**Function:** `VideoView.draw_face_rectangle()`, `VideoView.show_frame()`

```python
# Draws green rectangle on detected faces
# Displays frame in OpenCV window
# Exit condition: 'q' key or count >= samples
```

---

## Phase 2: Training Pipeline

### Entry Point
**File:** `src/controllers/face_recognition_controller.py`  
**Method:** `train_model()`  
**Line:** 52-70

### Step-by-Step Flow

#### 2.1 Dataset Loading
**Module:** `src/models/data_manager.py`  
**Function:** `DataManager.load_training_data()`

```python
# Input: dataset/ directory
# Process:
#   - os.walk() through dataset/
#   - Filter .jpg, .png, .jpeg files
#   - Extract person name from directory
# Output:
#   - faces: List[np.ndarray] - (200, 200) uint8 images
#   - labels: List[int] - numeric labels
#   - label_map: Dict[str, int] - {"person_name": id}
```

**Example:**
```python
faces = [img1, img2, ..., imgN]  # N images
labels = [0, 0, 0, ..., 1, 1, ..., 2, 2, ...]
label_map = {"john_doe": 0, "jane_smith": 1, "bob_jones": 2}
```

#### 2.2 Label Mapping
**Module:** `src/models/data_manager.py` (inline in load_training_data)

```python
# Auto-generates numeric IDs for each person
# Mapping stored in label_map dictionary
# IDs assigned sequentially (0, 1, 2, ...)
```

**Contract:**
- Directory name = person identifier
- One-to-one mapping: person → unique ID
- Consistent across training sessions (alphabetical order via os.walk)

#### 2.3 LBPH Training
**Module:** `src/models/face_recognizer.py`  
**Function:** `FaceRecognizer.train(faces, labels)`

```python
# Input:
#   - faces: List[np.ndarray] - grayscale (200, 200)
#   - labels: np.ndarray - int32 labels
# Algorithm: cv2.face.LBPHFaceRecognizer_create()
# Process:
#   1. Compute Local Binary Patterns for each image
#   2. Divide image into 8×8 grid (64 cells)
#   3. Create histogram (256 bins) per cell
#   4. Store histograms for each label
# Output: Trained model (internal state)
```

**LBPH Parameters (default):**
- `radius`: 1
- `neighbors`: 8
- `grid_x`: 8
- `grid_y`: 8

**Feature dimensions:** 64 cells × 256 bins = 16,384 features per image

#### 2.4 Model Serialization
**Module:** `src/models/data_manager.py`  
**Function:** `DataManager.save_model(model, label_map)`

```python
# Saves two files:
# 1. trainer/trainer.yml - LBPH model (YAML format)
# 2. trainer/labels.pickle - label mapping (Python pickle)
```

**File formats:**
- `trainer.yml`: OpenCV YAML (text-based, ~4-5MB)
- `labels.pickle`: Binary pickle (small, <1KB)

---

## Phase 3: Inference Pipeline

### Entry Point
**File:** `src/controllers/face_recognition_controller.py`  
**Method:** `recognize_faces()`  
**Line:** 72-115

### Step-by-Step Flow

#### 3.1 Model Loading
**Module:** `src/models/data_manager.py`  
**Function:** `DataManager.load_model_and_labels()`

```python
# Loads:
#   - trainer/trainer.yml → model_path
#   - trainer/labels.pickle → label_map
# Returns: (model_path: str, label_map: Dict[str, int])
```

**Module:** `src/models/face_recognizer.py`  
**Function:** `FaceRecognizer.load_model(model_path)`

```python
# Loads trained LBPH model from YAML file
# Sets internal state to trained
```

#### 3.2 Reverse Mapping Creation
**Module:** Controller (inline)

```python
# Creates reverse mapping: ID → name
reverse_map = {v: k for k, v in label_map.items()}
# Example: {0: "john_doe", 1: "jane_smith", 2: "bob_jones"}
```

#### 3.3 Frame Processing Loop
**Same as Phase 1 steps 1.2-1.5:**
- Camera capture
- Grayscale conversion
- Face detection
- ROI extraction

#### 3.4 Face Recognition
**Module:** `src/models/face_recognizer.py`  
**Function:** `FaceRecognizer.predict(face_image)`

```python
# Input: face_image (200, 200) uint8 grayscale
# Output: (predicted_id: int, confidence: float)
# Algorithm: Chi-Square distance between histograms
```

**Confidence interpretation:**
- Lower = more confident
- Typical range: 0-150
- < 50: Very confident
- 50-80: Confident
- ≥ 80: Uncertain (threshold)

#### 3.5 Confidence Thresholding
**Module:** `src/models/face_recognizer.py`  
**Function:** `FaceRecognizer.is_confident(confidence)`

```python
# Input: confidence (float)
# Threshold: 80 (from Config.CONFIDENCE_THRESHOLD)
# Output: bool (True if confident)
```

**Decision logic:**
```python
if confidence < 80:
    name = reverse_map[predicted_id]  # Known person
    color = (0, 255, 0)  # Green
else:
    name = "Unknown"  # Unknown person
    color = (0, 0, 255)  # Red
```

#### 3.6 Visualization
**Module:** `src/views/console_view.py`  
**Functions:** `VideoView.draw_face_rectangle()`, `VideoView.draw_text()`

```python
# Draws on frame:
#   - Bounding box (green/red)
#   - Person name (above box)
# Display: cv2.imshow("Recognition", frame)
```

---

## Data Flow Summary

### Data Shapes Throughout Pipeline

| Stage | Data | Shape | Type | Range |
|-------|------|-------|------|-------|
| Camera capture | frame | (H, W, 3) | uint8 | [0, 255] |
| Grayscale | gray | (H, W) | uint8 | [0, 255] |
| Face detection | faces | [(x,y,w,h), ...] | int | N/A |
| ROI extraction | roi | (200, 200) | uint8 | [0, 255] |
| Training input | faces list | List[(200,200)] | uint8 | [0, 255] |
| Training labels | labels | (N,) | int32 | [0, num_people) |
| Prediction input | roi | (200, 200) | uint8 | [0, 255] |
| Prediction output | (id, conf) | (int, float) | - | id≥0, conf≥0 |

### Critical Assumptions

1. **Image size:** All training and inference images are 200×200 pixels
2. **Color space:** Grayscale (single channel)
3. **Data type:** uint8 (0-255 range)
4. **Face detection:** Frontal faces only (Haar Cascade limitation)
5. **Lighting:** Consistent lighting between training and inference
6. **Distance:** Similar camera distance for training and inference

---

## Pipeline Optimization Opportunities

**KHÔNG XÁC MINH - Proposed enhancements:**

### Data Collection
- [ ] Add frame skipping (process every Nth frame)
- [ ] Add quality checks (blur detection, lighting)
- [ ] Add face alignment preprocessing

### Training
- [ ] Add data augmentation (flip, rotation, brightness)
- [ ] Add train/val split
- [ ] Add cross-validation

### Inference
- [ ] Add multi-threading (capture vs. process)
- [ ] Add frame buffering
- [ ] Add batch processing for multiple faces
- [ ] Add temporal smoothing (track across frames)

---

## Related Documentation

- [Models](models.md) - LBPH algorithm details
- [Datasets](datasets.md) - Data format specifications
- [Training](training.md) - Training workflow
- [Inference](inference.md) - Inference API
- [Configs](configs.md) - Pipeline parameters

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-15
