# AGENTS.md - AI Agent Development Guide

## Purpose

This document provides **mandatory guidelines** for AI agents working on this codebase. Following these rules ensures code quality, maintains system contracts, and prevents breaking changes.

**Target audience:** AI coding assistants, automated tools, and human developers using AI assistance.

---

## Mandatory Reading Order

**BEFORE making ANY code changes, read documentation in this order:**

1. **AGENTS.md** (this file) - Development rules and contracts
2. **docs/overview.md** - Project goals, structure, quickstart
3. **docs/pipeline.md** - End-to-end CV pipeline and data flow
4. **docs/models.md** - LBPH model contracts (input/output)
5. **docs/configs.md** - Configuration system
6. **docs/datasets.md** - Dataset format and contracts

**For specific tasks, also read:**
- Training changes → **docs/training.md**
- Inference changes → **docs/inference.md**
- Adding evaluation → **docs/evaluation.md**
- Experiment tracking → **docs/experiments.md**
- Debugging → **docs/troubleshooting.md**

---

## Core Rules

### Rule 1: NO FABRICATION

**❌ NEVER:**
- Invent functions, classes, or APIs that don't exist
- Assume behavior not verified in code
- Create contracts without documentation
- Guess implementation details

**✅ ALWAYS:**
- Verify existence before referencing
- Check actual implementation
- Mark unverified items as "KHÔNG XÁC MINH"
- Ask for clarification when uncertain

**Example - WRONG:**
```python
# Assuming a function exists without checking
result = model.predict_batch(faces)  # Does NOT exist!
```

**Example - CORRECT:**
```python
# Verify function exists first
# Check: src/models/face_recognizer.py has predict() but NOT predict_batch()
# Therefore, implement batch manually:
results = [model.predict(face) for face in faces]
```

---

### Rule 2: RESPECT CONTRACTS

**System contracts MUST NOT be changed without updating documentation.**

#### Critical Contracts

**Dataset Contract:**
- Location: `dataset/<person_name>/<person_name>_<index>.jpg`
- Format: Grayscale JPEG, 200×200 pixels
- Labels: Directory name = person identifier
- **DO NOT change without updating docs/datasets.md**

**Model Input Contract:**
```python
# Input to FaceRecognizer.predict()
face_image: np.ndarray
    - Shape: (200, 200)
    - Dtype: uint8
    - Range: [0, 255]
    - Color: Grayscale
```
**DO NOT change without updating docs/models.md**

**Model Output Contract:**
```python
# Output from FaceRecognizer.predict()
(predicted_id: int, confidence: float)
    - predicted_id: [0, num_people)
    - confidence: [0, ∞), lower = more confident
```
**DO NOT change without updating docs/models.md**

**Config Contract:**
```python
# All configuration via Config class
from config import Config
Config.CONFIDENCE_THRESHOLD  # Access like this
```
**DO NOT hardcode values. Use Config class.**

---

### Rule 3: DOCUMENTATION FIRST

**Before implementing features:**

1. **Check if documented:** Search docs/ for existing specification
2. **If not documented:** Create/update relevant doc first
3. **Then implement:** Code must match documentation
4. **Update docs:** If implementation differs, update docs immediately

**Workflow:**
```
1. Read relevant docs
2. Propose changes to docs (if needed)
3. Get approval
4. Implement code matching docs
5. Update docs if implementation differs
6. Mark completion
```

---

### Rule 4: TEST BEFORE COMMIT

**Definition of Done (DoD):**

Every code change MUST satisfy:

- [ ] **Functionality:** Code works as intended
- [ ] **Contracts:** Input/output contracts unchanged (or documented)
- [ ] **No breaking changes:** Existing functionality still works
- [ ] **Documentation:** Relevant docs updated
- [ ] **Code style:** Follows existing patterns
- [ ] **No hardcoded values:** Uses Config class
- [ ] **Error handling:** Appropriate try-catch blocks
- [ ] **Tested manually:** Ran and verified behavior

**Testing checklist:**
```bash
# 1. Verify imports work
python -c "from src.models.face_recognizer import FaceRecognizer"

# 2. Run main application
python main.py

# 3. Test each workflow
# - Data collection (option 1)
# - Training (option 2)
# - Inference (option 3)

# 4. Check for errors in output
```

---

### Rule 5: NO ASSUMPTIONS

**When uncertain, ASK. Do NOT:**
- Assume user requirements
- Guess implementation approach
- Infer missing specifications
- Make architectural decisions alone

**Instead:**
- State what you know from code
- List what is unclear
- Propose 2-3 options
- Ask for user decision

**Example:**
```
I found that evaluation metrics are not implemented (KHÔNG XÁC MINH).

Options:
A) Implement basic accuracy only
B) Implement full metrics (accuracy, precision, recall, F1)
C) Skip evaluation for now

Which approach do you prefer?
```

---

## Code Modification Guidelines

### Adding New Features

**Process:**

1. **Verify necessity:** Is feature truly needed?
2. **Check existing code:** Does similar functionality exist?
3. **Design contract:** Define inputs, outputs, behavior
4. **Document first:** Update relevant docs
5. **Implement:** Follow existing patterns
6. **Test:** Verify functionality
7. **Update docs:** Reflect actual implementation

**Example - Adding batch inference:**

```markdown
# 1. Document in docs/inference.md
## Batch Inference API

Function: `FaceRecognizer.predict_batch(face_images)`

Input:
- face_images: List[np.ndarray], each (200, 200) uint8

Output:
- List[(predicted_id: int, confidence: float)]
```

```python
# 2. Implement in src/models/face_recognizer.py
def predict_batch(self, face_images):
    """Predict multiple faces at once
    
    Args:
        face_images: List of face images (200×200 grayscale)
    
    Returns:
        List of (predicted_id, confidence) tuples
    """
    if not self._is_trained:
        raise Exception("Model chưa được train hoặc load.")
    
    results = []
    for face in face_images:
        pred_id, conf = self.predict(face)
        results.append((pred_id, conf))
    
    return results
```

```python
# 3. Test
faces = [face1, face2, face3]
results = recognizer.predict_batch(faces)
assert len(results) == len(faces)
```

---

### Modifying Existing Code

**BEFORE modifying:**

1. **Understand current behavior:** Read code thoroughly
2. **Check dependencies:** What calls this code?
3. **Verify contracts:** Will change break contracts?
4. **Plan migration:** How to update callers?

**Safe modifications:**
- ✅ Add optional parameters (with defaults)
- ✅ Add new methods (don't change existing)
- ✅ Improve error messages
- ✅ Add logging
- ✅ Optimize without changing behavior

**Dangerous modifications:**
- ⚠️ Change function signatures
- ⚠️ Change return types
- ⚠️ Change data formats
- ⚠️ Remove functionality

**For dangerous modifications:**
1. Document breaking change
2. Update all callers
3. Update documentation
4. Test thoroughly

---

### Refactoring Guidelines

**When refactoring:**

1. **Preserve behavior:** External behavior unchanged
2. **Maintain contracts:** Input/output unchanged
3. **Test equivalence:** Old and new produce same results
4. **Update docs:** If internal structure changes significantly

**Example - Refactoring data loading:**

```python
# OLD (works, but messy)
def load_training_data(self):
    faces = []
    labels = []
    # ... 20 lines of code ...
    return faces, labels, label_map

# NEW (cleaner, same behavior)
def load_training_data(self):
    """Load training data from dataset directory"""
    faces, labels = [], []
    label_map = self._build_label_map()
    
    for person, person_id in label_map.items():
        person_faces = self._load_person_faces(person)
        faces.extend(person_faces)
        labels.extend([person_id] * len(person_faces))
    
    return faces, labels, label_map

def _build_label_map(self):
    """Build mapping from person names to IDs"""
    # ...

def _load_person_faces(self, person):
    """Load all face images for a person"""
    # ...
```

**Verify:** Same output for same input ✓

---

## Architecture Principles

### MVC Pattern

**Maintain separation:**

- **Models** (`src/models/`): Business logic, data operations
- **Views** (`src/views/`): UI, display, user interaction
- **Controllers** (`src/controllers/`): Workflow orchestration

**DO NOT:**
- Put business logic in views
- Put UI code in models
- Put data operations in controllers (delegate to models)

**Example - WRONG:**
```python
# In controller - DON'T do data operations directly
def train_model(self):
    faces = []
    for root, dirs, files in os.walk(dataset_dir):  # ❌ Data operation in controller
        # ...
```

**Example - CORRECT:**
```python
# In controller - delegate to model
def train_model(self):
    faces, labels, label_map = self._data_manager.load_training_data()  # ✓
    self._face_recognizer.train(faces, labels)
```

---

### SOLID Principles

**Single Responsibility:**
- Each class has ONE reason to change
- `CameraService`: Only camera operations
- `FaceDetector`: Only face detection
- `FaceRecognizer`: Only face recognition

**Open/Closed:**
- Open for extension (subclassing)
- Closed for modification (don't change existing)

**Liskov Substitution:**
- Subclasses can replace base classes
- Maintain contracts in inheritance

**Interface Segregation:**
- Small, focused interfaces
- Don't force implementation of unused methods

**Dependency Inversion:**
- Depend on abstractions, not concretions
- Use dependency injection

---

## Common Pitfalls

### Pitfall 1: Hardcoding Values

**❌ WRONG:**
```python
def detect_faces(self, image):
    faces = self._cascade.detectMultiScale(image, 1.3, 5)  # Hardcoded!
```

**✅ CORRECT:**
```python
def detect_faces(self, image):
    faces = self._cascade.detectMultiScale(
        image,
        Config.DETECTION_SCALE_FACTOR,
        Config.DETECTION_MIN_NEIGHBORS
    )
```

---

### Pitfall 2: Ignoring Error Handling

**❌ WRONG:**
```python
def load_model(self, path):
    self._model.read(path)  # What if file doesn't exist?
```

**✅ CORRECT:**
```python
def load_model(self, path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found: {path}")
    
    try:
        self._model.read(path)
        self._is_trained = True
    except Exception as e:
        raise Exception(f"Failed to load model: {e}")
```

---

### Pitfall 3: Breaking Contracts

**❌ WRONG:**
```python
# Changing return type breaks contract!
def predict(self, face_image):
    pred_id, conf = self._model.predict(face_image)
    return {"id": pred_id, "confidence": conf}  # ❌ Changed from tuple to dict
```

**✅ CORRECT:**
```python
# Maintain contract
def predict(self, face_image):
    pred_id, conf = self._model.predict(face_image)
    return pred_id, conf  # ✓ Tuple as documented
```

---

### Pitfall 4: Assuming Features Exist

**❌ WRONG:**
```python
# Assuming batch prediction exists
results = recognizer.predict_batch(faces)  # Does NOT exist!
```

**✅ CORRECT:**
```python
# Check docs/models.md first
# No predict_batch() documented
# Implement manually:
results = [recognizer.predict(face) for face in faces]
```

---

## File Organization

### Where to Put New Code

**New model logic:**
- Location: `src/models/`
- Create new file: `src/models/new_feature.py`
- Follow existing patterns

**New controller logic:**
- Location: `src/controllers/`
- Extend existing controller or create new one

**New view logic:**
- Location: `src/views/`
- Separate console and video views

**New configuration:**
- Location: `config.py`
- Add to `Config` class

**New documentation:**
- Location: `docs/`
- Follow existing structure

---

## Version Control

### Commit Messages

**Format:**
```
<type>: <short description>

<detailed description>

<breaking changes if any>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance

**Example:**
```
feat: Add batch inference API

- Implemented predict_batch() in FaceRecognizer
- Updated docs/inference.md with API documentation
- Added usage examples

No breaking changes.
```

---

## When to Ask for Help

**ASK when:**
- Requirements unclear
- Multiple valid approaches
- Breaking change necessary
- Architecture decision needed
- Performance trade-offs involved
- Security implications

**DON'T ASK when:**
- Simple bug fix (obvious solution)
- Documentation update (clear what to document)
- Code formatting (follow existing style)
- Adding comments (self-explanatory)

---

## Quality Checklist

Before submitting code, verify:

### Functionality
- [ ] Code runs without errors
- [ ] Produces expected output
- [ ] Handles edge cases
- [ ] Error messages are clear

### Contracts
- [ ] Input contracts maintained
- [ ] Output contracts maintained
- [ ] No breaking changes (or documented)
- [ ] Backward compatible (if applicable)

### Code Quality
- [ ] Follows existing patterns
- [ ] No hardcoded values
- [ ] Proper error handling
- [ ] Clear variable names
- [ ] Appropriate comments (only where needed)

### Documentation
- [ ] Relevant docs updated
- [ ] API documented (if new function)
- [ ] Examples provided (if complex)
- [ ] KHÔNG XÁC MINH marked (if uncertain)

### Testing
- [ ] Manually tested
- [ ] Works with existing data
- [ ] No regressions
- [ ] Performance acceptable

---

## Emergency Procedures

### If You Break Something

1. **STOP:** Don't make it worse
2. **Identify:** What broke? What changed?
3. **Revert:** Undo breaking change
4. **Analyze:** Why did it break?
5. **Plan:** How to fix properly?
6. **Implement:** Fix with tests
7. **Verify:** Confirm fix works

### If You're Stuck

1. **Read docs:** Re-read relevant documentation
2. **Check code:** Verify actual implementation
3. **Search similar:** Look for similar patterns in codebase
4. **Simplify:** Break problem into smaller parts
5. **Ask:** Provide context and what you've tried

---

## Summary

**Golden Rules:**

1. **NO FABRICATION** - Only use what exists
2. **RESPECT CONTRACTS** - Don't break interfaces
3. **DOCUMENTATION FIRST** - Spec before code
4. **TEST BEFORE COMMIT** - Verify everything works
5. **NO ASSUMPTIONS** - Ask when uncertain

**Remember:**
- Read docs before coding
- Verify before assuming
- Test before committing
- Document as you go
- Ask when stuck

**When in doubt:**
- Check documentation
- Verify in code
- Ask for clarification
- Mark as "KHÔNG XÁC MINH"

---

## Quick Reference

**Key Files:**
- `config.py` - All configuration
- `main.py` - Entry point
- `src/controllers/face_recognition_controller.py` - Main workflow
- `src/models/face_recognizer.py` - LBPH model
- `src/models/face_detector.py` - Face detection
- `src/models/data_manager.py` - Data I/O

**Key Contracts:**
- Dataset: `dataset/<person>/<person>_<i>.jpg`, 200×200 grayscale
- Model input: (200, 200) uint8 grayscale
- Model output: (predicted_id: int, confidence: float)
- Config: All params via `Config` class

**Documentation:**
- Overview: `docs/overview.md`
- Pipeline: `docs/pipeline.md`
- Models: `docs/models.md`
- Configs: `docs/configs.md`
- All docs: `docs/`

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-15  
**Mandatory for:** All AI agents and automated tools working on this codebase
