# Prompt cho Gemini AI: Giai Đoạn 1 - Thu Thập Dữ Liệu

## Mục Tiêu
Tạo một **Data Flow Diagram (DFD)** chi tiết cho **Giai Đoạn 1: Thu Thập Dữ Liệu** của ứng dụng Nhận Diện Khuôn Mặt. Sơ đồ cần minh họa luồng dữ liệu hoàn chỉnh từ việc thu thập ảnh huấn luyện từ camera.

---

## Thông Tin Giai Đoạn

**Tên Giai Đoạn:** THU THẬP DỮ LIỆU (DATA COLLECTION)  
**Mục Đích:** Thu thập ảnh khuôn mặt cho từng người để huấn luyện model  
**Đầu Vào:** Tên người từ người dùng, số lượng ảnh cần thu thập (mặc định: 30)  
**Đầu Ra:** Ảnh khuôn mặt đã xử lý (200×200 grayscale) được lưu vào thư mục dataset/

---

## Luồng Dữ Liệu Chi Tiết

```
Nhập liệu từ người dùng (person_name, samples=30)
    ↓
[Controller] FaceRecognitionController.capture_faces(person_name, samples)
    ↓
[Model] CameraService.open() → Luồng Camera (H×W×3 BGR)
    ↓
[Xử lý] cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) → Grayscale (H×W uint8)
    ↓
[Model] FaceDetector.detect_faces(gray, scale_factor=1.3, min_neighbors=5)
    ↓
Kết quả: Hình chữ nhật khuôn mặt [(x,y,w,h), ...]
    ↓
Với mỗi khuôn mặt phát hiện được:
  ├─ [Model] FaceDetector.extract_face_roi(gray, face_rect)
  ├─ Xử lý: roi = gray[y:y+h, x:x+w]
  ├─ Resize: cv2.resize(roi, (200, 200))
  └─ Kết quả: ROI (200×200 uint8)
    ↓
[Model] DataManager.save_face_image(person_name, roi, count)
    ↓
Lưu vào ổ đĩa: dataset/<person_name>/<person_name>_<count>.jpg
    ↓
[View] VideoView.draw_face_rectangle(frame, face_rect, GREEN)
    ↓
[View] VideoView.draw_text(frame, f"Samples: {count}/{samples}", position)
    ↓
[View] VideoView.show_frame("Data Collection", frame)
    ↓
Kiểm tra: count >= samples? → Nếu đủ: Thoát, nếu chưa: Tiếp tục
    ↓
Thoát khi nhấn phím 'q' hoặc đủ số lượng ảnh
```

---

## Thành Phần MVC Trong Giai Đoạn Này

### **Controller:**
- `FaceRecognitionController.capture_faces(person_name, samples=30)`
- Điều phối toàn bộ luồng thu thập dữ liệu

### **Models:**
- `CameraService` - Quản lý camera (open, read, release)
- `FaceDetector` - Phát hiện và trích xuất ROI khuôn mặt
- `DataManager` - Lưu ảnh vào thư mục dataset/

### **Views:**
- `VideoView` - Hiển thị video và vẽ chú thích
- `ConsoleView` - Hiển thị thông báo và hướng dẫn

---

## Định Dạng Dữ Liệu

| Giai Đoạn | Dữ Liệu | Shape/Format | Type | Range |
|-----------|----------|--------------|------|-------|
| Camera capture | frame | (H, W, 3) | uint8 | [0, 255] |
| Grayscale | gray | (H, W) | uint8 | [0, 255] |
| Face detection | faces | [(x,y,w,h), ...] | int | N/A |
| ROI extraction | roi | (200, 200) | uint8 | [0, 255] |
| File lưu | image | (200, 200) | JPEG | [0, 255] |

---

## Các Phép Biến Đổi Dữ Liệu

1. **BGR → Grayscale:** `cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)`
2. **Face Detection:** Haar Cascade → Bounding boxes
3. **ROI Extraction:** Crop + Resize về 200×200
4. **File Storage:** ROI → JPEG file on disk

---

## Vị Trí Lưu Trữ

```
dataset/
├── john_doe/
│   ├── john_doe_0.jpg (200×200 grayscale JPEG)
│   ├── john_doe_1.jpg
│   ├── john_doe_2.jpg
│   └── ... (30 images per person)
├── jane_smith/
│   ├── jane_smith_0.jpg
│   └── ... (30 images)
└── [other_people]/
    └── ... (30 images each)
```

---

## Yêu Cầu Sơ Đồ

### **Phong Cách Trực Quan:**
- Sử dụng ký hiệu **flowchart** hoặc **data flow diagram**
- Phân biệt rõ các thành phần MVC bằng màu sắc:
  - Controller: Cam (Orange)
  - Models: Xanh dương (Blue)
  - Views: Xanh lá (Green)
  - Data stores: Xám (Gray)

### **Nhãn và Ghi Chú:**
- Hiển thị shapes/formats dữ liệu trên mũi tên
- Bao gồm tên hàm và tham số
- Đánh dấu các quyết định quan trọng
- Hiển thị vòng lặp (count < samples)

### **Bố Cục:**
- Sắp xếp theo thứ tự thời gian (từ trên xuống dưới)
- Nhóm các thành phần liên quan
- Hiển thị rõ điểm bắt đầu và kết thúc
- Vẽ rõ vòng lặp kiểm tra số lượng ảnh

### **Các Yếu Tố Cần Nhấn Mạnh:**
- **Input:** Người dùng nhập tên và số lượng ảnh
- **Processing:** Vòng lặp thu thập ảnh
- **Decision:** Kiểm tra đủ số lượng ảnh
- **Storage:** Lưu ảnh vào thư mục có cấu trúc
- **Feedback:** Hiển thị tiến trình trực quan

---

## Kịch Bản Sử Dụng

**Người dùng muốn thu thập 30 ảnh cho "john_doe":**
1. Nhập "john_doe" vào console
2. Camera mở, hiển thị video real-time
3. Hệ thống phát hiện khuôn mặt, vẽ hộp màu xanh
4. Mỗi lần phát hiện, trích xuất ROI 200×200
5. Lưu ảnh vào dataset/john_doe/john_doe_0.jpg
6. Tăng counter, hiển thị "Samples: 1/30"
7. Lặp lại cho đến khi đủ 30 ảnh
8. Hiển thị thông báo hoàn thành

---

## Ghi Chú Cho Gemini AI

- Đây là **Giai Đoạn 1** trong 4 giai đoạn của hệ thống
- Tập trung vào **thu thập và lưu trữ dữ liệu huấn luyện**
- Nhấn mạnh **vòng lặp thu thập** và **phản hồi trực quan**
- Hiển thị rõ **cấu trúc thư mục dataset**
- Đây là giai đoạn **input** cho toàn bộ hệ thống

---

**Định Dạng Đầu Ra:** PNG hoặc SVG với độ phân giải cao  
**Mức Độ Chi Tiết:** Chi tiết, hiển thị từng bước xử lý
