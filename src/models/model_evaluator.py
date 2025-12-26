# src/models/model_evaluator.py
import cv2
import numpy as np
import os
from config import Config
from src.models.data_manager import DataManager
from src.models.face_recognizer import FaceRecognizer

# Try to import sklearn, fallback to manual implementation if not available
try:
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("⚠️  scikit-learn chưa được cài đặt. Sử dụng implementation thủ công.")
    print("   Để có kết quả tốt hơn, chạy: pip install scikit-learn")

class ModelEvaluator:
    def __init__(self, test_split=0.2):
        """
        test_split: Tỷ lệ dữ liệu dùng cho test (0.2 = 20%)
        """
        self.test_split = test_split
        self.data_manager = DataManager()
        self.face_recognizer = FaceRecognizer()
    
    def _manual_accuracy_score(self, y_true, y_pred):
        """Tính accuracy thủ công"""
        return np.mean(np.array(y_true) == np.array(y_pred))
    
    def _manual_precision_score(self, y_true, y_pred, average='weighted'):
        """Tính precision thủ công"""
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        unique_labels = np.unique(np.concatenate([y_true, y_pred]))
        
        if average == 'weighted':
            precisions = []
            weights = []
            for label in unique_labels:
                if label == -1:  # Skip unknown
                    continue
                tp = np.sum((y_true == label) & (y_pred == label))
                fp = np.sum((y_true != label) & (y_pred == label))
                precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
                weight = np.sum(y_true == label)
                precisions.append(precision)
                weights.append(weight)
            
            if sum(weights) == 0:
                return 0.0
            return np.average(precisions, weights=weights)
        return 0.0
    
    def _manual_recall_score(self, y_true, y_pred, average='weighted'):
        """Tính recall thủ công"""
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        unique_labels = np.unique(np.concatenate([y_true, y_pred]))
        
        if average == 'weighted':
            recalls = []
            weights = []
            for label in unique_labels:
                if label == -1:  # Skip unknown
                    continue
                tp = np.sum((y_true == label) & (y_pred == label))
                fn = np.sum((y_true == label) & (y_pred != label))
                recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
                weight = np.sum(y_true == label)
                recalls.append(recall)
                weights.append(weight)
            
            if sum(weights) == 0:
                return 0.0
            return np.average(recalls, weights=weights)
        return 0.0
    
    def _manual_f1_score(self, y_true, y_pred, average='weighted'):
        """Tính F1 score thủ công"""
        precision = self._manual_precision_score(y_true, y_pred, average)
        recall = self._manual_recall_score(y_true, y_pred, average)
        if precision + recall == 0:
            return 0.0
        return 2 * (precision * recall) / (precision + recall)
    
    def _manual_confusion_matrix(self, y_true, y_pred):
        """Tính confusion matrix thủ công"""
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        unique_labels = np.unique(np.concatenate([y_true, y_pred]))
        
        cm = np.zeros((len(unique_labels), len(unique_labels)), dtype=int)
        label_to_idx = {label: idx for idx, label in enumerate(unique_labels)}
        
        for true_label, pred_label in zip(y_true, y_pred):
            true_idx = label_to_idx[true_label]
            pred_idx = label_to_idx[pred_label]
            cm[true_idx, pred_idx] += 1
        
        return cm
    
    def split_data(self, faces, labels, label_map):
        """
        Chia dữ liệu thành train và test
        """
        from collections import defaultdict
        
        # Nhóm ảnh theo label
        label_to_faces = defaultdict(list)
        for face, label in zip(faces, labels):
            label_to_faces[label].append(face)
        
        train_faces = []
        train_labels = []
        test_faces = []
        test_labels = []
        
        # Chia theo từng người để đảm bảo công bằng
        for label, face_list in label_to_faces.items():
            n_test = max(1, int(len(face_list) * self.test_split))
            
            # Shuffle để random
            indices = np.random.permutation(len(face_list))
            test_indices = indices[:n_test]
            train_indices = indices[n_test:]
            
            for idx in test_indices:
                test_faces.append(face_list[idx])
                test_labels.append(label)
            
            for idx in train_indices:
                train_faces.append(face_list[idx])
                train_labels.append(label)
        
        return train_faces, train_labels, test_faces, test_labels
    
    def evaluate(self, threshold=None):
        """
        Đánh giá model hiện tại
        """
        threshold = threshold or Config.CONFIDENCE_THRESHOLD
        
        # Load dữ liệu
        faces, labels, label_map = self.data_manager.load_training_data()
        
        if len(faces) == 0:
            raise ValueError("Không có dữ liệu để đánh giá.")
        
        print(f"Tổng số ảnh: {len(faces)}")
        print(f"Số người: {len(label_map)}")
        
        # Chia train/test
        train_faces, train_labels, test_faces, test_labels = self.split_data(
            faces, labels, label_map
        )
        
        print(f"\nTrain: {len(train_faces)} ảnh")
        print(f"Test: {len(test_faces)} ảnh")
        
        # Train model với train set
        print("\nĐang train model với train set...")
        self.face_recognizer.train(train_faces, train_labels)
        
        # Predict trên test set
        print("Đang đánh giá trên test set...")
        predictions = []
        confidences = []
        correct_predictions = 0
        
        for i, (test_face, true_label) in enumerate(zip(test_faces, test_labels)):
            predicted_id, confidence = self.face_recognizer.predict(test_face)
            
            # Áp dụng threshold
            if confidence < threshold:
                predictions.append(predicted_id)
            else:
                predictions.append(-1)  # Unknown
            
            confidences.append(confidence)
            
            if predicted_id == true_label and confidence < threshold:
                correct_predictions += 1
        
        # Tính metrics
        if HAS_SKLEARN:
            accuracy = accuracy_score(test_labels, predictions)
            precision = precision_score(test_labels, predictions, average='weighted', zero_division=0)
            recall = recall_score(test_labels, predictions, average='weighted', zero_division=0)
            f1 = f1_score(test_labels, predictions, average='weighted', zero_division=0)
            cm = confusion_matrix(test_labels, predictions)
        else:
            accuracy = self._manual_accuracy_score(test_labels, predictions)
            precision = self._manual_precision_score(test_labels, predictions, average='weighted')
            recall = self._manual_recall_score(test_labels, predictions, average='weighted')
            f1 = self._manual_f1_score(test_labels, predictions, average='weighted')
            cm = self._manual_confusion_matrix(test_labels, predictions)
        
        # Per-person accuracy
        reverse_map = {v: k for k, v in label_map.items()}
        per_person_acc = {}
        
        for label_id in label_map.values():
            mask = np.array(test_labels) == label_id
            if mask.sum() > 0:
                person_predictions = np.array(predictions)[mask]
                person_true = np.array(test_labels)[mask]
                person_acc = (person_predictions == person_true).sum() / len(person_predictions)
                per_person_acc[reverse_map[label_id]] = person_acc
        
        # Confidence statistics
        confidences = np.array(confidences)
        avg_confidence = confidences.mean()
        std_confidence = confidences.std()
        
        results = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'correct_predictions': correct_predictions,
            'total_test': len(test_faces),
            'confusion_matrix': cm,
            'per_person_accuracy': per_person_acc,
            'avg_confidence': avg_confidence,
            'std_confidence': std_confidence,
            'confidence_distribution': {
                'excellent (<30)': (confidences < 30).sum(),
                'very_good (30-50)': ((confidences >= 30) & (confidences < 50)).sum(),
                'good (50-70)': ((confidences >= 50) & (confidences < 70)).sum(),
                'acceptable (70-80)': ((confidences >= 70) & (confidences < 80)).sum(),
                'poor (80-100)': ((confidences >= 80) & (confidences < 100)).sum(),
                'very_poor (>100)': (confidences >= 100).sum()
            },
            'threshold': threshold
        }
        
        return results
    
    def print_report(self, results):
        """
        In báo cáo đánh giá
        """
        print("\n" + "="*60)
        print("BÁO CÁO ĐÁNH GIÁ MODEL")
        print("="*60)
        
        print(f"\n📊 METRICS TỔNG QUAN:")
        print(f"  Accuracy:  {results['accuracy']*100:.2f}%")
        print(f"  Precision: {results['precision']*100:.2f}%")
        print(f"  Recall:    {results['recall']*100:.2f}%")
        print(f"  F1-Score:  {results['f1_score']*100:.2f}%")
        
        print(f"\n✅ KẾT QUẢ:")
        print(f"  Đúng: {results['correct_predictions']}/{results['total_test']}")
        print(f"  Sai:  {results['total_test'] - results['correct_predictions']}/{results['total_test']}")
        
        print(f"\n🎯 CONFIDENCE STATISTICS:")
        print(f"  Trung bình: {results['avg_confidence']:.2f}")
        print(f"  Độ lệch chuẩn: {results['std_confidence']:.2f}")
        print(f"  Threshold: {results['threshold']}")
        
        print(f"\n📈 PHÂN BỐ CONFIDENCE:")
        dist = results['confidence_distribution']
        print(f"  Xuất sắc (<30):    {dist['excellent (<30)']}")
        print(f"  Rất tốt (30-50):   {dist['very_good (30-50)']}")
        print(f"  Tốt (50-70):       {dist['good (50-70)']}")
        print(f"  Chấp nhận (70-80): {dist['acceptable (70-80)']}")
        print(f"  Kém (80-100):      {dist['poor (80-100)']}")
        print(f"  Rất kém (>100):    {dist['very_poor (>100)']}")
        
        print(f"\n👤 ACCURACY THEO TỪNG NGƯỜI:")
        for person, acc in results['per_person_accuracy'].items():
            print(f"  {person}: {acc*100:.2f}%")
        
        print("\n" + "="*60)