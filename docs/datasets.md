# Datasets - Data Format and Management

## Dataset Overview

The facial recognition system uses a directory-based dataset structure where each person has a dedicated folder containing their face images. All images are grayscale, 200×200 pixels, stored as JPEG files.

**Location:** `dataset/` (auto-created at project root)  
**Format:** Directory-per-person with JPEG images  
**Label source:** Directory names

---

## Dataset Structure

### Directory Layout

```
dataset/
├── person_1/
│   ├── person_1_0.jpg
│   ├── person_1_1.jpg
│   ├── person_1_2.jpg
│   └── ...
├── person_2/
│   ├── person_2_0.jpg
│   ├── person_2_1.jpg
│   └── ...
└── person_N/
    └── ...
```

### Naming Conventions

**Directory names:**
- Format: `<person_identifier>` (no spaces, use underscores)
- Examples: `john_doe`, `jane_smith`, `nguyen_van_a`
- Case-sensitive (recommended: lowercase)
- No special characters (alphanumeric + underscore only)

**File names:**
- Format: `<person_identifier>_<index>.jpg`
- Index: Sequential integer starting from 0
- Examples: `john_doe_0.jpg`, `john_doe_1.jpg`, ..., `john_doe_29.jpg`

---

## Data Format Specifications

### Image Specifications

| Property | Value | Notes |
|----------|-------|-------|
| **Format** | JPEG | Lossy compression |
| **Color space** | Grayscale | Single channel |
| **Dimensions** | 200×200 pixels | Fixed size |
| **Data type** | uint8 | 8-bit unsigned integer |
| **Value range** | [0, 255] | 0=black, 255=white |
| **File size** | ~10-20 KB | Varies with content |

### Supported File Extensions

**Primary:** `.jpg`  
**Also supported:** `.png`, `.jpeg`

**Note:** All formats are converted to grayscale during loading, so color information is discarded.

---

## Label Schema

### Label Generation

Labels are automatically generated from directory names during training:

```python
# Example label mapping
label_map = {
    "john_doe": 0,
    "jane_smith": 1,
    "bob_jones": 2
}
```

**Rules:**
1. Each unique directory name gets a unique numeric ID
2. IDs are assigned sequentially (0, 1, 2, ...)
3. Assignment order depends on `os.walk()` traversal (typically alphabetical)
4. Mapping is saved to `trainer/labels.pickle`

### Label Consistency

**Important:** The label mapping is created during training and must remain consistent for inference.

**Implications:**
- Adding a new person requires retraining
- Removing a person requires retraining
- Renaming a directory requires retraining

**KHÔNG XÁC MINH:** Incremental training support (currently not implemented)

---

## Data Collection

### Collection Method

**Entry point:** `FaceRecognitionController.capture_faces(person_name, samples)`

**Process:**
1. User provides person name (no spaces)
2. System creates directory: `dataset/<person_name>/`
3. Camera opens and detects faces
4. For each detected face:
   - Extract ROI (face region)
   - Resize to 200×200
   - Save as `<person_name>_<count>.jpg`
5. Stop when `samples` images collected or user presses 'q'

### Collection Parameters

**From `config.py`:**
- `DEFAULT_SAMPLES = 30` - Default number of images per person
- `FACE_SIZE = (200, 200)` - Target image dimensions

**Configurable at runtime:**
```python
controller.capture_faces("john_doe", samples=50)  # Collect 50 images
```

### Collection Best Practices

**For optimal recognition accuracy:**

1. **Lighting:**
   - Consistent, diffuse lighting
   - Avoid harsh shadows
   - Similar lighting to inference environment

2. **Face angles:**
   - Mostly frontal faces
   - Include slight variations (±15° rotation)
   - Avoid extreme angles (>30°)

3. **Expressions:**
   - Mix of neutral and smiling
   - Natural expressions
   - Avoid extreme expressions

4. **Distance:**
   - Consistent camera distance
   - Face should fill ~60-80% of frame
   - Same distance as inference

5. **Background:**
   - Uncluttered background
   - Consistent background helps
   - Avoid busy patterns

6. **Quantity:**
   - Minimum: 20 images
   - Recommended: 30-50 images
   - More is better (diminishing returns after 100)

---

## Data Splits

**KHÔNG XÁC MINH - Current implementation does NOT split data.**

**Current behavior:**
- All collected images used for training
- No validation set
- No test set
- No cross-validation

**Implications:**
- Cannot measure generalization
- Risk of overfitting (minimal with LBPH)
- No objective accuracy metrics

**Proposed enhancement:**

```python
# Suggested split ratios
train_ratio = 0.7  # 70% for training
val_ratio = 0.15   # 15% for validation
test_ratio = 0.15  # 15% for testing

# Example with 30 images per person:
# - 21 images for training
# - 4-5 images for validation
# - 4-5 images for testing
```

---

## Data Transforms

### Current Transforms

**During collection:**
1. BGR to Grayscale: `cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)`
2. Resize to 200×200: `cv2.resize(roi, (200, 200))`

**During training:**
1. Load as grayscale: `cv2.imread(path, cv2.IMREAD_GRAYSCALE)`
2. Resize to 200×200: `cv2.resize(img, (200, 200))` (redundant safety)

**No normalization:**
- Images kept in [0, 255] range
- No mean subtraction
- No standard deviation scaling

### Data Augmentation

**KHÔNG XÁC MINH - No augmentation currently implemented.**

**Proposed augmentations:**

```python
# Horizontal flip
flipped = cv2.flip(image, 1)

# Rotation (±5 degrees)
rows, cols = image.shape
M = cv2.getRotationMatrix2D((cols/2, rows/2), angle=5, scale=1)
rotated = cv2.warpAffine(image, M, (cols, rows))

# Brightness adjustment
brighter = cv2.convertScaleAbs(image, alpha=1.2, beta=10)
darker = cv2.convertScaleAbs(image, alpha=0.8, beta=-10)

# Gaussian noise
noise = np.random.normal(0, 10, image.shape).astype(np.uint8)
noisy = cv2.add(image, noise)

# Gaussian blur
blurred = cv2.GaussianBlur(image, (5, 5), 0)
```

**Benefits:**
- Increases effective dataset size
- Improves robustness to variations
- Reduces overfitting

---

## Data Versioning

**KHÔNG XÁC MINH - No versioning system currently implemented.**

**Current state:**
- Dataset is mutable (can add/remove images anytime)
- No tracking of dataset changes
- No dataset snapshots
- No metadata (collection date, camera settings, etc.)

**Proposed versioning strategy:**

```
dataset/
├── v1/
│   ├── john_doe/
│   └── jane_smith/
├── v2/
│   ├── john_doe/
│   ├── jane_smith/
│   └── bob_jones/
└── metadata.json
```

**Metadata example:**
```json
{
  "version": "v2",
  "created": "2026-01-15T23:00:00Z",
  "num_people": 3,
  "total_images": 90,
  "camera_index": 0,
  "face_size": [200, 200]
}
```

---

## Data Quality

### Quality Checks

**KHÔNG XÁC MINH - No automated quality checks.**

**Manual quality checks recommended:**

1. **Face detection success:**
   - All images should contain faces
   - Face should be centered
   - Face should be clearly visible

2. **Image quality:**
   - Not blurry
   - Not overexposed/underexposed
   - Sufficient contrast

3. **Consistency:**
   - Similar lighting across images
   - Similar face size
   - Similar background

### Quality Issues

**Common problems:**

| Issue | Cause | Solution |
|-------|-------|----------|
| Blurry images | Camera motion, low light | Ensure stable camera, better lighting |
| Partial faces | Face too close to camera | Adjust distance |
| No face detected | Poor lighting, angle | Improve conditions, face camera |
| Inconsistent lighting | Moving between locations | Collect in same location |

### Data Cleaning

**Manual cleaning process:**

1. Review images in `dataset/<person>/`
2. Delete poor quality images
3. Retrain model with cleaned dataset

```bash
# Example: Remove blurry images
cd dataset/john_doe/
# Manually inspect and delete bad images
rm john_doe_5.jpg john_doe_12.jpg john_doe_23.jpg
```

**Note:** File indices don't need to be continuous.

---

## Dataset Statistics

**KHÔNG XÁC MINH - No built-in statistics tools.**

**Proposed statistics script:**

```python
import os
from config import Config

def dataset_stats():
    stats = {
        'num_people': 0,
        'total_images': 0,
        'images_per_person': {}
    }
    
    for person_dir in os.listdir(Config.DATASET_DIR):
        person_path = os.path.join(Config.DATASET_DIR, person_dir)
        if os.path.isdir(person_path):
            images = [f for f in os.listdir(person_path) 
                     if f.endswith(('.jpg', '.png', '.jpeg'))]
            stats['num_people'] += 1
            stats['total_images'] += len(images)
            stats['images_per_person'][person_dir] = len(images)
    
    return stats

# Usage
stats = dataset_stats()
print(f"People: {stats['num_people']}")
print(f"Total images: {stats['total_images']}")
print(f"Average images/person: {stats['total_images']/stats['num_people']:.1f}")
```

---

## Dataset Management

### Adding New Person

```bash
# Method 1: Via application
python main.py
> Choose: 1
> Enter name: new_person

# Method 2: Manual (not recommended)
mkdir dataset/new_person
# Copy images to dataset/new_person/
# Rename to new_person_0.jpg, new_person_1.jpg, ...
```

**After adding:** Retrain model (option 2 in menu)

### Removing Person

```bash
# Delete person directory
rm -rf dataset/person_to_remove/

# Retrain model
python main.py
> Choose: 2
```

### Updating Person Data

```bash
# Add more images for existing person
python main.py
> Choose: 1
> Enter name: existing_person
# New images will be appended (e.g., existing_person_30.jpg, ...)

# Retrain model
python main.py
> Choose: 2
```

### Backup Dataset

```bash
# Create backup
tar -czf dataset_backup_$(date +%Y%m%d).tar.gz dataset/

# Restore backup
tar -xzf dataset_backup_20260115.tar.gz
```

---

## Dataset Sources

**KHÔNG XÁC MINH - Current implementation only supports webcam collection.**

**Supported source:**
- Live webcam capture via OpenCV

**Not supported:**
- Importing existing image datasets
- Video file processing
- Batch import from directory
- Web scraping
- Public datasets (LFW, CelebA, etc.)

**Proposed enhancement:**

```python
def import_from_directory(source_dir, person_name):
    """Import existing images into dataset"""
    person_dir = os.path.join(Config.DATASET_DIR, person_name)
    os.makedirs(person_dir, exist_ok=True)
    
    count = 0
    for file in os.listdir(source_dir):
        if file.endswith(('.jpg', '.png', '.jpeg')):
            img = cv2.imread(os.path.join(source_dir, file), cv2.IMREAD_GRAYSCALE)
            img_resized = cv2.resize(img, Config.FACE_SIZE)
            
            output_path = os.path.join(person_dir, f"{person_name}_{count}.jpg")
            cv2.imwrite(output_path, img_resized)
            count += 1
```

---

## Data Privacy

**Considerations:**

1. **Local storage:** All data stored locally, not uploaded to cloud
2. **No encryption:** Images stored as plain JPEG files
3. **Access control:** Standard filesystem permissions
4. **Retention:** No automatic deletion policy

**KHÔNG XÁC MINH:** Privacy policy, GDPR compliance, consent management

**Recommendations:**
- Obtain consent before collecting face images
- Inform subjects about data usage
- Provide mechanism to delete personal data
- Secure storage location with appropriate permissions

---

## Related Documentation

- [Pipeline](pipeline.md) - How dataset flows through pipeline
- [Training](training.md) - How dataset is used for training
- [Configs](configs.md) - Dataset-related configuration
- [Troubleshooting](troubleshooting.md) - Dataset issues

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-15
