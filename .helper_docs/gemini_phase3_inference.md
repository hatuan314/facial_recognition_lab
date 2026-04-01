# Prompt cho Gemini AI: Giai Đoạn 3 - Suy Luận Thời Gian Thực

## Mục Tiêu
Tạo một **Data Flow Diagram (DFD)** chi tiết cho **Giai Đoạn 3: Suy Luận Thời Gian Thực (Inference)** của ứng dụng Nhận Diện Khuôn Mặt. Sơ đồ cần minh họa luồng dữ liệu hoàn chỉnh từ việc tải model đến nhận diện real-time trên video.

---

## Thông Tin Giai Đoạn

**Tên Giai Đoạn:** SUY LUẬN THỜI GIAN THỰC (INFERENCE)  
**Mục Đích:** Nhận diện khuôn mặt real-time từ camera sử dụng model đã train  
**Đầu Vào:** Luồng video từ camera, model đã train (trainer.yml, labels.pickle)  
**Đầu Ra:** Video có chú thích tên người và confidence

---

## Luồng Dữ Liệu Chi Tiết

```
[Controller] FaceRecognitionController.recognize_faces()
    ↓
[Model] DataManager.load_model_and_labels()
    ↓
Tải hai file:
  ├─ trainer/trainer.yml → Load vào FaceRecognizer
  └─ trainer/labels.pickle → label_map: {"john_doe": 0, "jane_smith": 1}
    ↓
Tạo reverse mapping:
  reverse_map = {0: "john_doe", 1: "jane_smith"}
    ↓
[Model] FaceRecognizer.load_model(trainer.yml)
    ↓
Model state: Trained = True
    ↓
[Model] CameraService.open() → Luồng Camera (H×W×3 BGR)
    ↓
VÒNG LẶP THỜI GIAN THỰC:
  ├─ Đọc frame: ret, frame = camera.read()
  ├─ Kiểm tra: if not ret → continue
  ├─ [Xử lý] cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  ├─ Kết quả: gray (H×W uint8)
    │
  ├─ [Model] FaceDetector.detect_faces(gray)
  ├─ Kết quả: faces = [(x,y,w,h), ...]
  │
  ├─ Với mỗi face_rect trong faces:
  │   ├─ [Model] FaceDetector.extract_face_roi(gray, face_rect)
  │   ├─ Xử lý: roi = gray[y:y+h, x:x+w]
  │   ├─ Resize: cv2.resize(roi, (200, 200))
  │   └─ Kết quả: roi (200×200 uint8)
  │
  │   ├─ [Model] FaceRecognizer.predict(roi)
  │   ├─ Kết quả: (predicted_id: int, confidence: float)
  │   │
  │   ├─ [Model] FaceRecognizer.is_confident(confidence, threshold=80)
  │   ├─ Quyết định:
  │   │   ├─ Nếu confidence < 80:
  │   │   │   ├─ name = reverse_map[predicted_id]
  │   │   │   └─ color = GREEN (0, 255, 0)
  │   │   └─ Nếu confidence ≥ 80:
  │   │       ├─ name = "Unknown"
  │   │       └─ color = RED (0, 0, 255)
  │
  │   ├─ [View] VideoView.draw_face_rectangle(frame, face_rect, color)
  │   ├─ [View] VideoView.draw_text(frame, name, (x, y-10), color)
  │   └─ [View] VideoView.draw_confidence(frame, f"{confidence:.1f}", (x, y+h+20))
  │
  ├─ [View] VideoView.show_frame("Face Recognition", frame)
  ├─ [Kiểm tra] VideoView.wait_key() == ord('q')
  └─ Nếu 'q' → Break loop, ngược lại → Continue
    ↓
[Model] CameraService.release()
    ↓
cv2.destroyAllWindows()
```

---

## Thành Phần MVC Trong Giai Đoạn Này

### **Controller:**
- `FaceRecognitionController.recognize_faces()`
- Điều phối toàn bộ luồng inference

### **Models:**
- `DataManager` - Tải model và labels
- `CameraService` - Quản lý camera
- `FaceDetector` - Phát hiện khuôn mặt
- `FaceRecognizer` - Dự đoán identity

### **Views:**
- `VideoView` - Hiển thị video và vẽ chú thích

---

## Quy Trình Decision Making

### **Confidence Thresholding:**
```
confidence < 80  → Known person (GREEN)
confidence ≥ 80  → Unknown person (RED)

Ngưỡng mặc định: 80 (Config.CONFIDENCE_THRESHOLD)
Có thể điều chỉnh: 60-100 (tùy mức độ nghiêm ngặt)
```

### **Reverse Mapping:**
```
predicted_id: 0 → name: "john_doe"
predicted_id: 1 → name: "jane_smith"
predicted_id: other → name: "Unknown"
```

---

## Định Dạng Dữ Liệu

| Giai Đoạn | Dữ Liệu | Shape/Format | Type | Range |
|-----------|----------|--------------|------|-------|
| Camera frame | frame | (H, W, 3) | uint8 | [0, 255] |
| Grayscale | gray | (H, W) | uint8 | [0, 255] |
| Face detection | faces | [(x,y,w,h), ...] | int | N/A |
| ROI extraction | roi | (200, 200) | uint8 | [0, 255] |
| Prediction | (id, conf) | (int, float) | - | id≥0, conf≥0 |
| Decision | name | string | text | Person names |
| Color | color | (R, G, B) | uint8 | [0, 255] |

---

## Các Phép Biến Đổi Dữ Liệu

1. **Model Loading:** YAML/Pickle → Internal state
2. **Frame Capture:** Camera → NumPy array
3. **Color Conversion:** BGR → Grayscale
4. **Face Detection:** Haar Cascade → Bounding boxes
5. **ROI Extraction:** Crop + Resize
6. **LBPH Prediction:** ROI → (ID, Confidence)
7. **Thresholding:** Confidence → Decision
8. **Reverse Mapping:** ID → Name
9. **Visualization:** Add annotations to frame

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
- Hiển thị shapes và formats dữ liệu
- Bao gồm ngưỡng confidence (80)
- Đánh dấu quyết định (Known vs Unknown)
- Hiển thị màu sắc (GREEN vs RED)

### **Bố Cục:**
- Sắp xếp theo thứ tự thời gian
- Nhấn mạnh **VÒNG LẶP THỜI GIAN THỰC**
- Hiển thị rõ điểm bắt đầu và kết thúc
- Vẽ rõ các decision points

### **Các Yếu Tố Cần Nhấn Mạnh:**
- **Real-time Loop:** Vòng lặp xử lý frame liên tục
- **Multiple Faces:** Xử lý nhiều khuôn mặt cùng lúc
- **Decision Logic:** Confidence thresholding
- **Visual Feedback:** Hộp màu và tên người
- **Exit Condition:** Thoát khi nhấn 'q'

---

## Ví Dụ Cụ Thể

**Frame với 2 khuôn mặt:**
```
Face 1: (x=100, y=50, w=150, h=200)
  ├─ ROI: (200×200 uint8)
  ├─ Prediction: (id=0, conf=45.2)
  ├─ Decision: 45.2 < 80 → Known
  ├─ Name: "john_doe"
  └─ Color: GREEN

Face 2: (x=300, y=80, w=120, h=180)
  ├─ ROI: (200×200 uint8)
  ├─ Prediction: (id=2, conf=125.8)
  ├─ Decision: 125.8 ≥ 80 → Unknown
  ├─ Name: "Unknown"
  └─ Color: RED
```

---

## Performance Characteristics

| Metric | Giá Trị | Ghi Chú |
|--------|---------|---------|
| Latency | <50ms/face | Thông thường trên CPU hiện đại |
| Throughput | 20+ FPS | Real-time processing |
| Accuracy | 80-85% | Khuôn mặt chính diện, ánh sáng tốt |
| Memory | ~180MB | Model + frame buffer |

---

## Ghi Chú Cho Gemini AI

- Đây là **Giai Đoạn 3** trong 4 giai đoạn của hệ thống
- Tập trung vào **nhận diện thời gian thực**
- Nhấn mạnh **vòng lặp real-time** và **decision logic**
- Hiển thị rõ **visual feedback** với màu sắc
- Đây là giai đoạn **output** chính cho người dùng

---

**Định Dạng Đầu Ra:** PNG hoặc SVG với độ phân giải cao  
**Mức Độ Chi Tiết:** Chi tiết, hiển thị vòng lặp và quyết định
