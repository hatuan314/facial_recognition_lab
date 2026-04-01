# Prompt cho Gemini AI: Giai Đoạn 4 - Đánh Giá Model

## Mục Tiêu
Tạo một **Data Flow Diagram (DFD)** chi tiết cho **Giai Đoạn 4: Đánh Giá Model** của ứng dụng Nhận Diện Khuôn Mặt. Sơ đồ cần minh họa luồng dữ liệu hoàn chỉnh từ việc chia dữ liệu đến tính toán và hiển thị các chỉ số đánh giá.

---

## Thông Tin Giai Đoạn

**Tên Giai Đoạn:** ĐÁNH GIÁ MODEL (EVALUATION)  
**Mục Đích:** Đánh giá hiệu suất của model đã train bằng các metrics chuẩn  
**Đầu Vào:** Toàn bộ dataset từ thư mục dataset/  
**Đầu Ra:** Báo cáo chi tiết về accuracy, precision, recall, F1-score

---

## Luồng Dữ Liệu Chi Tiết

```
[Controller] FaceRecognitionController.evaluate_model(use_cross_validation=False)
    ↓
[Model] DataManager.load_training_data()
    ↓
Tải toàn bộ dataset:
  ├─ faces: List[np.ndarray] - Mỗi ảnh (200×200 uint8)
  ├─ labels: List[int] - Nhãn tương ứng
  └─ label_map: Dict[str, int] - {"john_doe": 0, "jane_smith": 1, ...}
    ↓
[Model] ModelEvaluator.split_data(faces, labels, label_map, test_split=0.2)
    ↓
Stratified Split (80/20):
  ├─ train_faces, train_labels (80% dữ liệu)
  ├─ test_faces, test_labels (20% dữ liệu)
  └─ Đảm bảo tỷ lệ mỗi người được giữ nguyên
    ↓
[Model] FaceRecognizer.train(train_faces, train_labels)
    ↓
Huấn luyện trên tập train:
  ├─ Tính LBPH features cho training set
  ├─ Lưu histogram cho mỗi label
  └─ Internal state: Trained model
    ↓
[Model] FaceRecognizer.predict() trên tập test:
    ↓
Với mỗi test_face trong test_faces:
  ├─ predicted_id, confidence = predict(test_face)
  ├─ Áp dụng threshold (confidence < 80?)
  │   ├─ Nếu confident: final_prediction = predicted_id
  │   └─ Nếu không: final_prediction = -1 (Unknown)
  └─ Lưu vào predictions list
    ↓
[Model] ModelEvaluator.calculate_metrics(test_labels, predictions)
    ↓
Tính toán các metrics:
  ├─ Accuracy = (correct_predictions) / (total_predictions)
  ├─ Precision = TP / (TP + FP)
  ├─ Recall = TP / (TP + FN)
  ├─ F1-Score = 2 × (Precision × Recall) / (Precision + Recall)
  ├─ Confusion Matrix (num_people × num_people)
  ├─ Per-person accuracy (cho mỗi người)
  └─ Confidence statistics (mean, std, min, max)
    ↓
[Model] ModelEvaluator.print_report(results)
    ↓
Hiển thị báo cáo toàn diện:
  ├─ Overall metrics (Accuracy, Precision, Recall, F1)
  ├─ Confusion Matrix (visual table)
  ├─ Per-person performance
  ├─ Confidence analysis
  └─ Dataset statistics
```

---

## Thành Phần MVC Trong Giai Đoạn Này

### **Controller:**
- `FaceRecognitionController.evaluate_model()`
- Điều phối toàn bộ luồng đánh giá

### **Models:**
- `DataManager` - Tải dữ liệu
- `ModelEvaluator` - Chia dữ liệu và tính metrics
- `FaceRecognizer` - Huấn luyện và dự đoán

### **Views:**
- `ConsoleView` - Hiển thị báo cáo kết quả

---

## Chi Tiết Các Metrics

### **Basic Metrics:**
```
Accuracy = (Số dự đoán đúng) / (Tổng số dự đoán)
Precision = True Positives / (True Positives + False Positives)
Recall = True Positives / (True Positives + False Negatives)
F1-Score = 2 × (Precision × Recall) / (Precision + Recall)
```

### **Confusion Matrix:**
```
           Predicted
           │  0  │  1  │  2  │ Unknown
Actual ────┼─────┼─────┼─────┼─────────
    0      │ TP  │ FN  │ FN  │ FN
    1      │ FP  │ TP  │ FP  │ FP
    2      │ FP  │ FP  │ TP  │ FP
```

### **Per-Person Analysis:**
```
john_doe:    Accuracy = 85% (17/20 correct)
jane_smith:  Accuracy = 90% (18/20 correct)
bob_jones:   Accuracy = 75% (15/20 correct)
```

---

## Định Dạng Dữ Liệu

| Giai Đoạn | Dữ Liệu | Shape/Format | Type | Mô Tả |
|-----------|----------|--------------|------|-------|
| Full dataset | faces | List[(200,200)] | uint8 | N×200×200 |
| Full dataset | labels | (N,) | int32 | N |
| Train set | train_faces | List[(200,200)] | uint8 | 0.8N×200×200 |
| Train set | train_labels | (0.8N,) | int32 | 0.8N |
| Test set | test_faces | List[(200,200)] | uint8 | 0.2N×200×200 |
| Test set | test_labels | (0.2N,) | int32 | 0.2N |
| Predictions | predictions | (0.2N,) | int | -1 hoặc [0, num_people) |
| Metrics | results | dict | mixed | Various types |

---

## Các Phép Biến Đổi Dữ Liệu

1. **Data Loading:** Files → NumPy arrays + labels
2. **Train/Test Split:** Full dataset → Train + Test sets
3. **Model Training:** Train faces → Trained model
4. **Prediction:** Test faces → Predictions + confidences
5. **Thresholding:** Confidence → Binary decisions
6. **Metrics Calculation:** Predictions vs Labels → Performance metrics
7. **Report Generation:** Metrics → Formatted output

---

## Yêu Cầu Sơ Đồ

### **Phong Cách Trực Quan:**
- Sử dụng ký hiệu **flowchart** hoặc **data flow diagram**
- Phân biệt các thành phần MVC bằng màu sắc:
  - Controller: Cam (Orange)
  - Models: Xanh dương (Blue)
  - Views: Xanh lá (Green)
  - Data stores: Xám (Gray)

### **Nhãn và Ghi Chú:**
- Hiển thị tỷ lệ split (80/20)
- Bao gồm tên các metrics (Accuracy, Precision, Recall, F1)
- Đánh dấu threshold (confidence < 80)
- Hiển thị confusion matrix structure

### **Bố Cục:**
- Sắp xếp theo thứ tự xử lý
- Nhóm các bước tính metrics
- Hiển thị rõ input từ dataset/
- Vẽ rõ output là báo cáo

### **Các Yếu Tố Cần Nhấn Mạnh:**
- **Data Splitting:** Chia train/test với stratification
- **Training Phase:** Huấn luyện lại model trên train set
- **Prediction Phase:** Dự đoán trên test set
- **Metrics Calculation:** Tính toán các chỉ số đánh giá
- **Report Generation:** Hiển thị báo cáo toàn diện

---

## Ví Dụ Cụ Thể

**Với 3 người, mỗi người 30 ảnh (tổng 90 ảnh):**
```
Input:
  - Total: 90 images
  - Split: Train 72 images, Test 18 images

Processing:
  - Train on 72 images (24 per person)
  - Predict on 18 images (6 per person)

Output Metrics:
  - Overall Accuracy: 83.3% (15/18 correct)
  - Precision: 0.85
  - Recall: 0.83
  - F1-Score: 0.84
  - Confusion Matrix: 3×3 matrix
  - Per-person: john_doe: 85%, jane_smith: 83%, bob_jones: 82%
```

---

## Cross-Validation (Optional)

```
Nếu use_cross_validation=True:
  ├─ Chia dữ liệu thành K folds (K=5)
  ├─ Với mỗi fold:
  │   ├─ Train trên K-1 folds
  │   ├─ Test trên 1 fold
  │   └─ Tính metrics
  └─ Average metrics across K folds
```

---

## Ghi Chú Cho Gemini AI

- Đây là **Giai Đoạn 4** trong 4 giai đoạn của hệ thống
- Tập trung vào **đánh giá hiệu suất model**
- Nhấn mạnh **các metrics đánh giá** và **confusion matrix**
- Hiển thị rõ **train/test split** và **cross-validation**
- Đây là giai đoạn **validation** để kiểm tra chất lượng model

---

**Định Dạng Đầu Ra:** PNG hoặc SVG với độ phân giải cao  
**Mức Độ Chi Tiết:** Chi tiết, hiển thị metrics và confusion matrix
