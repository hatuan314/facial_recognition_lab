# Experiments - Tracking and Reproducibility

## Experiment Overview

**KHÔNG XÁC MINH - The current implementation does NOT include experiment tracking.**

This document describes:
1. Current state (no tracking)
2. Proposed experiment conventions
3. Reproducibility guidelines
4. Experiment management best practices

---

## Current State

### What Does NOT Exist

**Missing experiment infrastructure:**
- ❌ Experiment tracking system
- ❌ Hyperparameter logging
- ❌ Metrics logging
- ❌ Model versioning
- ❌ Experiment comparison tools
- ❌ Reproducibility mechanisms
- ❌ MLflow/Weights & Biases integration

**Current behavior:**
- Models overwrite previous versions
- No record of training parameters
- No performance history
- Manual note-taking required

---

## Proposed Experiment Conventions

### Experiment Naming

**Naming format:**
```
exp_<date>_<time>_<description>

Examples:
- exp_20260115_230000_baseline
- exp_20260115_231500_threshold_tuning
- exp_20260116_100000_more_training_data
```

**Components:**
- Date: YYYYMMDD
- Time: HHMMSS
- Description: Short, descriptive (use underscores)

### Directory Structure

**Proposed structure:**
```
experiments/
├── exp_20260115_230000_baseline/
│   ├── config.json
│   ├── model/
│   │   ├── trainer.yml
│   │   └── labels.pickle
│   ├── metrics.json
│   ├── logs/
│   │   └── training.log
│   └── README.md
├── exp_20260115_231500_threshold_tuning/
│   └── ...
└── experiments.csv  # Summary of all experiments
```

---

## Experiment Configuration

### Config Logging

**Proposed config.json:**
```json
{
  "experiment_id": "exp_20260115_230000_baseline",
  "timestamp": "2026-01-15T23:00:00Z",
  "description": "Baseline LBPH model with default parameters",
  
  "dataset": {
    "num_people": 3,
    "total_images": 90,
    "images_per_person": {
      "john_doe": 30,
      "jane_smith": 30,
      "bob_jones": 30
    },
    "split": {
      "train": 0.7,
      "val": 0.15,
      "test": 0.15
    }
  },
  
  "model": {
    "algorithm": "LBPH",
    "parameters": {
      "radius": 1,
      "neighbors": 8,
      "grid_x": 8,
      "grid_y": 8
    }
  },
  
  "training": {
    "face_size": [200, 200],
    "detection_scale_factor": 1.3,
    "detection_min_neighbors": 5
  },
  
  "inference": {
    "confidence_threshold": 80
  },
  
  "environment": {
    "python_version": "3.9.7",
    "opencv_version": "4.5.3",
    "os": "macOS 12.0",
    "cpu": "Apple M1"
  }
}
```

### Logging Configuration

**Proposed implementation:**
```python
import json
import datetime
from config import Config

def log_experiment_config(experiment_id, dataset_info):
    """Log experiment configuration"""
    config_data = {
        "experiment_id": experiment_id,
        "timestamp": datetime.datetime.now().isoformat(),
        "dataset": dataset_info,
        "model": {
            "algorithm": "LBPH",
            "parameters": {
                "radius": 1,
                "neighbors": 8,
                "grid_x": 8,
                "grid_y": 8
            }
        },
        "training": {
            "face_size": list(Config.FACE_SIZE),
            "detection_scale_factor": Config.DETECTION_SCALE_FACTOR,
            "detection_min_neighbors": Config.DETECTION_MIN_NEIGHBORS
        },
        "inference": {
            "confidence_threshold": Config.CONFIDENCE_THRESHOLD
        }
    }
    
    config_path = f"experiments/{experiment_id}/config.json"
    with open(config_path, 'w') as f:
        json.dump(config_data, f, indent=2)
```

---

## Metrics Logging

### Training Metrics

**Proposed metrics.json:**
```json
{
  "training": {
    "duration_seconds": 8.5,
    "num_images": 90,
    "num_people": 3
  },
  
  "validation": {
    "accuracy": 0.92,
    "precision": 0.91,
    "recall": 0.93,
    "f1_score": 0.92,
    "confusion_matrix": [[10, 0, 0], [0, 9, 1], [1, 0, 9]]
  },
  
  "test": {
    "accuracy": 0.89,
    "precision": 0.88,
    "recall": 0.90,
    "f1_score": 0.89
  },
  
  "confidence_stats": {
    "mean_confidence_correct": 45.2,
    "mean_confidence_incorrect": 95.7,
    "optimal_threshold": 75
  }
}
```

### Logging Implementation

**Proposed code:**
```python
def log_experiment_metrics(experiment_id, metrics):
    """Log experiment metrics"""
    metrics_path = f"experiments/{experiment_id}/metrics.json"
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)

# Usage
metrics = {
    "training": {
        "duration_seconds": training_duration,
        "num_images": len(faces),
        "num_people": len(label_map)
    },
    "validation": {
        "accuracy": val_accuracy,
        "precision": val_precision,
        "recall": val_recall,
        "f1_score": val_f1
    }
}

log_experiment_metrics(experiment_id, metrics)
```

---

## Reproducibility Checklist

### Essential for Reproducibility

**✅ Must have:**
1. **Dataset snapshot:** Copy or reference to exact dataset used
2. **Configuration:** All hyperparameters logged
3. **Code version:** Git commit hash or code snapshot
4. **Environment:** Python version, library versions
5. **Random seeds:** If any randomness (not applicable to LBPH)
6. **Model checkpoint:** Saved model files

**✅ Nice to have:**
7. Training logs
8. Evaluation results
9. Visualization outputs
10. Hardware specifications

### Reproducibility Implementation

**Proposed script:**
```python
import json
import subprocess
import sys
import cv2
import numpy as np
from datetime import datetime

def create_reproducibility_manifest(experiment_id):
    """Create comprehensive reproducibility manifest"""
    
    # Git information
    try:
        git_commit = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD']
        ).decode().strip()
        git_branch = subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
        ).decode().strip()
    except:
        git_commit = "unknown"
        git_branch = "unknown"
    
    manifest = {
        "experiment_id": experiment_id,
        "timestamp": datetime.now().isoformat(),
        
        "code": {
            "git_commit": git_commit,
            "git_branch": git_branch,
            "git_dirty": subprocess.call(['git', 'diff-index', '--quiet', 'HEAD']) != 0
        },
        
        "environment": {
            "python_version": sys.version,
            "opencv_version": cv2.__version__,
            "numpy_version": np.__version__
        },
        
        "configuration": {
            "face_size": list(Config.FACE_SIZE),
            "confidence_threshold": Config.CONFIDENCE_THRESHOLD,
            "detection_scale_factor": Config.DETECTION_SCALE_FACTOR,
            "detection_min_neighbors": Config.DETECTION_MIN_NEIGHBORS,
            "default_samples": Config.DEFAULT_SAMPLES
        },
        
        "determinism": {
            "algorithm": "LBPH",
            "is_deterministic": True,
            "random_seed": "N/A (deterministic algorithm)"
        }
    }
    
    manifest_path = f"experiments/{experiment_id}/reproducibility.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    return manifest
```

---

## Experiment Tracking

### Manual Tracking

**Proposed experiments.csv:**
```csv
experiment_id,date,description,num_people,num_images,accuracy,precision,recall,threshold,notes
exp_20260115_230000_baseline,2026-01-15,Baseline LBPH,3,90,0.89,0.88,0.90,80,Initial baseline
exp_20260115_231500_threshold_tuning,2026-01-15,Lower threshold to 70,3,90,0.92,0.95,0.89,70,Better precision
exp_20260116_100000_more_data,2026-01-16,50 images per person,3,150,0.94,0.93,0.95,80,More training data helps
```

**Update script:**
```python
import csv

def log_experiment_summary(experiment_id, summary):
    """Append experiment to summary CSV"""
    csv_path = "experiments/experiments.csv"
    
    # Check if file exists
    file_exists = os.path.isfile(csv_path)
    
    with open(csv_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=summary.keys())
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(summary)

# Usage
summary = {
    "experiment_id": experiment_id,
    "date": datetime.now().strftime("%Y-%m-%d"),
    "description": "Baseline LBPH",
    "num_people": 3,
    "num_images": 90,
    "accuracy": 0.89,
    "precision": 0.88,
    "recall": 0.90,
    "threshold": 80,
    "notes": "Initial baseline"
}

log_experiment_summary(experiment_id, summary)
```

### MLflow Integration

**KHÔNG XÁC MINH - MLflow not currently integrated.**

**Proposed MLflow integration:**

```python
import mlflow
import mlflow.sklearn

def run_experiment_with_mlflow(experiment_name):
    """Run experiment with MLflow tracking"""
    
    mlflow.set_experiment(experiment_name)
    
    with mlflow.start_run():
        # Log parameters
        mlflow.log_param("face_size", Config.FACE_SIZE)
        mlflow.log_param("confidence_threshold", Config.CONFIDENCE_THRESHOLD)
        mlflow.log_param("detection_scale_factor", Config.DETECTION_SCALE_FACTOR)
        mlflow.log_param("num_people", len(label_map))
        mlflow.log_param("num_images", len(faces))
        
        # Train model
        start_time = time.time()
        recognizer.train(faces, labels)
        training_duration = time.time() - start_time
        
        # Log metrics
        mlflow.log_metric("training_duration", training_duration)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)
        
        # Log model
        mlflow.log_artifact("trainer/trainer.yml")
        mlflow.log_artifact("trainer/labels.pickle")
        
        # Log dataset info
        with open("dataset_info.json", "w") as f:
            json.dump(dataset_info, f)
        mlflow.log_artifact("dataset_info.json")

# Run MLflow UI
# mlflow ui --port 5000
```

---

## Experiment Comparison

### Comparison Script

**Proposed implementation:**
```python
import pandas as pd
import matplotlib.pyplot as plt

def compare_experiments(experiment_ids):
    """Compare multiple experiments"""
    
    results = []
    for exp_id in experiment_ids:
        metrics_path = f"experiments/{exp_id}/metrics.json"
        config_path = f"experiments/{exp_id}/config.json"
        
        with open(metrics_path) as f:
            metrics = json.load(f)
        
        with open(config_path) as f:
            config = json.load(f)
        
        results.append({
            "experiment_id": exp_id,
            "accuracy": metrics["test"]["accuracy"],
            "precision": metrics["test"]["precision"],
            "recall": metrics["test"]["recall"],
            "threshold": config["inference"]["confidence_threshold"],
            "num_images": config["dataset"]["total_images"]
        })
    
    df = pd.DataFrame(results)
    print(df)
    
    # Plot comparison
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    df.plot(x="experiment_id", y="accuracy", kind="bar", ax=axes[0])
    axes[0].set_title("Accuracy Comparison")
    
    df.plot(x="experiment_id", y="precision", kind="bar", ax=axes[1])
    axes[1].set_title("Precision Comparison")
    
    df.plot(x="experiment_id", y="recall", kind="bar", ax=axes[2])
    axes[2].set_title("Recall Comparison")
    
    plt.tight_layout()
    plt.savefig("experiments/comparison.png")
    plt.show()

# Usage
compare_experiments([
    "exp_20260115_230000_baseline",
    "exp_20260115_231500_threshold_tuning",
    "exp_20260116_100000_more_data"
])
```

---

## Experiment Workflow

### Standard Workflow

**Step-by-step process:**

1. **Create experiment:**
   ```python
   experiment_id = f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_description"
   os.makedirs(f"experiments/{experiment_id}", exist_ok=True)
   ```

2. **Log configuration:**
   ```python
   log_experiment_config(experiment_id, dataset_info)
   ```

3. **Train model:**
   ```python
   start_time = time.time()
   recognizer.train(faces, labels)
   training_duration = time.time() - start_time
   ```

4. **Evaluate model:**
   ```python
   metrics = evaluate_model(recognizer, X_test, y_test)
   ```

5. **Log metrics:**
   ```python
   log_experiment_metrics(experiment_id, metrics)
   ```

6. **Save model:**
   ```python
   model_path = f"experiments/{experiment_id}/model/trainer.yml"
   recognizer._model.save(model_path)
   ```

7. **Update summary:**
   ```python
   log_experiment_summary(experiment_id, summary)
   ```

8. **Document results:**
   ```python
   # Create README.md with findings
   with open(f"experiments/{experiment_id}/README.md", "w") as f:
       f.write(f"# {experiment_id}\n\n")
       f.write(f"## Results\n\n")
       f.write(f"- Accuracy: {metrics['accuracy']:.2%}\n")
       f.write(f"- Precision: {metrics['precision']:.2%}\n")
       f.write(f"- Recall: {metrics['recall']:.2%}\n")
   ```

---

## Hyperparameter Tuning

### Grid Search

**Proposed grid search:**
```python
from itertools import product

def grid_search_threshold():
    """Grid search for optimal confidence threshold"""
    
    thresholds = [60, 70, 80, 90, 100]
    results = []
    
    for threshold in thresholds:
        # Set threshold
        Config.CONFIDENCE_THRESHOLD = threshold
        
        # Evaluate
        predictions = []
        for face in X_val:
            pred_id, conf = recognizer.predict(face)
            if conf < threshold:
                predictions.append(pred_id)
            else:
                predictions.append(-1)
        
        # Metrics
        accuracy = accuracy_score(y_val, predictions)
        precision = precision_score(y_val, predictions, average='weighted')
        recall = recall_score(y_val, predictions, average='weighted')
        f1 = f1_score(y_val, predictions, average='weighted')
        
        results.append({
            "threshold": threshold,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1
        })
    
    # Find best
    df = pd.DataFrame(results)
    best = df.loc[df['f1'].idxmax()]
    
    print("Grid Search Results:")
    print(df)
    print(f"\nBest threshold: {best['threshold']} (F1: {best['f1']:.2%})")
    
    return best['threshold']
```

### Random Search

**KHÔNG XÁC MINH - Not applicable (LBPH has few hyperparameters).**

LBPH parameters (radius, neighbors, grid size) are typically not tuned extensively.

---

## Experiment Best Practices

### DO:
- ✅ Create unique experiment ID for each run
- ✅ Log all configuration parameters
- ✅ Save model checkpoints
- ✅ Document experiment purpose and findings
- ✅ Use version control (git commit hash)
- ✅ Compare experiments systematically
- ✅ Archive failed experiments (learn from failures)

### DON'T:
- ❌ Overwrite previous experiments
- ❌ Forget to log hyperparameters
- ❌ Skip documentation
- ❌ Cherry-pick best results
- ❌ Delete "failed" experiments
- ❌ Tune on test set (use validation set)

---

## Experiment Archive

### Archiving Strategy

**When to archive:**
- Experiment completed successfully
- Results documented
- Model saved
- No longer actively iterating

**Archive structure:**
```
experiments/
├── active/
│   └── exp_20260116_120000_current/
└── archive/
    ├── 2026-01/
    │   ├── exp_20260115_230000_baseline/
    │   └── exp_20260115_231500_threshold_tuning/
    └── 2026-02/
        └── ...
```

**Archive script:**
```python
import shutil

def archive_experiment(experiment_id):
    """Move experiment to archive"""
    month = experiment_id.split('_')[1][:6]  # YYYYMM
    year_month = f"{month[:4]}-{month[4:]}"
    
    archive_dir = f"experiments/archive/{year_month}"
    os.makedirs(archive_dir, exist_ok=True)
    
    src = f"experiments/active/{experiment_id}"
    dst = f"{archive_dir}/{experiment_id}"
    
    shutil.move(src, dst)
    print(f"Archived: {experiment_id}")
```

---

## Related Documentation

- [Training](training.md) - Training workflow
- [Evaluation](evaluation.md) - Evaluation metrics
- [Configs](configs.md) - Configuration system
- [Models](models.md) - Model details

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-15
