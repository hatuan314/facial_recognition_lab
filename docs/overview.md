# Overview - Facial Recognition Lab

## Project Goals

**Primary Goal:** Educational facial recognition system using classical computer vision techniques (LBPH + Haar Cascade) for real-time face recognition via webcam.

**Key Objectives:**
- Demonstrate MVC architecture and SOLID principles in CV applications
- Provide hands-on experience with OpenCV face detection and recognition
- Enable quick prototyping of face recognition workflows
- Serve as reference implementation for computer vision coursework

## Non-Goals

**What this project is NOT:**
- ❌ Production-ready system with authentication/authorization
- ❌ Deep learning-based face recognition (no FaceNet/ArcFace)
- ❌ Distributed/scalable system with database backend
- ❌ Web service with REST API (CLI tool only)
- ❌ Multi-camera or video file processing system

**KHÔNG XÁC MINH:** Deployment targets, performance SLAs, accuracy requirements

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Language | Python 3.7+ | Core implementation |
| CV Library | OpenCV (opencv-contrib-python) | Face detection & recognition |
| Numerics | NumPy | Array operations |
| Serialization | Pickle | Label mapping storage |
| Architecture | MVC + SOLID | Code organization |

## Quick Start

### Installation

```bash
# Clone repository
cd facial_recognition_lab

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Run application
python main.py

# Interactive menu will appear:
# 1. Thu ảnh training    - Collect training data
# 2. Train model         - Train LBPH model
# 3. Nhận diện realtime  - Real-time recognition
# 4. Đánh giá accuracy   - Evaluate model performance
# 0. Thoát              - Exit
```

### Typical Workflow

```bash
# Step 1: Collect training data for a person
python main.py
> Choose: 1
> Enter name: john_doe
# Camera opens, collect 30 face images

# Step 2: Train model
python main.py
> Choose: 2
# Model trains and saves to trainer/

# Step 3: Evaluate model (optional)
python main.py
> Choose: 4
# Runs evaluation with train/test split and metrics

# Step 4: Run recognition
python main.py
> Choose: 3
# Camera opens with real-time face recognition
```

## Repository Structure

```
facial_recognition_lab/
├── main.py                    # Entry point
├── config.py                  # Configuration constants
├── requirements.txt           # Python dependencies
│
├── src/                       # Source code (MVC)
│   ├── controllers/           # Application logic
│   │   └── face_recognition_controller.py
│   ├── models/                # Business logic
│   │   ├── camera_service.py
│   │   ├── face_detector.py
│   │   ├── face_recognizer.py
│   │   ├── data_manager.py
│   │   └── model_evaluator.py
│   └── views/                 # Presentation
│       └── console_view.py
│
├── dataset/                   # Training images (auto-created)
├── trainer/                   # Trained models (auto-created)
├── haarcascades/              # Pre-trained cascades
└── docs/                      # Documentation
```

**Key Directories:**
- `src/controllers/` - Orchestrates workflows between models and views
- `src/models/` - Core CV logic (detection, recognition, data I/O)
- `src/views/` - UI layer (console menu, video display)
- `dataset/` - Training data organized by person
- `trainer/` - Serialized LBPH model and label mappings

## Where to Start

### For Users
1. Read this overview
2. Follow [Quick Start](#quick-start)
3. Check [docs/troubleshooting.md](troubleshooting.md) if issues arise

### For Developers
1. **Understand architecture:** Read [ARCHITECTURE.md](../ARCHITECTURE.md)
2. **Understand pipeline:** Read [docs/pipeline.md](pipeline.md)
3. **Understand contracts:** Read [docs/models.md](models.md) and [docs/datasets.md](datasets.md)
4. **Before coding:** Read [AGENTS.md](../AGENTS.md)

### For AI Agents
**MANDATORY READING ORDER:**
1. [AGENTS.md](../AGENTS.md) - Development rules and contracts
2. [docs/pipeline.md](pipeline.md) - Data flow understanding
3. [docs/models.md](models.md) - Model contracts
4. [docs/configs.md](configs.md) - Configuration system

## Key Concepts

### MVC Architecture
- **Model:** Business logic (camera, detection, recognition, data)
- **View:** UI layer (console, video display)
- **Controller:** Orchestration (workflow coordination)

### LBPH Algorithm
- Local Binary Patterns Histograms
- Classical texture-based face recognition
- Fast, lightweight, CPU-friendly
- See [docs/models.md](models.md) for details

### Haar Cascade
- Pre-trained face detector from OpenCV
- Fast but less accurate than modern detectors
- Good for real-time applications on CPU

## System Requirements

**Hardware:**
- Webcam (built-in or external)
- CPU: Any modern processor (Intel/AMD)
- RAM: 4GB minimum
- GPU: Not required

**Software:**
- Python 3.7+
- Operating System: Windows, macOS, or Linux
- Camera permissions enabled

**KHÔNG XÁC MINH:** Specific performance requirements (FPS, latency)

## Related Documentation

- [Pipeline](pipeline.md) - End-to-end CV pipeline
- [Configuration](configs.md) - Config system
- [Datasets](datasets.md) - Data format and management
- [Models](models.md) - LBPH architecture
- [Training](training.md) - Training workflow
- [Inference](inference.md) - Recognition API
- [Troubleshooting](troubleshooting.md) - Common issues

## License & Attribution

**KHÔNG XÁC MINH:** License type, attribution requirements

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-15  
**Maintainer:** KHÔNG XÁC MINH
