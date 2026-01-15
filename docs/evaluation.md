# Evaluation - Metrics and Protocol

## Evaluation Overview

The facial recognition system now includes **formal evaluation functionality** through the `ModelEvaluator` class, providing comprehensive metrics and analysis of model performance.

**Implemented features:**
- ✅ Train/test split with stratified sampling
- ✅ Accuracy, precision, recall, F1-score metrics
- ✅ Confusion matrix
- ✅ Per-person accuracy analysis
- ✅ Confidence statistics and distribution
- ✅ Cross-validation support
- ✅ Manual metrics fallback (no scikit-learn required)

This document describes:
1. Current implementation (fully functional)
2. Evaluation API and usage
3. Metrics calculations
4. Interpretation guidelines

---

## Current State

### What Exists

**Automated evaluation system:**
- `ModelEvaluator` class in `src/models/model_evaluator.py`
- `evaluate_model()` method in `FaceRecognitionController`
- Train/test split with stratified sampling (default 80/20)
- Full metrics suite (accuracy, precision, recall, F1)
- Confusion matrix visualization
- Per-person accuracy breakdown
- Confidence statistics and distribution analysis
- Cross-validation support (k-fold)
- Manual metrics fallback when scikit-learn unavailable

**CLI integration:**
- Menu option 4: "Đánh giá accuracy"
- Interactive evaluation with detailed reports
- Both single evaluation and cross-validation modes

**Implicit evaluation:**
- Confidence scores during inference
- Visual feedback (green = correct, red = unknown)
- User subjective assessment

### What Does NOT Exist

**Missing components:**
- ❌ ROC curves (not applicable to LBPH)
- ❌ AUC metrics (not applicable to LBPH)
- ❌ Learning curves (single-shot training)
- ❌ Hyperparameter optimization
- ❌ Automated threshold tuning

---

## Evaluation Entrypoints

### CLI Entrypoint

**Command:**
```bash
python main.py
```

**Interactive menu:**
```
1. Thu ảnh training
2. Train model
3. Nhận diện realtime
4. Đánh giá accuracy  ← Select this option
0. Thoát
```

**Process:**
1. Loads trained model from `trainer/trainer.yml`
2. Splits dataset into train/test (80/20 by default)
3. Trains model on train set
4. Evaluates on test set
5. Displays comprehensive report

---

### Programmatic Entrypoint

**File:** `src/controllers/face_recognition_controller.py`  
**Method:** `FaceRecognitionController.evaluate_model(use_cross_validation=False)`

**Usage:**
```python
from src.controllers.face_recognition_controller import FaceRecognitionController

controller = FaceRecognitionController()

# Single evaluation
results = controller.evaluate_model()

# Cross-validation
results = controller.evaluate_model(use_cross_validation=True)
```

**Direct evaluation:**
```python
from src.models.model_evaluator import ModelEvaluator

evaluator = ModelEvaluator(test_split=0.2)
results = evaluator.evaluate()
evaluator.print_report(results)
```

---

## Data Splitting Strategy

**Current implementation:**
```python
# ModelEvaluator.split_data() - Stratified sampling
train_faces, train_labels, test_faces, test_labels = evaluator.split_data(
    faces, labels, label_map
)
```

**Split characteristics:**
- Default: 80% train, 20% test
- Stratified by person (ensures each person represented in both sets)
- Random shuffle within each person's images
- Minimum 1 test image per person (even with small datasets)

**Example with 30 images per person:**
- Training: ~24 images per person
- Test: ~6 images per person

**Cross-validation:**
- k-fold cross-validation (default k=5)
- Stratified folds
- Averages metrics across folds

---

## Evaluation Metrics

### Classification Metrics

#### 1. Accuracy

**Definition:** Percentage of correct predictions

**Implementation:**
```python
# ModelEvaluator._manual_accuracy_score() or sklearn.metrics.accuracy_score
accuracy = np.mean(np.array(y_true) == np.array(y_pred))
```

**Current calculation:**
- Predictions with confidence < threshold are considered
- Predictions with confidence ≥ threshold are marked as "Unknown" (-1)
- Accuracy includes correct rejections (Unknown predictions for unknown faces)

**Interpretation:**
- 90-100%: Excellent
- 80-90%: Good
- 70-80%: Acceptable
- <70%: Poor (needs improvement)

#### 2. Precision

**Definition:** Of predicted positives, how many are correct?

**Implementation:**
```python
# ModelEvaluator._manual_precision_score() or sklearn.metrics.precision_score
precision = tp / (tp + fp)  # Weighted average across all labels
```

**Current calculation:**
- Weighted precision across all person labels
- Unknown predictions (-1) are excluded from precision calculation
- Handles cases where no true positives (returns 0.0)

**Use case:** Minimize false positives (wrong person recognized)

#### 3. Recall

**Definition:** Of actual positives, how many are detected?

**Implementation:**
```python
# ModelEvaluator._manual_recall_score() or sklearn.metrics.recall_score
recall = tp / (tp + fn)  # Weighted average across all labels
```

**Current calculation:**
- Weighted recall across all person labels
- Unknown predictions (-1) are excluded from recall calculation
- Handles cases where no true positives (returns 0.0)

**Use case:** Minimize false negatives (person not recognized)

#### 4. F1 Score

**Definition:** Harmonic mean of precision and recall

**Implementation:**
```python
# ModelEvaluator._manual_f1_score() or sklearn.metrics.f1_score
f1 = 2 * (precision * recall) / (precision + recall)
```

**Current calculation:**
- Weighted F1 score across all person labels
- Returns 0.0 if both precision and recall are 0.0

**Use case:** Balanced metric when precision and recall both matter

#### 5. Confusion Matrix

**Definition:** Matrix showing predicted vs. actual labels

**Implementation:**
```python
# ModelEvaluator._manual_confusion_matrix() or sklearn.metrics.confusion_matrix
cm = np.zeros((len(unique_labels), len(unique_labels)), dtype=int)
for true_label, pred_label in zip(y_true, y_pred):
    cm[true_idx, pred_idx] += 1
```

**Current calculation:**
- Includes all labels (including -1 for Unknown)
- Square matrix with all unique labels
- Rows: actual labels, Columns: predicted labels

**Interpretation:**
- Diagonal: Correct predictions
- Off-diagonal: Misclassifications
- Identify which people are confused with each other

---

### Additional Metrics

#### 6. Per-Person Accuracy

**Definition:** Accuracy calculated separately for each person

**Implementation:**
```python
# ModelEvaluator.evaluate() - per_person_accuracy
per_person_acc = {}
for label_id in label_map.values():
    mask = np.array(test_labels) == label_id
    person_predictions = np.array(predictions)[mask]
    person_true = np.array(test_labels)[mask]
    person_acc = (person_predictions == person_true).sum() / len(person_predictions)
```

**Use case:** Identify which people are harder/easier to recognize

#### 7. Confidence Statistics

**Definition:** Statistical analysis of confidence scores

**Metrics calculated:**
- Mean confidence
- Standard deviation
- Distribution across ranges (<30, 30-50, 50-70, 70-80, 80-100, >100)

**Use case:** Understand model confidence patterns and threshold effectiveness

---

### Confidence-Based Metrics

#### Confidence Distribution

**Analysis:**
```python
import numpy as np

confidences_correct = []
confidences_incorrect = []

for face, true_label in zip(X_test, y_test):
    pred_id, conf = model.predict(face)
    if pred_id == true_label:
        confidences_correct.append(conf)
    else:
        confidences_incorrect.append(conf)

print(f"Correct predictions - Mean confidence: {np.mean(confidences_correct):.2f}")
print(f"Incorrect predictions - Mean confidence: {np.mean(confidences_incorrect):.2f}")
```

**Expected behavior:**
- Correct predictions should have lower confidence scores
- Incorrect predictions should have higher confidence scores
- Clear separation indicates good model calibration

#### Threshold Analysis

**Find optimal threshold:**
```python
from sklearn.metrics import accuracy_score

thresholds = range(40, 120, 5)
accuracies = []

for threshold in thresholds:
    predictions = []
    for face, true_label in zip(X_test, y_test):
        pred_id, conf = model.predict(face)
        if conf < threshold:
            predictions.append(pred_id)
        else:
            predictions.append(-1)  # Unknown
    
    acc = accuracy_score(y_test, predictions)
    accuracies.append(acc)

optimal_threshold = thresholds[np.argmax(accuracies)]
print(f"Optimal threshold: {optimal_threshold}")
```

---

### Recognition Rate Metrics

#### True Acceptance Rate (TAR)

**Definition:** Rate at which genuine users are correctly accepted

```python
genuine_attempts = [(face, label) for face, label in zip(X_test, y_test)]
accepted = 0

for face, true_label in genuine_attempts:
    pred_id, conf = model.predict(face)
    if pred_id == true_label and conf < Config.CONFIDENCE_THRESHOLD:
        accepted += 1

tar = accepted / len(genuine_attempts)
print(f"True Acceptance Rate: {tar:.2%}")
```

#### False Acceptance Rate (FAR)

**Definition:** Rate at which impostors are incorrectly accepted

```python
# Test with unknown faces (not in training set)
impostor_faces = load_unknown_faces()  # KHÔNG XÁC MINH - not implemented
accepted = 0

for face in impostor_faces:
    pred_id, conf = model.predict(face)
    if conf < Config.CONFIDENCE_THRESHOLD:
        accepted += 1

far = accepted / len(impostor_faces)
print(f"False Acceptance Rate: {far:.2%}")
```

#### False Rejection Rate (FRR)

**Definition:** Rate at which genuine users are incorrectly rejected

```python
frr = 1 - tar
print(f"False Rejection Rate: {frr:.2%}")
```

---

## Cross-Validation

**KHÔNG XÁC MINH - Not currently implemented.**

**Proposed k-fold cross-validation:**

```python
from sklearn.model_selection import KFold

kfold = KFold(n_splits=5, shuffle=True, random_state=42)
accuracies = []

for fold, (train_idx, val_idx) in enumerate(kfold.split(faces)):
    X_train_fold = [faces[i] for i in train_idx]
    y_train_fold = [labels[i] for i in train_idx]
    X_val_fold = [faces[i] for i in val_idx]
    y_val_fold = [labels[i] for i in val_idx]
    
    # Train
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(X_train_fold, np.array(y_train_fold))
    
    # Evaluate
    predictions = []
    for face in X_val_fold:
        pred_id, conf = model.predict(face)
        predictions.append(pred_id if conf < 80 else -1)
    
    acc = accuracy_score(y_val_fold, predictions)
    accuracies.append(acc)
    print(f"Fold {fold+1}: {acc:.2%}")

print(f"Mean Accuracy: {np.mean(accuracies):.2%} ± {np.std(accuracies):.2%}")
```

**Benefits:**
- More robust accuracy estimate
- Detects overfitting
- Uses all data for both training and validation

---

## Manual Testing Protocol

### Testing Procedure

**Current manual testing:**

1. **Train model:**
   ```bash
   python main.py
   > Choose: 2
   ```

2. **Run recognition:**
   ```bash
   python main.py
   > Choose: 3
   ```

3. **Test scenarios:**
   - ✅ Known person, frontal face → Should show name (green)
   - ✅ Known person, slight angle → Should show name (green)
   - ✅ Known person, different lighting → Should show name (green)
   - ✅ Unknown person → Should show "Unknown" (red)
   - ✅ No face in frame → No detection

4. **Record observations:**
   - Which people are recognized correctly?
   - Which people are confused?
   - What conditions cause failures?

### Test Cases

**Positive tests (should recognize):**
- Same person, same conditions as training
- Same person, slight variations (angle, expression)
- Same person, different time of day

**Negative tests (should reject):**
- Unknown person (not in training set)
- Known person with extreme angle (>45°)
- Known person with occlusion (glasses, mask)
- No face in frame

**Edge cases:**
- Multiple faces in frame
- Partial face visible
- Very close to camera
- Very far from camera
- Poor lighting conditions

---

## Performance Benchmarks

**KHÔNG XÁC MINH - No formal benchmarks available.**

**Proposed benchmarks:**

### Accuracy Benchmarks

| Scenario | Expected Accuracy | Notes |
|----------|------------------|-------|
| Controlled environment | >90% | Same lighting, frontal faces |
| Varied lighting | >80% | Different times of day |
| Slight angles (±15°) | >75% | Minor pose variation |
| Varied expressions | >85% | Smiling, neutral, etc. |

### Speed Benchmarks

| Metric | Target | Notes |
|--------|--------|-------|
| Inference latency | <50ms | Per face detection |
| FPS | >20 | Real-time video |
| Training time | <30s | For 300 images |

---

## Error Analysis

**KHÔNG XÁC MINH - No automated error analysis.**

**Proposed error analysis:**

### Misclassification Analysis

```python
# Identify misclassified examples
errors = []
for i, (face, true_label) in enumerate(zip(X_test, y_test)):
    pred_id, conf = model.predict(face)
    if pred_id != true_label:
        errors.append({
            'index': i,
            'true_label': true_label,
            'pred_label': pred_id,
            'confidence': conf,
            'image': face
        })

print(f"Total errors: {len(errors)}")

# Analyze error patterns
for error in errors[:5]:  # Show first 5 errors
    print(f"True: {reverse_map[error['true_label']]}, "
          f"Predicted: {reverse_map[error['pred_label']]}, "
          f"Confidence: {error['confidence']:.2f}")
```

### Common Error Patterns

**Typical issues:**
1. **Lighting variations:** Different lighting between training and test
2. **Pose variations:** Face angle differs from training
3. **Similar appearances:** Two people look similar
4. **Poor quality:** Blurry or low-contrast images
5. **Occlusions:** Glasses, hair, hands covering face

---

## Evaluation Reports

**KHÔNG XÁC MINH - No automated reporting.**

**Proposed evaluation report:**

```python
def generate_evaluation_report(model, X_test, y_test, label_map):
    """Generate comprehensive evaluation report"""
    from sklearn.metrics import classification_report
    
    # Predictions
    predictions = []
    confidences = []
    for face in X_test:
        pred_id, conf = model.predict(face)
        predictions.append(pred_id if conf < 80 else -1)
        confidences.append(conf)
    
    # Classification report
    report = classification_report(
        y_test, predictions, 
        target_names=[label_map[i] for i in sorted(label_map.values())]
    )
    
    # Summary statistics
    accuracy = accuracy_score(y_test, predictions)
    mean_conf = np.mean(confidences)
    
    # Generate report
    report_text = f"""
    ===== EVALUATION REPORT =====
    Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    Dataset:
    - Test samples: {len(X_test)}
    - Number of people: {len(label_map)}
    
    Performance:
    - Accuracy: {accuracy:.2%}
    - Mean confidence: {mean_conf:.2f}
    
    Classification Report:
    {report}
    
    ============================
    """
    
    return report_text
```

---

## Threshold Tuning

### Current Threshold

**From `config.py`:**
```python
CONFIDENCE_THRESHOLD = 80
```

### Tuning Process

**Manual tuning:**
1. Start with default (80)
2. Run inference on test set
3. Observe false positives and false negatives
4. Adjust threshold:
   - Increase if too many false positives
   - Decrease if too many false negatives
5. Repeat until satisfied

**Automated tuning:**
```python
def find_optimal_threshold(model, X_val, y_val):
    """Find threshold that maximizes F1 score"""
    best_f1 = 0
    best_threshold = 80
    
    for threshold in range(40, 120, 5):
        predictions = []
        for face, true_label in zip(X_val, y_val):
            pred_id, conf = model.predict(face)
            if conf < threshold:
                predictions.append(pred_id)
            else:
                predictions.append(-1)
        
        f1 = f1_score(y_val, predictions, average='weighted')
        if f1 > best_f1:
            best_f1 = f1
            best_threshold = threshold
    
    return best_threshold, best_f1

optimal_threshold, f1 = find_optimal_threshold(model, X_val, y_val)
print(f"Optimal threshold: {optimal_threshold} (F1: {f1:.2%})")
```

---

## Evaluation Best Practices

### DO:
- ✅ Use separate test set (never seen during training)
- ✅ Stratify splits to maintain class balance
- ✅ Test in conditions similar to deployment
- ✅ Document evaluation methodology
- ✅ Report multiple metrics (not just accuracy)
- ✅ Analyze errors to identify patterns

### DON'T:
- ❌ Evaluate on training data (overfitting bias)
- ❌ Tune threshold on test set (data leakage)
- ❌ Cherry-pick best results
- ❌ Ignore edge cases
- ❌ Report only accuracy (incomplete picture)

---

## Continuous Evaluation

**KHÔNG XÁC MINH - No continuous evaluation system.**

**Proposed monitoring:**

```python
# Log predictions during inference
prediction_log = []

def log_prediction(true_label, pred_label, confidence):
    prediction_log.append({
        'timestamp': datetime.now(),
        'true_label': true_label,
        'pred_label': pred_label,
        'confidence': confidence,
        'correct': true_label == pred_label
    })

# Periodic evaluation
def evaluate_recent_predictions(window_hours=24):
    """Evaluate predictions from last N hours"""
    cutoff = datetime.now() - timedelta(hours=window_hours)
    recent = [p for p in prediction_log if p['timestamp'] > cutoff]
    
    if not recent:
        return
    
    accuracy = sum(p['correct'] for p in recent) / len(recent)
    mean_conf = np.mean([p['confidence'] for p in recent])
    
    print(f"Last {window_hours}h: Accuracy={accuracy:.2%}, Mean Conf={mean_conf:.2f}")
```

---

## Related Documentation

- [Training](training.md) - Training workflow
- [Models](models.md) - Model architecture and confidence scoring
- [Inference](inference.md) - Inference API
- [Configs](configs.md) - Threshold configuration
- [Experiments](experiments.md) - Experiment tracking

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-15
