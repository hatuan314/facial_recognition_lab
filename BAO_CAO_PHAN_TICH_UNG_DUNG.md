# Báo cáo Phân tích Ứng dụng Nhận diện Khuôn mặt

## Tổng quan

Ứng dụng nhận diện khuôn mặt thời gian thực sử dụng Python và OpenCV là một hệ thống giáo dục được thiết kế để minh họa các kỹ thuật thị giác máy tính cổ điển. Ứng dụng sử dụng thuật toán LBPH (Local Binary Patterns Histograms) kết hợp với Haar Cascade để nhận diện khuôn mặt qua webcam.

---

## Kiến trúc hệ thống

### 1. Mô hình MVC (Model-View-Controller)

Ứng dụng được xây dựng theo mô hình MVC, đảm bảo sự tách biệt giữa các thành phần:

#### **Models (src/models/)**
- **CameraService**: Quản lý các hoạt động liên quan đến camera
- **FaceDetector**: Phát hiện khuôn mặt sử dụng Haar Cascade
- **FaceRecognizer**: Nhận diện khuôn mặt sử dụng thuật toán LBPH
- **DataManager**: Quản lý việc lưu và tải dữ liệu (tập dữ liệu, mô hình)
- **ModelEvaluator**: Đánh giá hiệu suất mô hình với các chỉ số đo lường

#### **Views (src/views/)**
- **ConsoleView**: Giao diện dòng lệnh tương tác với người dùng
- **VideoView**: Hiển thị video và vẽ các chú thích (khung chữ nhật, văn bản)

#### **Controllers (src/controllers/)**
- **FaceRecognitionController**: Điều phối luồng công việc chính của ứng dụng

### 2. Nguyên tắc SOLID

Kiến trúc tuân thủ các nguyên tắc SOLID:

- **Trách nhiệm duy nhất (Single Responsibility)**: Mỗi lớp chỉ có một trách nhiệm duy nhất
- **Mở/Đóng (Open/Closed)**: Mở rộng cho phép thêm tính năng, đóng để sửa đổi
- **Thế Liskov (Liskov Substitution)**: Các lớp con có thể thay thế lớp cha
- **Phân tách Interface (Interface Segregation)**: Các giao diện nhỏ và tập trung
- **Đảo ngược Dependency (Dependency Inversion)**: Phụ thuộc vào trừu tượng, không phải cụ thể

### 3. Cấu trúc thư mục

```
facial_recognition_lab/
├── main.py                    # Entry point
├── config.py                  # Cấu hình tập trung
├── requirements.txt           # Dependencies
│
├── src/                       # Source code (MVC)
│   ├── controllers/           # Logic điều phối
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
├── dataset/                   # Dữ liệu huấn luyện
├── trainer/                   # Mô hình đã huấn luyện
├── haarcascades/              # Các mô hình cascade được huấn luyện sẵn
└── docs/                      # Tài liệu
```

### 4. Hệ thống cấu hình

- **Tệp**: `config.py`
- **Mẫu**: Lớp với các biến tĩnh
- **Đặc điểm**: Không sử dụng tệp cấu hình bên ngoài (YAML, JSON)
- **Truy cập**: `Config.PARAMETER_NAME`

**Các cấu hình chính:**
- `DATASET_DIR`: Thư mục lưu tập dữ liệu
- `TRAINER_DIR`: Thư mục lưu mô hình
- `FACE_SIZE`: Kích thước ảnh chuẩn (200, 200)
- `CONFIDENCE_THRESHOLD`: Ngưỡng độ tin cậy (80)
- `DETECTION_SCALE_FACTOR`: Hệ số tỷ lệ cho Haar Cascade (1.3)
- `DETECTION_MIN_NEIGHBORS`: Số lượng láng giềng tối thiểu cho Haar Cascade (5)

---

## Các chức năng chính

### 1. Thu thập dữ liệu (Data Collection)

**Mục đích**: Thu thập ảnh khuôn mặt cho huấn luyện

**Luồng hoạt động**:
1. Khởi tạo camera
2. Chụp khung hình liên tục từ webcam
3. Chuyển đổi sang thang độ xám
4. Phát hiện khuôn mặt bằng Haar Cascade
5. Cắt vùng quan tâm (ROI - Region of Interest)
6. Thay đổi kích thước về chuẩn (200×200)
7. Lưu vào `dataset/<person_name>/<person_name>_<index>.jpg`
8. Hiển thị tiến trình và phản hồi trực quan

**Hợp đồng**:
- Đầu vào: Tên người, số lượng ảnh (mặc định 30)
- Đầu ra:  ảnh thang độ xám 200×200 pixels
- Định dạng: JPEG, uint8, khoảng [0, 255]

### 2. Huấn luyện Mô hình (Training Model)

**Mục đích**: Huấn luyện mô hình LBPH từ tập dữ liệu

**Luồng hoạt động**:
1. Tải tất cả ảnh từ `dataset/`
2. Tạo ánh xạ nhãn (tên → ID)
3. Thay đổi kích thước tất cả ảnh về 200×200
4. Huấn luyện mô hình LBPH
5. Lưu mô hình vào `trainer/trainer.yml`
6. Lưu ánh xạ nhãn vào `trainer/labels.pickle`

**Hợp đồng**:
- Đầu vào: Danh sách[np.ndarray] faces, Danh sách[int] labels
- Đầu ra: Tệp mô hình (.yml) và ánh xạ nhãn (.pickle)
- Thuật toán: LBPH (Local Binary Patterns Histograms)

### 3. Nhận diện Thời gian thực (Real-time Recognition)

**Mục đích**: Nhận diện khuôn mặt trong luồng video

**Luồng hoạt động**:
1. Tải mô hình đã huấn luyện
2. Mở camera
3. Đọc khung hình liên tục
4. Chuyển đổi sang thang độ xám
5. Phát hiện khuôn mặt
6. Cắt vùng quan tâm cho mỗi khuôn mặt
7. Dự đoán bằng mô hình LBPH
8. Áp dụng ngưỡng độ tin cậy
9. Ánh xạ ID → tên người
10. Hiển thị kết quả với màu sắc:
    - Xanh lá: Nhận diện đúng
    - Đỏ: Không xác định hoặc độ tin cậy thấp

**Hợp đồng**:
- Đầu vào: Khung hình từ camera
- Đầu ra: (predicted_id: int, confidence: float)
- Ngưỡng: confidence < 80 → được nhận diện, ≥ 80 → không xác định

### 4. Đánh giá Mô hình (Model Evaluation)

**Mục đích**: Đo lường hiệu suất mô hình với các chỉ số

**Luồng hoạt động**:
1. Tải tập dữ liệu
2. Chia tập huấn luyện/kiểm tra (80/20, phân tầng)
3. Huấn luyện mô hình trên tập huấn luyện
4. Dự đoán trên tập kiểm tra
5. Tính toán các chỉ số:
   - Accuracy, Precision, Recall, F1-Score
   - Ma trận nhầm lẫn (Confusion Matrix)
   - Độ chính xác theo từng người
   - Thống kê độ tin cậy
6. Hiển thị báo cáo chi tiết

**Tính năng**:
- Hỗ trợ cả scikit-learn và triển khai thủ công
- Cross-validation (k-fold)
- Phân mẫu phân tầng
- Phân tích phân phối độ tin cậy

---

## Công nghệ sử dụng

### Công nghệ cốt lõi
- **Python 3.7+**: Ngôn ngữ lập trình chính
- **OpenCV (opencv-contrib-python)**: Thư viện thị giác máy tính
- **NumPy**: Các thao tác mảng
- **Pickle**: Tuần tự hóa cho ánh xạ nhãn
- **scikit-learn≥1.0.0**: Các chỉ số đánh giá (tùy chọn)

### Thuật toán
- **Haar Cascade**: Phát hiện khuôn mặt
- **LBPH (Local Binary Patterns Histograms)**: Nhận diện khuôn mặt
- **Phân mẫu phân tầng (Stratified Sampling)**: Chia dữ liệu
- **Khoảng cách Chi-Square**: Đo lường tương đồng LBPH

### Mẫu thiết kế
- **MVC**: Mẫu kiến trúc
- **SOLID**: Nguyên tắc thiết kế
- **Context Manager**: Quản lý tài nguyên (camera)
- **Dependency Injection**: Liên kết lỏng lẻo

---

## Điểm mạnh và Hạn chế

### Điểm mạnh
1. **Kiến trúc rõ ràng**: MVC + các nguyên tắc SOLID
2. **Chất lượng mã**: Code sạch, xử lý lỗi phù hợp
3. **Tài liệu**: Đầy đủ, có hợp đồng rõ ràng
4. **Modular**: Dễ mở rộng và bảo trì
5. **Giáo dục**: Phù hợp cho học tập và nghiên cứu
6. **Không yêu cầu GPU**: Chạy trên CPU

### Hạn chế
1. **Thị giác máy tính cổ điển**: Không sử dụng học sâu
2. **Camera đơn**: Chỉ hỗ trợ một camera
3. **Không có giao diện web**: Chỉ có giao diện dòng lệnh
4. **Khả năng mở rộng hạn chế**: Không thiết kế cho sản xuất
5. **Nhạy cảm với ánh sáng**: Haar Cascade nhạy cảm với điều kiện ánh sáng
6. **Hạn chế về tư thế**: LBPH hoạt động tốt nhất với khuôn mặt chính diện

---

## Các trường hợp sử dụng và Ứng dụng

### Giáo dục
- **Các khóa học Thị giác máy tính**: Minh họa các kỹ thuật CV cổ điển
- **Demo Học máy**: Hiển thị pipeline hoàn chỉnh
- **Nghiên cứu kiến trúc mã**: Ví dụ về MVC và SOLID

### Tạo mẫu nhanh (Prototyping)
- **PoC Nhận diện khuôn mặt**: Khái niệm chứng minh nhanh
- **So sánh thuật toán**: Thử nghiệm các thuật toán khác nhau
- **Thu thập dữ liệu**: Tập dữ liệu cho học sâu

### Nghiên cứu
- **Nghiên cứu LBPH**: Nghiên cứu và cải tiến thuật toán
- **Các chỉ số đánh giá**: Benchmark các phương pháp
- **Hệ thống thời gian thực**: Phát triển hệ thống thời gian thực

---

## Kết luận

Ứng dụng nhận diện khuôn mặt này là một hệ thống được thiết kế tốt, thể hiện các phương pháp tốt nhất trong phát triển phần mềm và thị giác máy tính. Với kiến trúc MVC rõ ràng, tuân thủ các nguyên tắc SOLID, và tài liệu đầy đủ, ứng dụng đóng vai trò như một công cụ giáo dục xuất sắc và nền tảng cho các phát triển nâng cao.

Mặc dù có những hạn chế về các phương pháp thị giác máy tính cổ điển, kiến trúc và chất lượng mã của ứng dụng cung cấp một nền tảng vững chắc cho việc:
- Học các khái niệm thị giác máy tính
- Hiểu về kiến trúc phần mềm
- Tạo mẫu nhanh các hệ thống nhận diện khuôn mặt
- Xây dựng các giải pháp nâng cao hơn

Ứng dụng đạt thành công các mục tiêu giáo dục của mình trong khi duy trì chất lượng mã, tiêu chuẩn tài liệu, và khả năng mở rộng cho các cải tiến trong tương lai.
