# Models - Architecture and Contracts

## Model Overview

The facial recognition system uses **LBPH (Local Binary Patterns Histograms)**, a classical computer vision algorithm for texture-based face recognition. LBPH is implemented via OpenCV's `cv2.face.LBPHFaceRecognizer_create()`.

**Algorithm:** LBPH (Local Binary Patterns Histograms)  
**Implementation:** OpenCV `cv2.face` module  
**Type:** Classical ML (not deep learning)  
**Training:** Supervised learning with labeled face images

---

## LBPH Algorithm

### Theory

LBPH recognizes faces by analyzing texture patterns:

1. **Local Binary Patterns (LBP):** For each pixel, compare with 8 neighbors to create binary pattern
2. **Histograms:** Divide image into grid, compute histogram of LBP values per cell
3. **Comparison:** Use Chi-Square distance to compare histograms

### Algorithm Steps

#### Step 1: Compute Local Binary Pattern

For each pixel (center):
```
Original 3×3 neighborhood:    Comparison with center (51):
  40  50  60                    0  0  1
  45  51  62         →          0  X  1
  43  48  55                    0  0  1

Binary pattern: 10110001 → Decimal: 177
```

**Rules:**
- If neighbor ≥ center: 1
- If neighbor < center: 0
- Create 8-bit binary number from 8 neighbors
- Convert to decimal (0-255)

#### Step 2: Create Histograms

1. Divide image into grid (default: 8×8 = 64 cells)
2. For each cell, create histogram of LBP values (256 bins)
3. Concatenate all histograms into feature vector

**Feature dimensions:** 64 cells × 256 bins = **16,384 features**

#### Step 3: Training

Store histograms for each labeled face image:
```
Person 0: [hist_img0, hist_img1, ..., hist_imgN]
Person 1: [hist_img0, hist_img1, ..., hist_imgM]
...
```

#### Step 4: Recognition

1. Compute histogram for query face
2. Compare with all stored histograms using Chi-Square distance
3. Return label with minimum distance

**Chi-Square distance formula:**
```
χ² = Σ [(H1(i) - H2(i))² / (H1(i) + H2(i))]
```

Where H1, H2 are histograms to compare.

---

## Model Architecture

### LBPH Parameters

**File:** `src/models/face_recognizer.py`  
**Creation:** `cv2.face.LBPHFaceRecognizer_create()`

**Default parameters (OpenCV):**
```python
model = cv2.face.LBPHFaceRecognizer_create(
    radius=1,        # Radius for LBP
    neighbors=8,     # Number of sample points
    grid_x=8,        # Horizontal grid cells
    grid_y=8,        # Vertical grid cells
    threshold=80.0   # Confidence threshold (not used in current implementation)
)
```

**Parameter descriptions:**

| Parameter | Default | Range | Impact |
|-----------|---------|-------|--------|
| `radius` | 1 | 1-3 | Larger = more context, less detail |
| `neighbors` | 8 | 4-16 | More = more features, slower |
| `grid_x` | 8 | 4-16 | More cells = more spatial info |
| `grid_y` | 8 | 4-16 | More cells = more spatial info |
| `threshold` | 80.0 | 0-∞ | Confidence cutoff (handled externally) |

**Current implementation:** Uses default parameters (not configurable via Config)

---

## Input/Output Contract

### Training Input

**Function:** `FaceRecognizer.train(faces, labels)`

**Input contract:**
```python
faces: List[np.ndarray]
    - Type: List of numpy arrays
    - Shape per image: (200, 200)
    - Dtype: uint8
    - Range: [0, 255]
    - Color: Grayscale (single channel)
    - Count: N images (typically 20-100 per person)

labels: np.ndarray
    - Type: Numpy array
    - Shape: (N,)
    - Dtype: int32
    - Range: [0, num_people)
    - Mapping: Corresponds to faces list
```

**Example:**
```python
faces = [img1, img2, img3, ...]  # 90 images total
labels = np.array([0, 0, 0, ..., 1, 1, ..., 2, 2, ...])  # 3 people
# Person 0: 30 images
# Person 1: 30 images
# Person 2: 30 images
```

**Output:** Trained model (internal state updated)

---

### Inference Input

**Function:** `FaceRecognizer.predict(face_image)`

**Input contract:**
```python
face_image: np.ndarray
    - Shape: (200, 200)
    - Dtype: uint8
    - Range: [0, 255]
    - Color: Grayscale
    - Preprocessing: Must match training images
```

**Output contract:**
```python
(predicted_id, confidence)

predicted_id: int
    - Label of predicted person
    - Range: [0, num_people)
    - Maps to label_map via labels.pickle

confidence: float
    - Chi-Square distance
    - Range: [0, ∞)
    - Interpretation: LOWER = MORE CONFIDENT
    - Typical range: 0-150
```

**Confidence interpretation:**
- `< 50`: Very confident match
- `50-80`: Confident match (default accepts)
- `80-100`: Uncertain (default rejects)
- `> 100`: Very different (definitely reject)

---

## Model Serialization

### Save Format

**Function:** `model.save(filepath)`  
**File:** `trainer/trainer.yml`  
**Format:** YAML (OpenCV format)

**File structure:**
```yaml
%YAML:1.0
---
opencv_storage:
  format: 3
  my_lbph:
    radius: 1
    neighbors: 8
    grid_x: 8
    grid_y: 8
    histograms: [...]  # Histogram data
    labels: [...]      # Numeric labels
```

**File size:** ~4-5 MB for 3 people with 30 images each

**Characteristics:**
- Human-readable (text format)
- Cross-platform compatible
- OpenCV-specific format
- Contains all trained histograms

---

### Load Format

**Function:** `model.read(filepath)`  
**File:** `trainer/trainer.yml`

**Requirements:**
- File must exist
- File must be valid OpenCV YAML
- Model must be created before loading: `cv2.face.LBPHFaceRecognizer_create()`

**Example:**
```python
model = cv2.face.LBPHFaceRecognizer_create()
model.read("trainer/trainer.yml")
# Model now ready for prediction
```

---

## Label Mapping

### Storage

**File:** `trainer/labels.pickle`  
**Format:** Python pickle (binary)

**Content:**
```python
label_map: Dict[str, int]
# Example:
{
    "john_doe": 0,
    "jane_smith": 1,
    "bob_jones": 2
}
```

**Usage:**
```python
import pickle

# Save
with open("trainer/labels.pickle", "wb") as f:
    pickle.dump(label_map, f)

# Load
with open("trainer/labels.pickle", "rb") as f:
    label_map = pickle.load(f)

# Reverse mapping for inference
reverse_map = {v: k for k, v in label_map.items()}
# {0: "john_doe", 1: "jane_smith", 2: "bob_jones"}
```

---

## Model Checkpoints

### Checkpoint Strategy

**KHÔNG XÁC MINH - No versioning or checkpointing currently implemented.**

**Current behavior:**
- Single model file: `trainer/trainer.yml`
- Overwritten on each training
- No history or versioning
- No metadata (training date, accuracy, etc.)

**Proposed enhancement:**

```
trainer/
├── checkpoints/
│   ├── model_20260115_230000.yml
│   ├── model_20260115_230500.yml
│   └── ...
├── metadata/
│   ├── model_20260115_230000.json
│   └── ...
├── trainer.yml          # Latest model (symlink or copy)
└── labels.pickle        # Latest labels
```

**Metadata example:**
```json
{
  "timestamp": "2026-01-15T23:00:00Z",
  "num_people": 3,
  "num_images": 90,
  "images_per_person": {"john_doe": 30, "jane_smith": 30, "bob_jones": 30},
  "config": {
    "face_size": [200, 200],
    "confidence_threshold": 80
  }
}
```

---

## Model Export

### ONNX Export

**KHÔNG XÁC MINH - ONNX export not currently supported.**

LBPH is an OpenCV-specific algorithm with no direct ONNX export. Would require:
1. Custom ONNX operator implementation
2. Or reimplementation in PyTorch/TensorFlow
3. Or use as preprocessing + simple classifier

**Not applicable for current implementation.**

---

### TorchScript Export

**KHÔNG XÁC MINH - TorchScript export not applicable.**

LBPH is not a PyTorch model, so TorchScript export is not relevant.

---

### Deployment Format

**Current deployment:**
- OpenCV YAML format (`trainer.yml`)
- Requires OpenCV with `cv2.face` module
- Platform: Any system with opencv-contrib-python

**Deployment requirements:**
```bash
pip install opencv-contrib-python
```

**No GPU required:** LBPH runs on CPU only

---

## Postprocessing

### Confidence Thresholding

**Module:** `src/models/face_recognizer.py`  
**Function:** `FaceRecognizer.is_confident(confidence, threshold=None)`

```python
def is_confident(self, confidence, threshold=None):
    threshold = threshold or Config.CONFIDENCE_THRESHOLD
    return confidence < threshold
```

**Usage in inference:**
```python
predicted_id, confidence = model.predict(face_image)

if confidence < Config.CONFIDENCE_THRESHOLD:
    name = reverse_map[predicted_id]  # Known person
else:
    name = "Unknown"  # Reject as unknown
```

**Threshold tuning:**
- Lower threshold (60-70): Fewer false positives, more "Unknown"
- Higher threshold (90-100): More false positives, fewer "Unknown"
- Default (80): Balanced

---

### Label Decoding

**Process:**
1. Model predicts numeric ID (0, 1, 2, ...)
2. Look up ID in reverse mapping
3. Return person name

**Example:**
```python
# Load label mapping
with open("trainer/labels.pickle", "rb") as f:
    label_map = pickle.load(f)

# Create reverse mapping
reverse_map = {v: k for k, v in label_map.items()}
# {0: "john_doe", 1: "jane_smith", 2: "bob_jones"}

# Decode prediction
predicted_id = 1
name = reverse_map[predicted_id]  # "jane_smith"
```

---

### Visualization

**Module:** `src/views/console_view.py`  
**Functions:** `VideoView.draw_face_rectangle()`, `VideoView.draw_text()`

**Postprocessing for display:**
```python
# Determine color based on confidence
if confidence < threshold:
    color = (0, 255, 0)  # Green = known
    name = reverse_map[predicted_id]
else:
    color = (0, 0, 255)  # Red = unknown
    name = "Unknown"

# Draw on frame
cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
```

---

## Model Limitations

### Algorithmic Limitations

1. **Pose variation:** Poor performance on non-frontal faces (>30° rotation)
2. **Lighting sensitivity:** Sensitive to dramatic lighting changes
3. **Scale sensitivity:** Requires consistent face size (handled by resize)
4. **Occlusion:** Poor with glasses, masks, or partial occlusion
5. **Aging:** Accuracy degrades as subjects age
6. **Accuracy:** Lower than modern deep learning methods

### Performance Characteristics

**Strengths:**
- ✅ Fast inference (CPU-friendly)
- ✅ Small model size (~5MB)
- ✅ Low memory footprint
- ✅ Deterministic (no randomness)
- ✅ Interpretable (histogram comparison)

**Weaknesses:**
- ❌ Lower accuracy than deep learning
- ❌ Sensitive to pose and lighting
- ❌ No transfer learning
- ❌ Limited to frontal faces

---

## Model Comparison

**KHÔNG XÁC MINH - No alternative models currently implemented.**

**Comparison with other algorithms:**

| Algorithm | Accuracy | Speed | Model Size | GPU Required |
|-----------|----------|-------|------------|--------------|
| **LBPH** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | No |
| Eigenfaces | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | No |
| Fisherfaces | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | No |
| FaceNet | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | Yes |
| ArcFace | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | Yes |

---

## Model Retraining

### When to Retrain

**Required retraining scenarios:**
1. Adding new person to dataset
2. Removing person from dataset
3. Adding more images for existing person
4. Changing `Config.FACE_SIZE`
5. Changing LBPH parameters (if customized)

**Not required:**
1. Changing `Config.CONFIDENCE_THRESHOLD` (inference-only)
2. Changing detection parameters (detection-only)
3. Changing camera settings

### Retraining Process

**Command:**
```bash
python main.py
> Choose: 2  # Train model
```

**Process:**
1. Scans `dataset/` directory
2. Loads all images
3. Creates/updates label mapping
4. Trains LBPH model
5. Saves `trainer.yml` and `labels.pickle`

**Duration:** Typically <10 seconds for 3 people with 30 images each

---

## Model Validation

**KHÔNG XÁC MINH - No validation metrics currently computed.**

**Proposed validation:**

```python
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

# Split data
X_train, X_val, y_train, y_val = train_test_split(
    faces, labels, test_size=0.2, stratify=labels
)

# Train
model.train(X_train, y_train)

# Validate
predictions = []
for face in X_val:
    pred_id, conf = model.predict(face)
    predictions.append(pred_id)

# Metrics
accuracy = accuracy_score(y_val, predictions)
cm = confusion_matrix(y_val, predictions)

print(f"Validation Accuracy: {accuracy:.2%}")
print(f"Confusion Matrix:\n{cm}")
```

---

## Related Documentation

- [Pipeline](pipeline.md) - How model fits in pipeline
- [Training](training.md) - Training workflow
- [Inference](inference.md) - Inference API
- [Configs](configs.md) - Model configuration
- [Datasets](datasets.md) - Input data format

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-15
