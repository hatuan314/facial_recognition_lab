# Prompt cho Gemini AI: Giai Đoạn 2 - Huấn Luyện Model

## Mục Tiêu
Tạo một **Data Flow Diagram (DFD)** chi tiết cho **Giai Đoạn 2: Huấn Luyện Model** của ứng dụng Nhận Diện Khuôn Mặt. Sơ đồ cần minh họa luồng dữ liệu hoàn chỉnh từ việc tải dữ liệu huấn luyện đến việc lưu model đã train.

---

## Thông Tin Giai Đoạn

**Tên Giai Đoạn:** HUẤN LUYỆN MODEL (TRAINING)  
**Mục Đích:** Huấn luyện thuật toán LBPH trên dữ liệu đã thu thập  
**Đầu Vào:** Thư mục dataset/ với ảnh của nhiều người  
**Đầu Ra:** Model đã train (trainer.yml) và ánh xạ nhãn (labels.pickle)

---

## Luồng Dữ Liệu Chi Tiết

```
[Controller] FaceRecognitionController.train_model()
    ↓
[Model] DataManager.load_training_data()
    ↓
Quét thư mục dataset/:
  ├─ os.walk(dataset/)
  ├─ Lọc file .jpg, .png, .jpeg
  ├─ Trích xuất tên người từ thư mục
  └─ Tạo label_map: {"john_doe": 0, "jane_smith": 1, "bob_jones": 2}
    ↓
Tạo danh sách ảnh huấn luyện:
  ├─ faces: List[np.ndarray] - Mỗi ảnh (200×200 uint8)
  ├─ labels: List[int] - Nhãn tương ứng [0,0,0,...,1,1,1,...]
  └─ label_map: Dict[str, int] - Ánh xạ tên → ID
    ↓
[Model] FaceRecognizer.train(faces, labels)
    ↓
Thuật toán LBPH:
  ├─ Tính toán Local Binary Patterns cho mỗi ảnh
  ├─ Chia ảnh thành lưới 8×8 (64 ô)
  ├─ Tạo histogram (256 bins) cho mỗi ô
  ├─ Tổng hợp: 64 ô × 256 bins = 16,384 đặc trưng/ảnh
  ├─ Lưu trữ histogram cho mỗi nhãn
  └─ Internal state: Trained model
    ↓
[Model] DataManager.save_model(trained_model, label_map)
    ↓
Lưu hai file:
  ├─ trainer/trainer.yml (LBPH model, YAML format, ~4-5MB)
  └─ trainer/labels.pickle (Ánh xạ nhãn, Binary, <1KB)
    ↓
[View] ConsoleView.show_success("Huấn luyện hoàn thành!")
    ↓
[View] ConsoleView.show_info(f"Đã huấn luyện {len(label_map)} người")
```

---

## Thành Phần MVC Trong Giai Đoạn Này

### **Controller:**
- `FaceRecognitionController.train_model()`
- Điều phối toàn bộ luồng huấn luyện

### **Models:**
- `DataManager` - Tải dữ liệu và lưu model
- `FaceRecognizer` - Thực hiện thuật toán LBPH

### **Views:**
- `ConsoleView` - Hiển thị thông báo và kết quả

---

## Thuật Toán LBPH Chi Tiết

### **Local Binary Patterns (LBP):**
```
Với mỗi pixel trung tâm:
  ├─ So sánh với 8 pixels xung quanh
  ├─ Nếu pixel xung quanh ≥ pixel trung tâm → 1, ngược lại → 0
  ├─ Tạo số nhị phân 8-bit
  └─ Chuyển thành decimal (0-255)
```

### **Histogram Creation:**
```
Chia ảnh (200×200) thành lưới 8×8:
  ├─ 64 ô, mỗi ô 25×25 pixels
  ├─ Tính LBP cho mỗi pixel trong ô
  ├─ Tạo histogram 256 bins cho mỗi ô
  └─ Ghép 64 histograms → feature vector (16,384 chiều)
```

---

## Định Dạng Dữ Liệu

| Giai Đoạn | Dữ Liệu | Shape/Format | Type | Kích Thước |
|-----------|----------|--------------|------|------------|
| Input images | faces | List[(200,200)] | uint8 | N×200×200 |
| Labels | labels | (N,) | int32 | N |
| Label mapping | label_map | {"name": id} | dict | M entries |
| LBPH features | histograms | (64, 256) | float | 64×256 per image |
| Model file | trainer.yml | YAML | text | ~4-5MB |
| Labels file | labels.pickle | Binary | binary | <1KB |

---

## Cấu Trúc File Đầu Ra

```
trainer/
├── trainer.yml
│   ├── LBPH parameters (radius: 1, neighbors: 8, grid_x: 8, grid_y: 8)
│   ├── Histogram data cho mỗi label
│   └── Model metadata
└── labels.pickle
    ├── {"john_doe": 0, "jane_smith": 1, "bob_jones": 2}
    └── Reverse mapping capability
```

---

## Các Phép Biến Đổi Dữ Liệu

1. **File Loading:** JPEG files → NumPy arrays
2. **Label Mapping:** Person names → Numeric IDs
3. **LBPH Training:** Images → Histogram features
4. **Model Serialization:** Internal state → YAML file
5. **Label Serialization:** Dictionary → Pickle file

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
- Bao gồm các tham số LBPH (radius=1, neighbors=8, grid=8×8)
- Đánh dấu kích thước feature vectors (16,384)
- Hiển thị kích thước file đầu ra

### **Bố Cục:**
- Sắp xếp theo thứ tự xử lý (từ trái sang phải hoặc trên xuống)
- Nhóm các bước liên quan đến LBPH
- Hiển thị rõ input từ dataset/
- Vẽ rõ output vào trainer/

### **Các Yếu Tố Cần Nhấn Mạnh:**
- **Data Loading:** Quét thư mục và tạo ánh xạ nhãn
- **LBPH Algorithm:** Chi tiết các bước xử lý
- **Feature Extraction:** 8×8 grid và 256 bins
- **Model Storage:** Hai file đầu ra với định dạng khác nhau
- **Success Feedback:** Thông báo hoàn thành

---

## Ví Dụ Cụ Thể

**Với 3 người (john_doe: 30 ảnh, jane_smith: 25 ảnh, bob_jones: 35 ảnh):**
```
Input:
  - Total images: 90
  - faces: List[90] × (200×200 uint8)
  - labels: [0×30, 1×25, 2×35]
  - label_map: {"john_doe": 0, "jane_smith": 1, "bob_jones": 2}

Processing:
  - 90 feature vectors × 16,384 dimensions
  - 3 histogram groups (mỗi người)

Output:
  - trainer.yml: ~4.5MB
  - labels.pickle: ~50 bytes
```

---

## Ghi Chú Cho Gemini AI

- Đây là **Giai Đoạn 2** trong 4 giai đoạn của hệ thống
- Tập trung vào **huấn luyện thuật toán LBPH**
- Nhấn mạnh **các bước xử lý bên trong LBPH**
- Hiển thị rõ **cấu trúc file model và labels**
- Đây là giai đoạn **processing** tạo ra model cho inference

---

**Định Dạng Đầu Ra:** PNG hoặc SVG với độ phân giải cao  
**Mức Độ Chi Tiết:** Chi tiết, hiển thị thuật toán LBPH
