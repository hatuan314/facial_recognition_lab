# Training - Workflow and Entrypoints

## Training Overview

The training process converts collected face images into an LBPH model capable of recognizing those faces. Training is fast (typically <10 seconds) and runs entirely on CPU.

**Algorithm:** LBPH (Local Binary Patterns Histograms)  
**Framework:** OpenCV `cv2.face` module  
**Hardware:** CPU only (no GPU required)  
**Duration:** <10 seconds for 90 images (3 people × 30 images)

---

## Training Entrypoints

### CLI Entrypoint

**Command:**
```bash
python main.py
```

**Interactive menu:**
```
1. Thu ảnh training
2. Train model         ← Select this option
3. Nhận diện realtime
4. Đánh giá accuracy   ← New evaluation option
0. Thoát
```

**Process:**
1. System scans `dataset/` directory
2. Loads all face images
3. Creates label mapping
4. Trains LBPH model
5. Saves model to `trainer/trainer.yml`
6. Saves labels to `trainer/labels.pickle`

**Note:** For evaluation metrics, use option 4 which includes train/test split and comprehensive metrics.

---

### Programmatic Entrypoint

**File:** `src/controllers/face_recognition_controller.py`  
**Method:** `FaceRecognitionController.train_model()`  
**Lines:** 52-70

**Usage:**
```python
from src.controllers.face_recognition_controller import FaceRecognitionController

controller = FaceRecognitionController()
controller.train_model()
```

**Direct model training:**
```python
from src.models.face_recognizer import FaceRecognizer
from src.models.data_manager import DataManager
import numpy as np

# Load data
data_manager = DataManager()
faces, labels, label_map = data_manager.load_training_data()

# Train model
recognizer = FaceRecognizer()
recognizer.train(faces, np.array(labels))

# Save model
data_manager.save_model(recognizer._model, label_map)
```

---

## Training Workflow

### Step-by-Step Process

#### 1. Data Loading

**Module:** `src/models/data_manager.py`  
**Function:** `DataManager.load_training_data()`

```python
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
```

**Output:**
- `faces`: List of numpy arrays (200×200 grayscale)
- `labels`: List of integers (person IDs)
- `label_map`: Dict mapping person names to IDs

**Example:**
```python
faces = [img1, img2, ..., img90]  # 90 images
labels = [0, 0, ..., 1, 1, ..., 2, 2, ...]  # 3 people
label_map = {"john_doe": 0, "jane_smith": 1, "bob_jones": 2}
```

#### 2. Model Initialization

**Module:** `src/models/face_recognizer.py`  
**Function:** `FaceRecognizer.__init__()`

```python
def __init__(self):
    self._model = cv2.face.LBPHFaceRecognizer_create()
    self._is_trained = False
```

**LBPH parameters (default):**
- `radius`: 1
- `neighbors`: 8
- `grid_x`: 8
- `grid_y`: 8

**KHÔNG XÁC MINH:** Custom LBPH parameters not exposed in Config

#### 3. Training

**Module:** `src/models/face_recognizer.py`  
**Function:** `FaceRecognizer.train(faces, labels)`

```python
def train(self, faces, labels):
    if len(faces) == 0:
        raise ValueError("Không có dữ liệu để train.")
    
    self._model.train(faces, np.array(labels))
    self._is_trained = True
```

**Process:**
1. Validate input (non-empty)
2. Call OpenCV LBPH training
3. Set trained flag

**Training algorithm:**
1. For each face image:
   - Compute Local Binary Patterns
   - Divide into 8×8 grid (64 cells)
   - Compute histogram (256 bins) per cell
   - Store histogram with label
2. Build internal model structure

**No explicit loss function:** LBPH is not gradient-based

#### 4. Model Serialization

**Module:** `src/models/data_manager.py`  
**Function:** `DataManager.save_model(model, label_map)`

```python
def save_model(self, model, label_map):
    model_path = os.path.join(self._trainer_dir, Config.TRAINER_MODEL_FILE)
    labels_path = os.path.join(self._trainer_dir, Config.LABELS_PICKLE_FILE)
    
    model.save(model_path)
    
    with open(labels_path, "wb") as f:
        pickle.dump(label_map, f)
```

**Saves two files:**
1. `trainer/trainer.yml` - LBPH model (YAML format)
2. `trainer/labels.pickle` - Label mapping (Python pickle)

---

## Loss Function

**KHÔNG XÁC MINH - LBPH does not use an explicit loss function.**

**Algorithm characteristics:**
- Non-parametric method
- No gradient descent
- No backpropagation
- Stores histograms directly

**Comparison metric:**
- Chi-Square distance between histograms
- Used during inference, not training
- Lower distance = more similar

---

## Optimizer

**KHÔNG XÁC MINH - No optimizer (not applicable to LBPH).**

LBPH is not a neural network, so concepts like SGD, Adam, learning rate, etc. do not apply.

**Training is deterministic:**
- No random initialization
- No stochastic updates
- Same data → same model

---

## Learning Rate Scheduler

**KHÔNG XÁC MINH - Not applicable (no learning rate in LBPH).**

---

## Automatic Mixed Precision (AMP)

**KHÔNG XÁC MINH - Not applicable (CPU-only, no GPU training).**

LBPH training runs on CPU and does not benefit from AMP.

---

## Distributed Data Parallel (DDP)

**KHÔNG XÁC MINH - Not implemented (single-process training).**

Current implementation:
- Single-process training
- No multi-GPU support
- No distributed training

**Training is fast enough (<10s) that distribution is unnecessary.**

---

## Training Logging

### Console Output

**Module:** `src/views/console_view.py`  
**Functions:** `ConsoleView.show_info()`, `ConsoleView.show_success()`

**Current logging:**
```python
self._console_view.show_info("Đang load dữ liệu training...")
self._console_view.show_info(f"Đang train model với {len(faces)} ảnh...")
self._console_view.show_info("Đang lưu model...")
self._console_view.show_success(f"Training hoàn tất! Đã train {len(label_map)} người.")
```

**Output example:**
```
ℹ Đang load dữ liệu training...
ℹ Đang train model với 90 ảnh...
ℹ Đang lưu model...
✓ Training hoàn tất! Đã train 3 người.
```

### Structured Logging

**KHÔNG XÁC MINH - No structured logging (Python logging module not used).**

**Proposed enhancement:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Usage
logger.info(f"Loading training data from {dataset_dir}")
logger.info(f"Training with {len(faces)} images, {len(label_map)} people")
logger.info(f"Model saved to {model_path}")
```

---

## Training Seeds

**KHÔNG XÁC MINH - No seed setting (LBPH is deterministic).**

**Deterministic behavior:**
- LBPH algorithm is deterministic
- No random initialization
- No stochastic processes
- Same input data → same model output

**No seed required for reproducibility.**

---

## Training Artifacts

### Generated Files

**Location:** `trainer/` directory

**Files:**
1. **trainer.yml**
   - LBPH model in OpenCV YAML format
   - Size: ~4-5 MB (for 3 people, 90 images)
   - Contains: Histograms, parameters, labels

2. **labels.pickle**
   - Python pickle format
   - Size: <1 KB
   - Contains: `{"person_name": id}` mapping

### Artifact Management

**Current behavior:**
- Overwrites existing files on each training
- No versioning
- No backup

**KHÔNG XÁC MINH:** Artifact versioning, metadata tracking

**Proposed enhancement:**
```python
import datetime

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
model_path = f"trainer/checkpoints/model_{timestamp}.yml"
labels_path = f"trainer/checkpoints/labels_{timestamp}.pickle"
metadata_path = f"trainer/metadata/metadata_{timestamp}.json"

# Save with timestamp
model.save(model_path)

# Save metadata
metadata = {
    "timestamp": timestamp,
    "num_people": len(label_map),
    "num_images": len(faces),
    "people": list(label_map.keys()),
    "config": {
        "face_size": Config.FACE_SIZE,
        "confidence_threshold": Config.CONFIDENCE_THRESHOLD
    }
}

with open(metadata_path, 'w') as f:
    json.dump(metadata, f, indent=2)
```

---

## Training Configuration

### Configurable Parameters

**From `config.py`:**

```python
# Data collection
DEFAULT_SAMPLES = 30  # Images per person

# Image processing
FACE_SIZE = (200, 200)  # Must match training and inference

# Detection (affects data quality)
DETECTION_SCALE_FACTOR = 1.3
DETECTION_MIN_NEIGHBORS = 5
```

**LBPH parameters (hardcoded):**
- `radius`: 1
- `neighbors`: 8
- `grid_x`: 8
- `grid_y`: 8

**To customize LBPH parameters:**
```python
# Modify src/models/face_recognizer.py
def __init__(self):
    self._model = cv2.face.LBPHFaceRecognizer_create(
        radius=2,        # Increased from 1
        neighbors=16,    # Increased from 8
        grid_x=10,       # Increased from 8
        grid_y=10        # Increased from 8
    )
```

---

## Training Best Practices

### Data Quality

**Before training:**
1. ✅ Verify dataset has sufficient images (≥20 per person)
2. ✅ Check image quality (not blurry, good lighting)
3. ✅ Ensure consistent conditions across images
4. ✅ Remove duplicate or poor-quality images

### Training Process

**During training:**
1. ✅ Ensure `dataset/` directory is populated
2. ✅ Check console output for errors
3. ✅ Verify model files are created in `trainer/`
4. ✅ Test recognition after training

### Post-Training

**After training:**
1. ✅ Test with known faces (should recognize correctly)
2. ✅ Test with unknown faces (should show "Unknown")
3. ✅ Adjust `CONFIDENCE_THRESHOLD` if needed
4. ✅ Backup model files if important

---

## Training Validation

**KHÔNG XÁC MINH - No validation during training.**

**Current behavior:**
- No train/val split
- No accuracy metrics
- No validation loop
- No early stopping

**Proposed validation:**
```python
from sklearn.model_selection import train_test_split

# Split data
X_train, X_val, y_train, y_val = train_test_split(
    faces, labels, test_size=0.2, stratify=labels, random_state=42
)

# Train on training set only
recognizer.train(X_train, y_train)

# Validate
correct = 0
for face, true_label in zip(X_val, y_val):
    pred_id, conf = recognizer.predict(face)
    if pred_id == true_label and conf < Config.CONFIDENCE_THRESHOLD:
        correct += 1

accuracy = correct / len(X_val)
print(f"Validation Accuracy: {accuracy:.2%}")
```

---

## Incremental Training

**KHÔNG XÁC MINH - Incremental training not supported.**

**Current behavior:**
- Full retraining required for any data changes
- Cannot add new person without retraining
- Cannot update existing person without retraining

**LBPH limitation:** OpenCV's LBPH does not support incremental updates

**Workaround:** Fast retraining (<10s) makes this less critical

---

## Training Errors

### Common Errors

#### Error: "Không có dữ liệu trong dataset"
**Cause:** `dataset/` directory is empty  
**Solution:** Collect training data first (option 1 in menu)

#### Error: "need at least one array to concatenate"
**Cause:** No valid images found in dataset  
**Solution:** 
- Check `dataset/` has subdirectories with images
- Verify image file extensions (.jpg, .png, .jpeg)
- Check file permissions

#### Error: Model file not created
**Cause:** Permission issues or disk full  
**Solution:**
- Check write permissions for `trainer/` directory
- Verify sufficient disk space

---

## Training Performance

### Timing Benchmarks

**KHÔNG XÁC MINH - No formal benchmarks available.**

**Approximate timings (MacBook Pro M1):**
- 30 images (1 person): ~2 seconds
- 90 images (3 people): ~5 seconds
- 300 images (10 people): ~15 seconds

**Factors affecting speed:**
- Number of images
- Image size (200×200 is optimal)
- CPU performance
- Disk I/O speed

### Memory Usage

**KHÔNG XÁC MINH - No memory profiling available.**

**Approximate memory:**
- Loading 90 images: ~40 MB
- Training process: ~100 MB peak
- Final model: ~5 MB on disk

**No memory issues expected for typical datasets (<1000 images).**

---

## Training Monitoring

**KHÔNG XÁC MINH - No training monitoring tools.**

**Current state:**
- No progress bars
- No ETA estimates
- No resource monitoring
- No tensorboard/wandb integration

**Proposed enhancement:**
```python
from tqdm import tqdm

# Progress bar for data loading
for file in tqdm(files, desc="Loading images"):
    img = cv2.imread(file)
    faces.append(img)

# Training progress
print("Training model...")
start_time = time.time()
recognizer.train(faces, labels)
duration = time.time() - start_time
print(f"Training completed in {duration:.2f}s")
```

---

## Related Documentation

- [Pipeline](pipeline.md) - Training in context of full pipeline
- [Models](models.md) - LBPH algorithm details
- [Datasets](datasets.md) - Training data format
- [Configs](configs.md) - Training configuration
- [Evaluation](evaluation.md) - Post-training evaluation

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-15
