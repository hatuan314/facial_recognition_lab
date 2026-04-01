# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the application
python main.py

# Install dependencies
pip install -r requirements.txt

# Verify imports work
python -c "from src.models.face_recognizer import FaceRecognizer"

# Check all module imports
python -c "from src.controllers.face_recognition_controller import FaceRecognitionController"
```

The app presents an interactive menu:
- `1` — Collect training images (30 per person via webcam)
- `2` — Train LBPH model
- `3` — Real-time face recognition via webcam
- `4` — Evaluate model accuracy (sklearn metrics, 80/20 split)
- `0` — Exit

No automated test suite exists. Testing is manual via the menu options above.

## Architecture

MVC pattern with strict separation:

```
main.py
└── FaceRecognitionController (src/controllers/)
    ├── CameraService     — OpenCV VideoCapture wrapper (context manager)
    ├── FaceDetector      — Haar Cascade detection, returns (x,y,w,h) rects
    ├── FaceRecognizer    — LBPH train/predict/save/load
    ├── DataManager       — Dataset I/O + model serialization
    ├── ModelEvaluator    — Metrics with sklearn (fallback: manual impl)
    ├── ConsoleView       — Menu, prompts, status messages
    └── VideoView         — OpenCV window, bounding boxes, text overlay
```

**Data flow:**
1. `DataManager.load_training_data()` reads `dataset/<person>/<person>_<i>.jpg` → returns `(faces, labels, label_map)`
2. `FaceRecognizer.train(faces, labels)` fits the LBPH model
3. `DataManager.save_model()` persists to `trainer/trainer.yml` + `trainer/labels.pickle`
4. During inference: `FaceRecognizer.predict(face)` returns `(predicted_id: int, confidence: float)` — lower confidence = more certain

## Key Contracts

Never break these without updating the corresponding `docs/` file:

| Contract | Value |
|---|---|
| Dataset path | `dataset/<person_name>/<person_name>_<index>.jpg` |
| Face image format | Grayscale JPEG, 200×200 pixels |
| Model input | `np.ndarray` shape `(200, 200)`, dtype `uint8` |
| Model output | `(predicted_id: int, confidence: float)` tuple |
| Config access | Always use `Config` class from `config.py`, never hardcode |
| Confidence | Lower = more confident; threshold at `Config.CONFIDENCE_THRESHOLD` (default: 80) |

## Configuration

All tunable parameters live in `config.py` `Config` class:
- `CONFIDENCE_THRESHOLD = 80` — predictions above this are "Unknown"
- `FACE_SIZE = (200, 200)` — normalized face dimensions
- `DEFAULT_SAMPLES = 30` — images collected per person
- `DETECTION_SCALE_FACTOR`, `DETECTION_MIN_NEIGHBORS` — Haar Cascade tuning
- `Config.ensure_directories()` — auto-creates `dataset/` and `trainer/`

## Documentation

Detailed specs live in `docs/`:
- `docs/pipeline.md` — end-to-end CV pipeline
- `docs/models.md` — LBPH algorithm and model contracts
- `docs/datasets.md` — dataset format specification
- `docs/training.md` / `docs/inference.md` / `docs/evaluation.md` — workflow docs
- `docs/troubleshooting.md` — common issues (camera access, missing cascade, poor accuracy)

Before modifying any model I/O contracts, training/inference behavior, or dataset format, read and update the relevant doc in `docs/`.
