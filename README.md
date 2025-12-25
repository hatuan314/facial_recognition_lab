# Hướng Dẫn Sử Dụng - Facial Recognition Lab

## 📋 Mục Lục
- [Giới Thiệu](#giới-thiệu)
- [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
- [Cài Đặt](#cài-đặt)
- [Hướng Dẫn Sử Dụng](#hướng-dẫn-sử-dụng)
- [Xử Lý Lỗi Thường Gặp](#xử-lý-lỗi-thường-gặp)

---

## 🎯 Giới Thiệu

**Facial Recognition Lab** là ứng dụng nhận diện khuôn mặt theo thời gian thực sử dụng OpenCV và thuật toán LBPH (Local Binary Patterns Histograms). Ứng dụng cho phép:
- Thu thập dữ liệu khuôn mặt
- Huấn luyện mô hình nhận diện
- Nhận diện khuôn mặt realtime qua webcam

---

## 💻 Yêu Cầu Hệ Thống

### Phần Cứng
- **Webcam**: Camera hoạt động tốt (tích hợp hoặc rời)
- **RAM**: Tối thiểu 4GB
- **CPU**: Bất kỳ (Intel/AMD đời mới)

### Phần Mềm
- **Python**: Phiên bản 3.7 trở lên
- **Hệ điều hành**: Windows, macOS, hoặc Linux
- **Thư viện**: opencv-python, opencv-contrib-python, numpy

---

## 🔧 Cài Đặt

### Bước 1: Clone hoặc Download Project

```bash
# Clone từ git (nếu có)
git clone <repository-url>
cd facial_recognition_lab

# Hoặc giải nén file zip vào thư mục
```

### Bước 2: Cài Đặt Dependencies

```bash
# Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# Hoặc cài đặt thủ công
pip install opencv-python opencv-contrib-python numpy
```

### Bước 3: Kiểm Tra Cấu Trúc Thư Mục

Đảm bảo project có cấu trúc sau:

```
facial_recognition_lab/
├── main.py                 # File chính
├── requirements.txt        # Danh sách dependencies
├── haarcascades/          # Chứa file cascade
│   └── haarcascade_frontalface_default.xml
├── dataset/               # Tự động tạo - chứa ảnh training
└── trainer/               # Tự động tạo - chứa model đã train
```

**Lưu ý**: Thư mục `dataset/` và `trainer/` sẽ được tạo tự động khi chạy chương trình.

---

## 📖 Hướng Dẫn Sử Dụng

### Khởi Chạy Chương Trình

```bash
python main.py
```

Sau khi chạy, bạn sẽ thấy menu với các tùy chọn:

```
1. Thu ảnh training
2. Train model
3. Nhận diện realtime
0. Thoát
```

---

### 🎥 Bước 1: Thu Thập Dữ Liệu Khuôn Mặt

**Mục đích**: Thu thập ảnh khuôn mặt để huấn luyện mô hình.

#### Các Bước Thực Hiện:

1. **Chọn tùy chọn `1` từ menu**
   
2. **Nhập tên người** (không dấu, ví dụ: `nguyen_van_a`, `john_doe`)
   ```
   Tên người (không dấu): nguyen_van_a
   ```

3. **Thu thập ảnh**:
   - Cửa sổ camera sẽ mở ra
   - Đặt khuôn mặt vào khung hình
   - Hệ thống tự động chụp khi phát hiện khuôn mặt (khung màu xanh lá)
   - Mặc định thu thập **30 ảnh**
   - Để thu được ảnh tốt:
     - Đứng ở vị trí có ánh sáng tốt
     - Xoay đầu nhẹ sang các góc khác nhau
     - Thay đổi biểu cảm (mỉm cười, nghiêm túc, v.v.)

4. **Kết thúc**: 
   - Tự động dừng sau 30 ảnh
   - Hoặc nhấn phím `q` để dừng sớm

5. **Lặp lại** cho mỗi người cần nhận diện

**Kết quả**: Ảnh được lưu tại `dataset/<tên_người>/`

---

### 🤖 Bước 2: Huấn Luyện Mô Hình

**Mục đích**: Tạo mô hình nhận diện từ dữ liệu đã thu thập.

#### Các Bước Thực Hiện:

1. **Đảm bảo đã thu thập ảnh** cho ít nhất 1 người

2. **Chọn tùy chọn `2` từ menu**

3. **Quá trình training**:
   - Hệ thống tự động quét thư mục `dataset/`
   - Đọc tất cả ảnh (.jpg, .png, .jpeg)
   - Huấn luyện mô hình LBPH
   - Lưu mô hình vào `trainer/trainer.yml`
   - Lưu mapping labels vào `trainer/labels.pickle`

4. **Hoàn tất**: Thông báo training thành công

**Thời gian**: Phụ thuộc số lượng ảnh (thường < 10 giây)

---

### 👤 Bước 3: Nhận Diện Khuôn Mặt Realtime

**Mục đích**: Sử dụng mô hình để nhận diện khuôn mặt qua webcam.

#### Các Bước Thực Hiện:

1. **Đảm bảo đã train mô hình** (Bước 2)

2. **Chọn tùy chọn `3` từ menu**

3. **Nhận diện**:
   - Cửa sổ camera mở ra
   - Hệ thống tự động nhận diện khuôn mặt trong frame
   - **Khung màu xanh lá** + tên người: Nhận diện thành công
   - **Khung màu đỏ** + "Unknown": Không nhận diện được
   
4. **Hiểu kết quả**:
   - Độ tin cậy < 80: Nhận diện chính xác
   - Độ tin cậy ≥ 80: Không chắc chắn → hiển thị "Unknown"

5. **Kết thúc**: Nhấn phím `q` để thoát

---

### 🚪 Thoát Chương Trình

Chọn `0` hoặc nhấn bất kỳ phím nào khác từ menu.

---

## ⚠️ Xử Lý Lỗi Thường Gặp

### 1. **Lỗi: "Không mở được camera"**

**Nguyên nhân**:
- Camera đang được sử dụng bởi ứng dụng khác
- Không có quyền truy cập camera
- Camera bị lỗi

**Giải pháp**:
```bash
# Đóng các ứng dụng đang dùng camera (Zoom, Skype, etc.)
# Kiểm tra quyền truy cập camera trong System Preferences (macOS)
# hoặc Settings → Privacy → Camera (Windows)

# Thử camera khác (nếu có nhiều camera)
# Sửa trong main.py dòng 21:
cam = cv2.VideoCapture(1)  # Thay 0 bằng 1, 2, ...
```

---

### 2. **Lỗi: "Không tìm thấy file cascade"**

**Nguyên nhân**: Thiếu file `haarcascade_frontalface_default.xml`

**Giải pháp**:
```bash
# Download file cascade từ OpenCV GitHub
# Đặt vào thư mục: haarcascades/haarcascade_frontalface_default.xml
```

Hoặc download từ: https://github.com/opencv/opencv/tree/master/data/haarcascades

---

### 3. **Lỗi: "No module named 'cv2'"**

**Nguyên nhân**: Chưa cài đặt OpenCV

**Giải pháp**:
```bash
pip install opencv-python opencv-contrib-python
```

---

### 4. **Nhận diện sai hoặc hiển thị "Unknown" liên tục**

**Nguyên nhân**:
- Dữ liệu training không đủ
- Ánh sáng khác biệt giữa training và testing
- Góc chụp khác nhau

**Giải pháp**:
- Thu thập thêm ảnh (50-100 ảnh)
- Đảm bảo điều kiện ánh sáng tương tự
- Thu thập ảnh ở nhiều góc độ khác nhau
- Train lại model sau khi thêm ảnh

---

### 5. **Lỗi khi train: "need at least one array to concatenate"**

**Nguyên nhân**: Thư mục `dataset/` trống hoặc không có ảnh hợp lệ

**Giải pháp**:
- Chạy Bước 1 để thu thập ảnh trước
- Kiểm tra thư mục `dataset/` có chứa ảnh

---

## 💡 Tips Sử Dụng Hiệu Quả

### Để đạt độ chính xác cao:

1. **Thu thập dữ liệu tốt**:
   - Ít nhất 30-50 ảnh mỗi người
   - Đa dạng góc độ (trái, phải, nghiêng đầu)
   - Đa dạng biểu cảm
   - Ánh sáng tốt, không quá tối hoặc quá sáng

2. **Môi trường training = testing**:
   - Cùng điều kiện ánh sáng
   - Cùng vị trí camera
   - Cùng khoảng cách từ camera

3. **Cập nhật model thường xuyên**:
   - Thêm ảnh mới và train lại khi nhận diện sai
   - Xóa ảnh chất lượng kém trong thư mục dataset

4. **Tối ưu hiệu suất**:
   - Giữ số người nhận diện ở mức vừa phải (< 20 người)
   - Nếu có nhiều người, cân nhắc train riêng từng nhóm

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề không có trong tài liệu này:
1. Kiểm tra file `CHI_TIET_TINH_NANG.md` để hiểu rõ cách hoạt động
2. Xem log lỗi trong terminal
3. Kiểm tra phiên bản Python và thư viện

---

## 📝 Ghi Chú

- **Quyền riêng tư**: Dữ liệu khuôn mặt được lưu local, không upload lên server
- **Backup**: Nên backup thư mục `dataset/` và `trainer/` định kỳ
- **Cập nhật**: Chạy lại training sau khi thêm người mới

---

**Chúc bạn sử dụng thành công! 🎉**
