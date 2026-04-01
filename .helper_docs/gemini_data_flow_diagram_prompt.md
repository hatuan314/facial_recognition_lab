# Prompt cho Gemini AI: Tạo Sơ Đồ Luồng Dữ Liệu (Data Flow Diagram)

## Mục Tiêu
Tạo một **Data Flow Diagram (DFD)** toàn diện cho ứng dụng Nhận Diện Khuôn Mặt được xây dựng bằng Python, OpenCV và thuật toán LBPH. Sơ đồ cần minh họa luồng dữ liệu hoàn chỉnh qua tất cả bốn giai đoạn chính của hệ thống.

---

## Tổng Quan Hệ Thống

**Tên Ứng Dụng:** Facial Recognition Lab  
**Kiến Trúc:** MVC (Model-View-Controller) + SOLID Principles  
**Technology Stack:** Python 3.7+, OpenCV (opencv-contrib-python), NumPy, Pickle  
**Algorithms:** Haar Cascade (detection), LBPH (recognition)

---

## Các Thành Phần Sơ Đồ Yêu Cầu

### 1. **Bốn Giai Đoạn Chính Cần Trực Quan Hóa**

#### **GIAI ĐOẠN 1: THU THẬP DỮ LIỆU (DATA COLLECTION)**
```
Nhập liệu từ người dùng (person_name) 
    ↓
[Controller] FaceRecognitionController.capture_faces()
    ↓
[Model] CameraService.open() → Luồng Camera (H×W×3 BGR)
    ↓
[Xử lý] cv2.cvtColor() → Grayscale (H×W uint8)
    ↓
[Model] FaceDetector.detect_faces() → Hình chữ nhật khuôn mặt [(x,y,w,h)]
    ↓
[Model] FaceDetector.extract_face_roi() → ROI (200×200 uint8)
    ↓
[Model] DataManager.save_face_image() → Lưu vào ổ đĩa
    ↓
dataset/<person_name>/<person_name>_<index>.jpg
    ↓
[View] VideoView.draw_rectangle() + show_frame() → Phản hồi trực quan
```

#### **GIAI ĐOẠN 2: HUẤN LUYỆN (TRAINING)**
```
[Controller] FaceRecognitionController.train_model()
    ↓
[Model] DataManager.load_training_data()
    ↓
Tải tất cả ảnh từ dataset/ → faces: List[(200,200)]
    ↓
Tạo ánh xạ nhãn → label_map: {"john": 0, "mary": 1}
    ↓
Tạo danh sách nhãn → labels: [0,0,0,...,1,1,1,...]
    ↓
[Model] FaceRecognizer.train(faces, labels)
    ↓
Thuật toán LBPH:
  - Tính toán Local Binary Patterns
  - Chia thành lưới 8×8 (64 ô)
  - Tạo histogram (256 bins mỗi ô)
  - Lưu trữ feature vectors (16,384 đặc trưng)
    ↓
[Model] DataManager.save_model()
    ↓
Lưu hai file:
  - trainer/trainer.yml (LBPH model)
  - trainer/labels.pickle (ánh xạ nhãn)
    ↓
[View] ConsoleView.show_success() → Thông báo người dùng
```

#### **GIAI ĐOẠN 3: SUY LUẬN (INFERENCE - Nhận Diện Thời Gian Thực)**
```
[Controller] FaceRecognitionController.recognize_faces()
    ↓
[Model] DataManager.load_model_and_labels()
    ↓
Tải: trainer.yml + labels.pickle
    ↓
Tạo reverse_map: {0: "john", 1: "mary"}
    ↓
[Model] CameraService.open() → Luồng Camera
    ↓
Vòng lặp (thời gian thực):
  ├─ Đọc frame (H×W×3 BGR)
  ├─ Chuyển sang grayscale (H×W uint8)
  ├─ [Model] FaceDetector.detect_faces() → [(x,y,w,h)]
  ├─ Với mỗi khuôn mặt:
  │   ├─ Trích xuất ROI (200×200 uint8)
  │   ├─ [Model] FaceRecognizer.predict(roi)
  │   ├─ Đầu ra: (predicted_id: int, confidence: float)
  │   ├─ Áp dụng ngưỡng (confidence < 80?)
  │   ├─ Nếu tin cậy: name = reverse_map[predicted_id], color = GREEN
  │   ├─ Nếu không: name = "Unknown", color = RED
  │   ├─ [View] VideoView.draw_face_rectangle(frame, rect, color)
  │   └─ [View] VideoView.draw_text(frame, name, position)
  └─ [View] VideoView.show_frame() → Hiển thị video có chú thích
    ↓
Thoát khi nhấn phím 'q'
```

#### **GIAI ĐOẠN 4: ĐÁNH GIÁ (EVALUATION)**
```
[Controller] FaceRecognitionController.evaluate_model()
    ↓
[Model] DataManager.load_training_data()
    ↓
[Model] ModelEvaluator.split_data() → Chia Train/Test (80/20)
    ↓
Kết quả chia:
  - train_faces, train_labels (80%)
  - test_faces, test_labels (20%)
    ↓
[Model] FaceRecognizer.train(train_faces, train_labels)
    ↓
Dự đoán trên tập test:
  Với mỗi test_face:
    ├─ predicted_id, confidence = predict(test_face)
    └─ Áp dụng ngưỡng → final_prediction
    ↓
[Model] ModelEvaluator.calculate_metrics()
    ↓
Tính toán:
  - Accuracy, Precision, Recall, F1-Score
  - Confusion Matrix
  - Độ chính xác theo từng người
  - Thống kê confidence
    ↓
[Model] ModelEvaluator.print_report()
    ↓
[View] ConsoleView → Hiển thị báo cáo toàn diện
```

---

### 2. **Các Tầng Kiến Trúc MVC**

**Models (Logic Nghiệp Vụ):**
- `CameraService` - Các thao tác camera
- `FaceDetector` - Phát hiện khuôn mặt (Haar Cascade)
- `FaceRecognizer` - Nhận diện khuôn mặt (LBPH)
- `DataManager` - Các thao tác File I/O
- `ModelEvaluator` - Tính toán các chỉ số

**Views (Giao Diện):**
- `ConsoleView` - Giao diện dòng lệnh
- `VideoView` - Hiển thị video và chú thích

**Controllers (Điều Phối):**
- `FaceRecognitionController` - Điều phối luồng công việc

---

### 3. **Định Dạng Dữ Liệu và Hợp Đồng**

| Giai Đoạn | Tên Dữ Liệu | Shape/Format | Type | Range |
|-----------|--------------|--------------|------|-------|
| Chụp từ camera | frame | (H, W, 3) | uint8 | [0, 255] |
| Grayscale | gray | (H, W) | uint8 | [0, 255] |
| Phát hiện khuôn mặt | faces | [(x,y,w,h), ...] | int | N/A |
| Trích xuất ROI | roi | (200, 200) | uint8 | [0, 255] |
| Ảnh huấn luyện | faces | List[(200, 200)] | uint8 | [0, 255] |
| Nhãn huấn luyện | labels | (N,) | int32 | [0, num_people) |
| Ánh xạ nhãn | label_map | {"name": id} | dict | N/A |
| Kết quả dự đoán | (id, conf) | (int, float) | - | id≥0, conf≥0 |
| File model | trainer.yml | YAML | file | ~4-5MB |
| File nhãn | labels.pickle | Binary | file | <1KB |

---

### 4. **Các Phép Biến Đổi Dữ Liệu Chính**

1. **BGR → Grayscale:** `cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)`
2. **Phát hiện khuôn mặt:** Haar Cascade → Bounding boxes
3. **Trích xuất ROI:** Crop + Resize về 200×200
4. **Ánh xạ nhãn:** Tên người → ID số
5. **Huấn luyện LBPH:** Ảnh → Histogram features
6. **Dự đoán:** ROI → (ID, Confidence)
7. **Ngưỡng hóa:** Confidence → Quyết định Chấp nhận/Từ chối
8. **Ánh xạ ngược:** ID số → Tên người

---

### 5. **Vị Trí Lưu Trữ**

```
dataset/
├── john_doe/
│   ├── john_doe_0.jpg (200×200 grayscale)
│   ├── john_doe_1.jpg
│   └── ... (30 images)
├── jane_smith/
│   └── ... (30 images)

trainer/
├── trainer.yml (LBPH model, YAML format)
└── labels.pickle (Label mapping, binary)

haarcascades/
└── haarcascade_frontalface_default.xml (Pre-trained cascade)
```

---

## Yêu Cầu Về Sơ Đồ

### **Phong Cách Trực Quan:**
- Sử dụng ký hiệu **flowchart** hoặc **data flow diagram**
- Phân biệt rõ ràng giữa:
  - **Các tiến trình** (hình chữ nhật/hình chữ nhật bo tròn)
  - **Kho dữ liệu** (hình trụ hoặc hình chữ nhật mở)
  - **Luồng dữ liệu** (mũi tên có nhãn)
  - **Thực thể bên ngoài** (User, Camera, Display)
- Sử dụng **mã màu** cho các tầng MVC:
  - Models: Xanh dương (Blue)
  - Views: Xanh lá (Green)
  - Controllers: Cam (Orange)
  - Kho dữ liệu: Xám (Gray)

### **Nhãn:**
- Hiển thị shapes/formats của dữ liệu trên mũi tên (ví dụ: "(200×200 uint8)")
- Bao gồm tên hàm (ví dụ: "FaceDetector.detect_faces()")
- Đánh dấu các ngưỡng quan trọng (ví dụ: "confidence < 80")

### **Bố Cục:**
- Sắp xếp theo các giai đoạn (4 phần riêng biệt hoặc swimlanes)
- Hiển thị rõ hướng luồng dữ liệu (từ trên xuống dưới hoặc trái sang phải)
- Nhóm các thành phần liên quan lại với nhau

### **Mức Độ Chi Tiết:**
- **Tổng quan cấp cao** hiển thị tất cả 4 giai đoạn
- Bao gồm các phép biến đổi dữ liệu chính
- Hiển thị các thao tác file I/O
- Chỉ rõ các vòng lặp nếu có (ví dụ: xử lý frame thời gian thực)

---

## Ví Dụ Về Ký Hiệu

```
[Nhập liệu từ người dùng: person_name]
        ↓
┌─────────────────────────────────────┐
│ Controller:                         │
│ FaceRecognitionController           │
│ .capture_faces(person_name, 30)     │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│ Model: CameraService                │
│ .open() → VideoCapture              │
└─────────────────────────────────────┘
        ↓ (H×W×3 BGR uint8)
┌─────────────────────────────────────┐
│ Xử lý:                            │
│ cv2.cvtColor(BGR→GRAY)              │
└─────────────────────────────────────┘
        ↓ (H×W uint8)
┌─────────────────────────────────────┐
│ Model: FaceDetector                 │
│ .detect_faces(gray)                 │
└─────────────────────────────────────┘
        ↓ [(x,y,w,h), ...]
        ...
```

---

## Thông Tin Bổ Sung

### **Hợp Đồng Quan Trọng:**
1. **Dataset:** `dataset/<person_name>/<person_name>_<index>.jpg` (200×200 grayscale JPEG)
2. **Đầu vào Model:** `(200, 200) uint8 grayscale`
3. **Đầu ra Model:** `(predicted_id: int, confidence: float)`
4. **Ngưỡng Confidence:** `< 80 = nhận diện được, ≥ 80 = không xác định`

### **Thuật Toán:**
- **Haar Cascade:** Viola-Jones (2001) - Phát hiện khuôn mặt dựa trên cạnh
- **LBPH:** Local Binary Patterns Histograms - Nhận diện dựa trên kết cấu

### **Hiệu Suất:**
- **Độ trễ:** <50ms mỗi khuôn mặt (thông thường trên CPU hiện đại)
- **Throughput:** 20+ FPS thời gian thực
- **Độ chính xác:** 80-85% (khuôn mặt chính diện, ánh sáng tốt)

---

Định Dạng Đầu Ra

Vui lòng tạo một **sơ đồ trực quan** (không phải code) có:
1. Hiển thị rõ ràng tất cả 4 giai đoạn
2. Minh họa luồng dữ liệu bằng mũi tên và nhãn
3. Bao gồm shapes và formats của dữ liệu
4. Phân biệt các thành phần MVC bằng màu sắc
5. Hiển thị vị trí lưu trữ file
6. Chỉ rõ các vòng lặp và điểm quyết định
7. Dễ đọc và được sắp xếp tốt

**Các loại sơ đồ ưu tiên:**
- Data Flow Diagram (DFD) Level 1 hoặc Level 2
- Flowchart có chú thích dữ liệu
- Sơ đồ kiến trúc hệ thống với luồng dữ liệu

**Định dạng:** Ảnh PNG hoặc SVG với độ phân giải cao (phù hợp cho tài liệu)

---

## Ghi Chú cho Gemini AI

- Đây là một **dự án giáo dục** minh họa thị giác máy tính cổ điển
- Tập trung vào **các phép biến đổi dữ liệu** và **luồng giữa các thành phần**
- Nhấn mạnh sự tách biệt của **kiến trúc MVC**
- Hiển thị cách dữ liệu di chuyển từ **camera → lưu trữ → model → hiển thị**
- Bao gồm các thao tác **file I/O** (lưu/tải model và ảnh)
- Nôi bật **vòng lặp thời gian thực** ở Giai đoạn 3 (inference)

---

**Mục Đích Tài Liệu:** Hướng dẫn Gemini AI tạo sơ đồ luồng dữ liệu chính xác  
**Đối Tượng Mục Tiêu:** Sinh viên, lập trình viên, nhà nghiên cứu  
**Mức Độ Phức Tạp:** Trung bình (giả định có kiến thức CV cơ bản)
