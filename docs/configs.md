# Configuration System

## Overview

The project uses a centralized configuration system via a Python class in `config.py`. All configuration parameters are defined as class variables, providing a single source of truth for paths, hyperparameters, and system settings.

**File:** `config.py` (root directory)  
**Pattern:** Static class with class variables  
**No external config files:** No YAML, JSON, or INI files

**Dependencies:** `requirements.txt` specifies:
- `numpy` - Array operations
- `opencv-contrib-python` - Computer vision
- `scikit-learn>=1.0.0` - Evaluation metrics (optional, fallback available)

---

## Configuration Schema

### Complete Configuration

```python
import os

class Config:
    # ============================================================
    # PATHS (Dynamic, Cross-Platform)
    # ============================================================
    PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
    DATASET_DIR = os.path.join(PROJECT_PATH, "dataset")
    TRAINER_DIR = os.path.join(PROJECT_PATH, "trainer")
    CASCADE_PATH = os.path.join(PROJECT_PATH, "haarcascades", 
                                "haarcascade_frontalface_default.xml")
    
    # ============================================================
    # FILE NAMES
    # ============================================================
    TRAINER_MODEL_FILE = "trainer.yml"
    LABELS_PICKLE_FILE = "labels.pickle"
    
    # ============================================================
    # DATA COLLECTION PARAMETERS
    # ============================================================
    DEFAULT_SAMPLES = 30              # Number of images to collect per person
    
    # ============================================================
    # IMAGE PROCESSING PARAMETERS
    # ============================================================
    FACE_SIZE = (200, 200)            # Standard face image size (width, height)
    
    # ============================================================
    # FACE DETECTION PARAMETERS (Haar Cascade)
    # ============================================================
    DETECTION_SCALE_FACTOR = 1.3      # Image pyramid scale factor
    DETECTION_MIN_NEIGHBORS = 5       # Minimum neighbors for detection
    
    # ============================================================
    # FACE RECOGNITION PARAMETERS (LBPH)
    # ============================================================
    CONFIDENCE_THRESHOLD = 80         # Recognition confidence threshold
    
    # ============================================================
    # HARDWARE CONFIGURATION
    # ============================================================
    CAMERA_INDEX = 0                  # Camera device index (0 = default)
    
    # ============================================================
    # UTILITY METHODS
    # ============================================================
    @classmethod
    def ensure_directories(cls):
        """Create required directories if they don't exist"""
        os.makedirs(cls.DATASET_DIR, exist_ok=True)
        os.makedirs(cls.TRAINER_DIR, exist_ok=True)
```

---

## Configuration Parameters

### Path Configuration

#### `PROJECT_PATH`
- **Type:** `str`
- **Value:** Dynamic (auto-detected)
- **Purpose:** Root directory of the project
- **Calculation:** `os.path.dirname(os.path.abspath(__file__))`
- **Example:** `/Users/user/facial_recognition_lab`

#### `DATASET_DIR`
- **Type:** `str`
- **Value:** `{PROJECT_PATH}/dataset`
- **Purpose:** Storage location for training images
- **Structure:** `dataset/<person_name>/<person_name>_<index>.jpg`

#### `TRAINER_DIR`
- **Type:** `str`
- **Value:** `{PROJECT_PATH}/trainer`
- **Purpose:** Storage location for trained models and labels
- **Contents:** `trainer.yml`, `labels.pickle`

#### `CASCADE_PATH`
- **Type:** `str`
- **Value:** `{PROJECT_PATH}/haarcascades/haarcascade_frontalface_default.xml`
- **Purpose:** Path to Haar Cascade classifier for face detection
- **Required:** Must exist before running

---

### Data Collection Parameters

#### `DEFAULT_SAMPLES`
- **Type:** `int`
- **Default:** `30`
- **Purpose:** Number of face images to collect per person
- **Range:** Recommended 20-100
- **Impact:** More samples = better accuracy, longer collection time

**Tuning guide:**
- 20-30: Quick testing
- 50-100: Better accuracy
- 100+: Diminishing returns

---

### Image Processing Parameters

#### `FACE_SIZE`
- **Type:** `Tuple[int, int]`
- **Default:** `(200, 200)`
- **Purpose:** Standard size for all face images (training and inference)
- **Format:** `(width, height)` in pixels
- **Constraint:** Must be consistent across training and inference

**Why 200×200:**
- Balance between detail and processing speed
- LBPH works well with this resolution
- Reasonable file size (~10-20KB per JPEG)

---

### Face Detection Parameters

#### `DETECTION_SCALE_FACTOR`
- **Type:** `float`
- **Default:** `1.3`
- **Purpose:** Scale factor for image pyramid in Haar Cascade detection
- **Range:** `1.01` to `2.0`
- **Impact:**
  - Lower (1.05-1.2): More accurate, slower, more detections
  - Higher (1.4-2.0): Faster, may miss faces

**Tuning guide:**
```python
# High accuracy, slow
DETECTION_SCALE_FACTOR = 1.1

# Balanced (default)
DETECTION_SCALE_FACTOR = 1.3

# Fast, may miss faces
DETECTION_SCALE_FACTOR = 1.5
```

#### `DETECTION_MIN_NEIGHBORS`
- **Type:** `int`
- **Default:** `5`
- **Purpose:** Minimum number of neighbor rectangles to retain detection
- **Range:** `1` to `10`
- **Impact:**
  - Lower (1-3): More detections, more false positives
  - Higher (6-10): Fewer false positives, may miss faces

**Tuning guide:**
```python
# Sensitive (more false positives)
DETECTION_MIN_NEIGHBORS = 3

# Balanced (default)
DETECTION_MIN_NEIGHBORS = 5

# Conservative (fewer false positives)
DETECTION_MIN_NEIGHBORS = 7
```

---

### Face Recognition Parameters

#### `CONFIDENCE_THRESHOLD`
- **Type:** `float`
- **Default:** `80`
- **Purpose:** Maximum confidence score to accept a recognition
- **Range:** `0` to `150+`
- **Interpretation:** Lower confidence = more certain match

**Confidence scale:**
- `< 50`: Very confident match
- `50-80`: Confident match (default accepts)
- `80-100`: Uncertain (default rejects as "Unknown")
- `> 100`: Very different

**Tuning guide:**
```python
# Strict (fewer false positives, more "Unknown")
CONFIDENCE_THRESHOLD = 60

# Balanced (default)
CONFIDENCE_THRESHOLD = 80

# Lenient (more false positives, fewer "Unknown")
CONFIDENCE_THRESHOLD = 100
```

**Trade-offs:**
- Lower threshold: Higher precision, lower recall
- Higher threshold: Lower precision, higher recall

---

### Hardware Configuration

#### `CAMERA_INDEX`
- **Type:** `int`
- **Default:** `0`
- **Purpose:** Camera device index for OpenCV VideoCapture
- **Values:**
  - `0`: Default camera (usually built-in webcam)
  - `1`, `2`, ...: External cameras
  - String: IP camera URL (requires modification)

**Multiple cameras:**
```python
# Built-in webcam
CAMERA_INDEX = 0

# External USB camera
CAMERA_INDEX = 1

# Second external camera
CAMERA_INDEX = 2
```

---

## Override Methods

### Method 1: Direct File Modification

**Edit `config.py` directly:**

```python
# config.py
class Config:
    CONFIDENCE_THRESHOLD = 70  # Changed from 80
    DEFAULT_SAMPLES = 50       # Changed from 30
```

**Pros:** Permanent, version-controlled  
**Cons:** Requires code change

---

### Method 2: Runtime Override

**Modify after import:**

```python
from config import Config

# Override before using
Config.CONFIDENCE_THRESHOLD = 70
Config.DEFAULT_SAMPLES = 50

# Then run application
from src.controllers.face_recognition_controller import FaceRecognitionController
controller = FaceRecognitionController()
controller.run()
```

**Pros:** No file modification, flexible  
**Cons:** Not persistent, must set each run

---

### Method 3: Custom Config Script

**Create `custom_config.py`:**

```python
from config import Config

# Override parameters
Config.CONFIDENCE_THRESHOLD = 70
Config.DEFAULT_SAMPLES = 50
Config.DETECTION_SCALE_FACTOR = 1.2

# Run application
if __name__ == "__main__":
    from src.controllers.face_recognition_controller import FaceRecognitionController
    controller = FaceRecognitionController()
    controller.run()
```

**Run:** `python custom_config.py`

**Pros:** Reusable, separate from main code  
**Cons:** Extra file to maintain

---

### Method 4: Dependency Injection (Advanced)

**Pass custom config to components:**

```python
from src.models.face_detector import FaceDetector

# Override for specific component
detector = FaceDetector()
faces = detector.detect_faces(
    gray_image,
    scale_factor=1.2,  # Override default
    min_neighbors=3    # Override default
)
```

**Pros:** Fine-grained control  
**Cons:** Verbose, must pass to each call

---

## Environment Variables

**KHÔNG XÁC MINH - Current implementation does NOT use environment variables.**

**Proposed enhancement:**

```python
import os

class Config:
    # Allow env var override
    CONFIDENCE_THRESHOLD = float(os.getenv('FR_CONFIDENCE_THRESHOLD', 80))
    DEFAULT_SAMPLES = int(os.getenv('FR_DEFAULT_SAMPLES', 30))
    CAMERA_INDEX = int(os.getenv('FR_CAMERA_INDEX', 0))
```

**Usage:**
```bash
export FR_CONFIDENCE_THRESHOLD=70
export FR_DEFAULT_SAMPLES=50
python main.py
```

---

## Configuration Examples

### Example 1: High Accuracy Setup

```python
from config import Config

# Strict detection
Config.DETECTION_SCALE_FACTOR = 1.1
Config.DETECTION_MIN_NEIGHBORS = 6

# Strict recognition
Config.CONFIDENCE_THRESHOLD = 60

# More training data
Config.DEFAULT_SAMPLES = 100
```

**Use case:** Controlled environment, accuracy critical

---

### Example 2: Fast Performance Setup

```python
from config import Config

# Fast detection
Config.DETECTION_SCALE_FACTOR = 1.5
Config.DETECTION_MIN_NEIGHBORS = 3

# Lenient recognition
Config.CONFIDENCE_THRESHOLD = 100

# Quick training
Config.DEFAULT_SAMPLES = 20
```

**Use case:** Real-time demo, speed critical

---

### Example 3: Multiple Camera Setup

```python
from config import Config
from src.models.camera_service import CameraService

# Camera 1 (built-in)
cam1 = CameraService(camera_index=0)

# Camera 2 (external)
cam2 = CameraService(camera_index=1)
```

**Use case:** Multi-camera surveillance

---

### Example 4: Different Face Sizes

```python
from config import Config

# Higher resolution for better accuracy
Config.FACE_SIZE = (300, 300)

# Note: Must retrain model with new size
# Existing trainer.yml will be incompatible
```

**Warning:** Changing `FACE_SIZE` requires retraining from scratch

---

## Configuration Validation

**KHÔNG XÁC MINH - No built-in validation currently exists.**

**Proposed validation:**

```python
class Config:
    @classmethod
    def validate(cls):
        """Validate configuration parameters"""
        assert 1.01 <= cls.DETECTION_SCALE_FACTOR <= 2.0, \
            "DETECTION_SCALE_FACTOR must be in [1.01, 2.0]"
        
        assert 1 <= cls.DETECTION_MIN_NEIGHBORS <= 10, \
            "DETECTION_MIN_NEIGHBORS must be in [1, 10]"
        
        assert cls.CONFIDENCE_THRESHOLD > 0, \
            "CONFIDENCE_THRESHOLD must be positive"
        
        assert cls.DEFAULT_SAMPLES > 0, \
            "DEFAULT_SAMPLES must be positive"
        
        assert os.path.exists(cls.CASCADE_PATH), \
            f"Cascade file not found: {cls.CASCADE_PATH}"
```

---

## Configuration Best Practices

### DO:
- ✅ Use `Config` class for all constants
- ✅ Document parameter ranges and impacts
- ✅ Test configuration changes thoroughly
- ✅ Keep default values sensible for most use cases

### DON'T:
- ❌ Hardcode values in business logic
- ❌ Change `FACE_SIZE` without retraining
- ❌ Use extreme parameter values without testing
- ❌ Modify paths to non-existent directories

---

## Troubleshooting Configuration Issues

### Issue: "Cascade file not found"
**Cause:** `CASCADE_PATH` points to non-existent file  
**Solution:** Verify `haarcascades/haarcascade_frontalface_default.xml` exists

### Issue: No faces detected
**Cause:** `DETECTION_SCALE_FACTOR` too high or `DETECTION_MIN_NEIGHBORS` too high  
**Solution:** Lower both parameters

### Issue: Too many false positives
**Cause:** `DETECTION_MIN_NEIGHBORS` too low  
**Solution:** Increase to 6-7

### Issue: Always shows "Unknown"
**Cause:** `CONFIDENCE_THRESHOLD` too low  
**Solution:** Increase to 90-100

### Issue: Wrong person recognized
**Cause:** `CONFIDENCE_THRESHOLD` too high or insufficient training data  
**Solution:** Lower threshold or collect more samples

---

## Related Documentation

- [Pipeline](pipeline.md) - How config affects pipeline
- [Models](models.md) - LBPH parameters
- [Training](training.md) - Training configuration
- [Troubleshooting](troubleshooting.md) - Config-related issues

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-15
