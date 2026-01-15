# Troubleshooting - Common Issues and Solutions

## Overview

This document provides solutions to common issues encountered when using the facial recognition system. Issues are organized by phase: setup, data collection, training, and inference.

---

## Setup Issues

### Issue: "No module named 'cv2'"

**Symptom:**
```
ImportError: No module named 'cv2'
```

**Cause:** OpenCV not installed

**Solution:**
```bash
pip install opencv-contrib-python
```

**Verification:**
```python
import cv2
print(cv2.__version__)  # Should print version number
```

---

### Issue: "No module named 'cv2.face'"

**Symptom:**
```
AttributeError: module 'cv2' has no attribute 'face'
```

**Cause:** Installed `opencv-python` instead of `opencv-contrib-python`

**Solution:**
```bash
# Uninstall opencv-python
pip uninstall opencv-python

# Install opencv-contrib-python
pip install opencv-contrib-python
```

**Note:** `opencv-contrib-python` includes extra modules like `face`

---

### Issue: Permission denied when creating directories

**Symptom:**
```
PermissionError: [Errno 13] Permission denied: 'dataset'
```

**Cause:** Insufficient file system permissions

**Solution:**
```bash
# Check current directory permissions
ls -la

# Run with appropriate permissions
# Option 1: Change directory permissions
chmod 755 .

# Option 2: Run from user directory
cd ~/facial_recognition_lab
python main.py
```

---

## Camera Issues

### Issue: "Không mở được camera"

**Symptom:**
```
Exception: Không mở được camera.
```

**Causes and Solutions:**

#### Cause 1: Camera in use by another application
**Solution:**
- Close applications using camera (Zoom, Skype, FaceTime, etc.)
- Check Activity Monitor (macOS) or Task Manager (Windows)

#### Cause 2: Camera permissions not granted
**Solution (macOS):**
1. System Preferences → Security & Privacy → Camera
2. Enable camera access for Terminal or Python

**Solution (Windows):**
1. Settings → Privacy → Camera
2. Enable camera access for apps

#### Cause 3: Wrong camera index
**Solution:**
```python
# Try different camera indices
Config.CAMERA_INDEX = 1  # Try 1, 2, 3...
```

#### Cause 4: No camera available
**Solution:**
- Connect external webcam
- Check camera is recognized by system
- macOS: Photo Booth app should work
- Windows: Camera app should work

---

### Issue: Camera opens but shows black screen

**Symptom:** Camera window opens but displays black/blank screen

**Causes and Solutions:**

#### Cause 1: Camera initializing
**Solution:** Wait 2-3 seconds for camera to initialize

#### Cause 2: Camera covered or faulty
**Solution:**
- Check camera lens is not covered
- Test camera with other applications
- Try external camera

#### Cause 3: Driver issues
**Solution:**
- Update camera drivers (Windows)
- Restart computer
- Check system camera settings

---

## Data Collection Issues

### Issue: No faces detected during collection

**Symptom:** Camera shows video but no green rectangle appears

**Causes and Solutions:**

#### Cause 1: Poor lighting
**Solution:**
- Ensure adequate lighting
- Face camera toward light source
- Avoid backlighting

#### Cause 2: Face too far or too close
**Solution:**
- Position face 50-100cm from camera
- Face should fill ~60-80% of frame

#### Cause 3: Face angle too extreme
**Solution:**
- Face camera directly (frontal view)
- Keep head rotation within ±15°

#### Cause 4: Detection parameters too strict
**Solution:**
```python
# In config.py, adjust parameters
Config.DETECTION_SCALE_FACTOR = 1.2  # Lower from 1.3
Config.DETECTION_MIN_NEIGHBORS = 3   # Lower from 5
```

---

### Issue: Cascade file not found

**Symptom:**
```
FileNotFoundError: Không tìm thấy file cascade: haarcascades/haarcascade_frontalface_default.xml
```

**Cause:** Missing Haar Cascade XML file

**Solution:**
```bash
# Download cascade file
mkdir -p haarcascades
cd haarcascades
curl -O https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml
cd ..
```

**Verification:**
```bash
ls haarcascades/haarcascade_frontalface_default.xml
```

---

### Issue: Images not saving

**Symptom:** Collection completes but no images in dataset folder

**Causes and Solutions:**

#### Cause 1: Directory not created
**Solution:**
```python
# Ensure directories exist
Config.ensure_directories()
```

#### Cause 2: Permission issues
**Solution:**
```bash
# Check permissions
ls -la dataset/

# Fix permissions
chmod -R 755 dataset/
```

#### Cause 3: Disk full
**Solution:**
- Check available disk space
- Free up space if needed

---

## Training Issues

### Issue: "Không có dữ liệu trong dataset"

**Symptom:**
```
ValueError: Không có dữ liệu trong dataset. Vui lòng thu ảnh trước.
```

**Cause:** Dataset directory empty or no valid images

**Solution:**
1. Collect training data first (option 1 in menu)
2. Verify images exist:
   ```bash
   ls -R dataset/
   ```
3. Check image file extensions (.jpg, .png, .jpeg)

---

### Issue: "need at least one array to concatenate"

**Symptom:**
```
ValueError: need at least one array to concatenate
```

**Cause:** No valid images found during training

**Solutions:**

#### Check 1: Dataset structure
```bash
# Correct structure:
dataset/
├── person_1/
│   ├── person_1_0.jpg
│   └── ...
└── person_2/
    └── ...

# Incorrect (files in root):
dataset/
├── image1.jpg  # Wrong!
└── image2.jpg  # Wrong!
```

#### Check 2: File extensions
```bash
# Find all images
find dataset/ -type f -name "*.jpg" -o -name "*.png" -o -name "*.jpeg"
```

#### Check 3: File corruption
```python
# Test loading images
import cv2
img = cv2.imread("dataset/person/image.jpg")
if img is None:
    print("Corrupted image!")
```

---

### Issue: Training very slow

**Symptom:** Training takes >1 minute for small dataset

**Causes and Solutions:**

#### Cause 1: Too many images
**Solution:** LBPH should be fast (<10s for 100 images). If slow, check:
- CPU usage (other processes?)
- Disk I/O (slow drive?)

#### Cause 2: Large image files
**Solution:**
```python
# Images should be 200×200, ~10-20KB each
# Check file sizes
import os
for root, dirs, files in os.walk("dataset"):
    for file in files:
        path = os.path.join(root, file)
        size = os.path.getsize(path) / 1024  # KB
        if size > 100:
            print(f"Large file: {path} ({size:.1f} KB)")
```

---

### Issue: Model file not created

**Symptom:** Training completes but no trainer.yml file

**Causes and Solutions:**

#### Cause 1: Permission issues
**Solution:**
```bash
# Check trainer directory
ls -la trainer/

# Fix permissions
chmod 755 trainer/
```

#### Cause 2: Disk full
**Solution:** Check available disk space

#### Cause 3: Path issues
**Solution:**
```python
# Verify paths
from config import Config
print(f"Trainer dir: {Config.TRAINER_DIR}")
print(f"Exists: {os.path.exists(Config.TRAINER_DIR)}")
```

---

## Inference Issues

### Issue: "Model hoặc labels chưa được train"

**Symptom:**
```
FileNotFoundError: Model hoặc labels chưa được train.
```

**Cause:** Attempting inference before training

**Solution:**
1. Train model first (option 2 in menu)
2. Verify model files exist:
   ```bash
   ls trainer/trainer.yml
   ls trainer/labels.pickle
   ```

---

### Issue: Always shows "Unknown"

**Symptom:** All faces recognized as "Unknown" (red box)

**Causes and Solutions:**

#### Cause 1: Confidence threshold too low
**Solution:**
```python
# Increase threshold in config.py
Config.CONFIDENCE_THRESHOLD = 100  # Increase from 80
```

#### Cause 2: Different conditions from training
**Solution:**
- Ensure similar lighting
- Maintain similar distance from camera
- Use frontal face angle

#### Cause 3: Insufficient training data
**Solution:**
- Collect more images (50-100 per person)
- Retrain model

#### Cause 4: Model not loaded correctly
**Solution:**
```python
# Verify model loaded
recognizer = FaceRecognizer()
recognizer.load_model("trainer/trainer.yml")
print(f"Model trained: {recognizer._is_trained}")  # Should be True
```

---

### Issue: Wrong person recognized

**Symptom:** System recognizes person A as person B

**Causes and Solutions:**

#### Cause 1: Confidence threshold too high
**Solution:**
```python
# Lower threshold
Config.CONFIDENCE_THRESHOLD = 60  # Decrease from 80
```

#### Cause 2: Similar appearances
**Solution:**
- Collect more diverse training data
- Increase training samples per person
- Consider if people look genuinely similar

#### Cause 3: Poor training data quality
**Solution:**
- Review training images for quality
- Remove blurry or poor-quality images
- Retrain with clean dataset

---

### Issue: Recognition flickering

**Symptom:** Name rapidly changes between correct and "Unknown"

**Cause:** Confidence score near threshold

**Solutions:**

#### Solution 1: Adjust threshold
```python
# Fine-tune threshold
Config.CONFIDENCE_THRESHOLD = 75  # Adjust as needed
```

#### Solution 2: Implement temporal smoothing
```python
# Proposed enhancement (not currently implemented)
from collections import deque

class Smoother:
    def __init__(self, window=5):
        self.history = deque(maxlen=window)
    
    def smooth(self, pred_id):
        self.history.append(pred_id)
        # Return most common prediction
        from collections import Counter
        return Counter(self.history).most_common(1)[0][0]
```

---

### Issue: Low FPS / Laggy video

**Symptom:** Video stutters, low frame rate

**Causes and Solutions:**

#### Cause 1: High resolution
**Solution:**
```python
# Reduce frame resolution
ret, frame = cam.read()
frame = cv2.resize(frame, (640, 480))  # Downscale
```

#### Cause 2: Slow detection
**Solution:**
```python
# Faster detection parameters
Config.DETECTION_SCALE_FACTOR = 1.5  # Increase from 1.3
Config.DETECTION_MIN_NEIGHBORS = 3   # Decrease from 5
```

#### Cause 3: Process every frame
**Solution:**
```python
# Skip frames
frame_count = 0
while True:
    ret, frame = cam.read()
    frame_count += 1
    
    if frame_count % 2 == 0:  # Process every 2nd frame
        continue
    
    # Process frame
```

#### Cause 4: CPU overload
**Solution:**
- Close other applications
- Check CPU usage in Activity Monitor/Task Manager

---

## Configuration Issues

### Issue: Changes to config.py not taking effect

**Symptom:** Modified configuration values not reflected in application

**Causes and Solutions:**

#### Cause 1: Python caching
**Solution:**
```bash
# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Restart application
python main.py
```

#### Cause 2: Hardcoded values
**Solution:** Verify code uses `Config.PARAMETER` not hardcoded values

#### Cause 3: Need to retrain
**Solution:** Some config changes (e.g., FACE_SIZE) require retraining

---

## Platform-Specific Issues

### macOS Issues

#### Issue: "Operation not permitted" camera access
**Solution:**
1. System Preferences → Security & Privacy → Camera
2. Add Terminal or Python to allowed apps
3. Restart Terminal

#### Issue: M1/M2 compatibility
**Solution:**
```bash
# Use native ARM64 Python
arch -arm64 python3 main.py

# Or install Rosetta 2
softwareupdate --install-rosetta
```

---

### Windows Issues

#### Issue: Camera index different
**Solution:**
```python
# Windows often uses different indices
Config.CAMERA_INDEX = 1  # Try 0, 1, 2
```

#### Issue: Path separators
**Solution:** Code uses `os.path.join()` which handles this automatically

---

### Linux Issues

#### Issue: Camera permissions
**Solution:**
```bash
# Add user to video group
sudo usermod -a -G video $USER

# Logout and login again
```

#### Issue: Missing system libraries
**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install libgl1-mesa-glx libglib2.0-0

# Fedora
sudo dnf install mesa-libGL glib2
```

---

## Debugging Techniques

### Enable Verbose Logging

**Proposed enhancement:**
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.debug("Debug information here")
```

---

### Check OpenCV Installation

```python
import cv2
print(f"OpenCV version: {cv2.__version__}")
print(f"Has face module: {hasattr(cv2, 'face')}")

# List available modules
print(cv2.getBuildInformation())
```

---

### Verify Dataset

```python
import os
from config import Config

def verify_dataset():
    """Verify dataset structure and contents"""
    if not os.path.exists(Config.DATASET_DIR):
        print("❌ Dataset directory does not exist")
        return
    
    people = os.listdir(Config.DATASET_DIR)
    people = [p for p in people if os.path.isdir(os.path.join(Config.DATASET_DIR, p))]
    
    if not people:
        print("❌ No people in dataset")
        return
    
    print(f"✓ Found {len(people)} people:")
    
    for person in people:
        person_dir = os.path.join(Config.DATASET_DIR, person)
        images = [f for f in os.listdir(person_dir) 
                 if f.endswith(('.jpg', '.png', '.jpeg'))]
        print(f"  - {person}: {len(images)} images")
        
        if len(images) < 20:
            print(f"    ⚠️  Warning: Less than 20 images")

verify_dataset()
```

---

### Test Model Loading

```python
from src.models.face_recognizer import FaceRecognizer
from src.models.data_manager import DataManager

try:
    data_manager = DataManager()
    model_path, label_map = data_manager.load_model_and_labels()
    print(f"✓ Model path: {model_path}")
    print(f"✓ Label map: {label_map}")
    
    recognizer = FaceRecognizer()
    recognizer.load_model(model_path)
    print(f"✓ Model loaded successfully")
    print(f"✓ Is trained: {recognizer._is_trained}")
    
except Exception as e:
    print(f"❌ Error: {e}")
```

---

## Getting Help

### Information to Provide

When seeking help, provide:

1. **Error message:** Full error traceback
2. **Python version:** `python --version`
3. **OpenCV version:** `python -c "import cv2; print(cv2.__version__)"`
4. **Operating system:** macOS/Windows/Linux version
5. **Steps to reproduce:** What you did before error
6. **Dataset info:** Number of people, images per person
7. **Configuration:** Relevant Config values

### Example Bug Report

```
**Issue:** Cannot train model

**Error:**
ValueError: need at least one array to concatenate

**Environment:**
- Python: 3.9.7
- OpenCV: 4.5.3.56
- OS: macOS 12.0 (M1)

**Steps:**
1. Collected 30 images for john_doe
2. Selected option 2 (Train model)
3. Error occurred

**Dataset:**
- 1 person (john_doe)
- 30 images in dataset/john_doe/
- All files are .jpg format

**Config:**
- FACE_SIZE: (200, 200)
- DEFAULT_SAMPLES: 30
```

---

## Related Documentation

- [Overview](overview.md) - System overview
- [Pipeline](pipeline.md) - Understanding the pipeline
- [Configs](configs.md) - Configuration options
- [Training](training.md) - Training workflow
- [Inference](inference.md) - Inference workflow

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-15
