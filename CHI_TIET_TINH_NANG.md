# Chi Tiết Tính Năng - Facial Recognition Lab

## 📋 Mục Lục
- [Tổng Quan Kiến Trúc](#tổng-quan-kiến-trúc)
- [Cấu Hình và Biến Toàn Cục](#cấu-hình-và-biến-toàn-cục)
- [Chi Tiết Các Hàm](#chi-tiết-các-hàm)
- [Thuật Toán LBPH](#thuật-toán-lbph)
- [Luồng Xử Lý Dữ Liệu](#luồng-xử-lý-dữ-liệu)
- [Kỹ Thuật Tối Ưu](#kỹ-thuật-tối-ưu)

---

## 🏗️ Tổng Quan Kiến Trúc

### Sơ Đồ Luồng Chương Trình

```
main.py
│
├── Khởi tạo
│   ├── Import thư viện (cv2, os, numpy, pickle)
│   ├── Thiết lập đường dẫn động (PROJECT_PATH)
│   └── Tạo thư mục cần thiết (dataset, trainer)
│
├── Menu Chính (menu())
│   ├── Tùy chọn 1 → capture_faces()
│   ├── Tùy chọn 2 → train_model()
│   └── Tùy chọn 3 → recognize()
│
└── Hàm hỗ trợ
    ├── load_cascade()
    └── get_camera()
```

### Công Nghệ Sử Dụng

| Thư Viện | Mục Đích | Vai Trò |
|----------|----------|---------|
| **OpenCV (cv2)** | Xử lý ảnh & video | Core của ứng dụng |
| **NumPy** | Tính toán ma trận | Xử lý dữ liệu ảnh |
| **Pickle** | Serialization | Lưu/đọc label mapping |
| **os** | File system | Quản lý thư mục, đường dẫn |

---

## 🔧 Cấu Hình và Biến Toàn Cục

### 1. PROJECT_PATH (Dòng 6)

```python
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
```

**Mục đích**: Xác định thư mục gốc của project một cách động.

**Cách hoạt động**:
- `__file__`: Biến đặc biệt chứa đường dẫn file hiện tại (`main.py`)
- `os.path.abspath(__file__)`: Chuyển thành đường dẫn tuyệt đối
- `os.path.dirname()`: Lấy thư mục cha

**Ví dụ**:
```
File: /Users/user/project/main.py
→ PROJECT_PATH = /Users/user/project
```

**Ưu điểm**:
- ✅ Cross-platform (Windows, macOS, Linux)
- ✅ Không cần sửa code khi chuyển máy
- ✅ Hoạt động với đường dẫn có khoảng trắng hoặc ký tự đặc biệt

**Trước đây** (hardcoded):
```python
PROJECT_PATH = r"D:\caohoc\facerecog"  # ❌ Chỉ chạy trên máy cụ thể
```

---

### 2. DATASET_DIR (Dòng 8)

```python
DATASET_DIR = os.path.join(PROJECT_PATH, "dataset")
```

**Mục đích**: Thư mục chứa ảnh training.

**Cấu trúc thư mục**:
```
dataset/
├── nguyen_van_a/
│   ├── nguyen_van_a_0.jpg
│   ├── nguyen_van_a_1.jpg
│   └── ...
├── tran_thi_b/
│   ├── tran_thi_b_0.jpg
│   └── ...
└── ...
```

**Chi tiết**:
- Mỗi người = 1 thư mục con
- Tên thư mục = tên người (không dấu)
- Ảnh định dạng: `.jpg`, `.png`, `.jpeg`
- Kích thước: 200x200 pixels (grayscale)

---

### 3. TRAINER_DIR (Dòng 9)

```python
TRAINER_DIR = os.path.join(PROJECT_PATH, "trainer")
```

**Mục đích**: Lưu model đã train và label mapping.

**Nội dung**:
```
trainer/
├── trainer.yml        # Model LBPH đã train
└── labels.pickle      # Mapping tên → ID số
```

**trainer.yml**: 
- Format: YAML (OpenCV)
- Chứa: Histogram patterns, radius, neighbors, grid parameters
- Kích thước: 10KB - 1MB (tùy số người)

**labels.pickle**:
```python
{
    "nguyen_van_a": 0,
    "tran_thi_b": 1,
    "le_van_c": 2
}
```

---

### 4. CASCADE_PATH (Dòng 10)

```python
CASCADE_PATH = os.path.join(PROJECT_PATH, "haarcascades", "haarcascade_frontalface_default.xml")
```

**Mục đích**: Đường dẫn tới Haar Cascade Classifier.

**Haar Cascade là gì?**
- Thuật toán phát hiện đối tượng (object detection)
- Được train sẵn bởi OpenCV
- Dựa trên đặc trưng Haar-like features
- Fast & lightweight

**File XML chứa**:
- Cascade stages (khoảng 20-25 stages)
- Weak classifiers cho mỗi stage
- Threshold values
- Kích thước: ~900KB

**Ứng dụng**: Phát hiện vị trí khuôn mặt trong ảnh/video.

---

### 5. Tạo Thư Mục Tự Động (Dòng 12-13)

```python
os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(TRAINER_DIR, exist_ok=True)
```

**Chức năng**:
- Tạo thư mục nếu chưa tồn tại
- `exist_ok=True`: Không báo lỗi nếu đã tồn tại
- Đảm bảo structure đúng khi chạy lần đầu

---

## 🛠️ Chi Tiết Các Hàm

### 1. load_cascade() - Dòng 15-18

```python
def load_cascade():
    if not os.path.exists(CASCADE_PATH):
        raise FileNotFoundError(f"Không tìm thấy file cascade: {CASCADE_PATH}")
    return cv2.CascadeClassifier(CASCADE_PATH)
```

**Mục đích**: Load Haar Cascade classifier để phát hiện khuôn mặt.

**Luồng xử lý**:
1. Kiểm tra file XML có tồn tại không
2. Nếu không → raise Exception với thông báo rõ ràng
3. Nếu có → tạo đối tượng `CascadeClassifier`

**Return**: Đối tượng classifier có thể gọi `detectMultiScale()`

**Error Handling**: 
- Tránh crash khi thiếu file
- Thông báo lỗi rõ ràng giúp debug

---

### 2. get_camera() - Dòng 20-24

```python
def get_camera():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        raise Exception("Không mở được camera.")
    return cam
```

**Mục đích**: Khởi tạo và kiểm tra kết nối camera.

**Chi tiết**:
- `VideoCapture(0)`: Mở camera mặc định (index 0)
  - 0 = camera chính (thường là webcam laptop)
  - 1, 2, ... = camera phụ (nếu có)
- `isOpened()`: Kiểm tra camera có sẵn sàng không

**Lưu ý khi dùng**:
```python
# ✅ Đúng
cam = get_camera()
# ... sử dụng camera
cam.release()  # Luôn nhớ release!

# ❌ Sai - Leak resources
cam = get_camera()
# ... không release
```

---

### 3. capture_faces() - Dòng 26-48

```python
def capture_faces(name, samples=30):
    cascade = load_cascade()
    cap = get_camera()
    person_dir = os.path.join(DATASET_DIR, name)
    os.makedirs(person_dir, exist_ok=True)
    count = 0

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            roi = cv2.resize(gray[y:y+h, x:x+w], (200,200))
            cv2.imwrite(os.path.join(person_dir,f"{name}_{count}.jpg"), roi)
            count += 1
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        cv2.imshow("Capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or count >= samples:
            break

    cap.release()
    cv2.destroyAllWindows()
```

**Mục đích**: Thu thập ảnh khuôn mặt để training.

#### **Parameters**:
- `name` (str): Tên người (dùng làm tên thư mục)
- `samples` (int, default=30): Số ảnh cần thu thập

#### **Luồng xử lý chi tiết**:

**Bước 1: Khởi tạo** (Dòng 27-31)
```python
cascade = load_cascade()          # Load face detector
cap = get_camera()                # Mở camera
person_dir = os.path.join(...)    # Tạo đường dẫn thư mục người
os.makedirs(person_dir, ...)      # Tạo thư mục
count = 0                          # Counter ảnh
```

**Bước 2: Vòng lặp chụp ảnh** (Dòng 33-45)

*2.1. Đọc frame từ camera* (Dòng 34)
```python
ret, frame = cap.read()
```
- `ret`: Boolean, True nếu đọc thành công
- `frame`: Numpy array (H×W×3), BGR color space

*2.2. Chuyển sang grayscale* (Dòng 35)
```python
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
```
**Tại sao grayscale?**
- Giảm dữ liệu: 3 channels → 1 channel
- Cascade hoạt động tốt hơn với grayscale
- Tăng tốc độ xử lý (3x faster)

*2.3. Phát hiện khuôn mặt* (Dòng 36)
```python
faces = cascade.detectMultiScale(gray, 1.3, 5)
```

**Parameters giải thích**:
- `scaleFactor=1.3`: Tỷ lệ scale ảnh giữa các lần scan
  - Càng gần 1.0 → Chính xác hơn, chậm hơn
  - Càng lớn → Nhanh hơn, bỏ sót hơn
  - Khuyến nghị: 1.1 - 1.4
  
- `minNeighbors=5`: Số lượng neighbors tối thiểu
  - Số vùng overlap cần thiết để xác nhận là mặt
  - Càng cao → Ít false positive, có thể bỏ sót
  - Khuyến nghị: 3 - 6

**Return**: 
```python
faces = [(x1, y1, w1, h1), (x2, y2, w2, h2), ...]
```
- `x, y`: Tọa độ góc trên-trái
- `w, h`: Chiều rộng, chiều cao bounding box

*2.4. Xử lý từng khuôn mặt* (Dòng 37-41)
```python
for (x,y,w,h) in faces:
    roi = cv2.resize(gray[y:y+h, x:x+w], (200,200))
    cv2.imwrite(os.path.join(person_dir,f"{name}_{count}.jpg"), roi)
    count += 1
    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
```

**Chi tiết từng dòng**:

1. **Extract ROI (Region of Interest)**:
   ```python
   roi = gray[y:y+h, x:x+w]  # Cắt vùng khuôn mặt
   ```
   - Slicing numpy array để lấy vùng khuôn mặt
   
2. **Resize về 200×200**:
   ```python
   roi = cv2.resize(roi, (200,200))
   ```
   - Chuẩn hóa kích thước cho training
   - LBPH yêu cầu ảnh cùng kích thước
   
3. **Lưu ảnh**:
   ```python
   cv2.imwrite(path, roi)
   ```
   - Format: JPEG (nén, tiết kiệm không gian)
   - Tên file: `nguyen_van_a_0.jpg`, `nguyen_van_a_1.jpg`, ...

4. **Vẽ bounding box**:
   ```python
   cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
   ```
   - Màu: (0,255,0) = Green trong BGR
   - Độ dày: 2 pixels
   - Mục đích: Visual feedback cho user

*2.5. Hiển thị và kiểm tra điều kiện dừng* (Dòng 43-45)
```python
cv2.imshow("Capture", frame)
if cv2.waitKey(1) & 0xFF == ord('q') or count >= samples:
    break
```

**cv2.waitKey(1)**:
- Chờ 1ms cho keyboard input
- Return: ASCII code của phím (hoặc -1 nếu không có)
- `& 0xFF`: Lấy 8 bit cuối (đảm bảo cross-platform)
- `ord('q')`: ASCII code của 'q' (113)

**Điều kiện dừng**:
- User nhấn 'q' → Dừng sớm
- `count >= samples` → Đủ số lượng ảnh

**Bước 3: Cleanup** (Dòng 47-48)
```python
cap.release()
cv2.destroyAllWindows()
```
- Release camera resources
- Đóng tất cả OpenCV windows

#### **Tối ưu có thể thêm**:
```python
# Kiểm tra chất lượng ảnh
if w < 100 or h < 100:
    continue  # Bỏ qua khuôn mặt quá nhỏ

# Thêm delay giữa các ảnh
if count > 0 and count % 5 == 0:
    time.sleep(0.5)  # Dừng 0.5s mỗi 5 ảnh
```

---

### 4. train_model() - Dòng 50-74

```python
def train_model():
    faces = []
    labels = []
    map_label = {}
    idx = 0

    for root, dirs, files in os.walk(DATASET_DIR):
        for file in files:
            if file.endswith((".jpg",".png",".jpeg")):
                path = os.path.join(root,file)
                person = os.path.basename(root)
                if person not in map_label:
                    map_label[person] = idx
                    idx += 1

                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                img = cv2.resize(img,(200,200))
                faces.append(img)
                labels.append(map_label[person])

    rec = cv2.face.LBPHFaceRecognizer_create()
    rec.train(faces, np.array(labels))
    rec.save(os.path.join(TRAINER_DIR, "trainer.yml"))
    with open(os.path.join(TRAINER_DIR,"labels.pickle"), "wb") as f:
        pickle.dump(map_label, f)
```

**Mục đích**: Train mô hình LBPH từ dataset đã thu thập.

#### **Luồng xử lý chi tiết**:

**Bước 1: Khởi tạo data structures** (Dòng 51-54)
```python
faces = []        # Danh sách ảnh (numpy arrays)
labels = []       # Danh sách labels tương ứng
map_label = {}    # Mapping: tên → ID số
idx = 0           # Counter cho ID
```

**Bước 2: Thu thập dữ liệu** (Dòng 56-68)

*2.1. Duyệt thư mục dataset* (Dòng 56)
```python
for root, dirs, files in os.walk(DATASET_DIR):
```

**os.walk()** trả về tuple cho mỗi thư mục:
- `root`: Đường dẫn thư mục hiện tại
- `dirs`: List thư mục con
- `files`: List files trong thư mục

**Ví dụ**:
```
dataset/
├── nguyen_van_a/
│   ├── nguyen_van_a_0.jpg
│   └── nguyen_van_a_1.jpg
└── tran_thi_b/
    └── tran_thi_b_0.jpg

→ Iteration 1: root="dataset", dirs=["nguyen_van_a", "tran_thi_b"], files=[]
→ Iteration 2: root="dataset/nguyen_van_a", dirs=[], files=["nguyen_van_a_0.jpg", ...]
→ Iteration 3: root="dataset/tran_thi_b", dirs=[], files=["tran_thi_b_0.jpg"]
```

*2.2. Filter files ảnh* (Dòng 58)
```python
if file.endswith((".jpg",".png",".jpeg")):
```
- Chỉ xử lý files ảnh
- Bỏ qua `.DS_Store`, `Thumbs.db`, etc.

*2.3. Lấy tên người* (Dòng 60)
```python
person = os.path.basename(root)
```
- `root` = `/path/to/dataset/nguyen_van_a`
- `basename(root)` = `nguyen_van_a`

*2.4. Tạo mapping ID* (Dòng 61-63)
```python
if person not in map_label:
    map_label[person] = idx
    idx += 1
```

**Tại sao cần mapping?**
- LBPH chỉ nhận số nguyên làm label
- Cần map: `"nguyen_van_a"` → `0`, `"tran_thi_b"` → `1`, ...

*2.5. Load và chuẩn bị ảnh* (Dòng 65-68)
```python
img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)  # Load as grayscale
img = cv2.resize(img,(200,200))                # Resize (phòng trường hợp)
faces.append(img)                              # Thêm vào list
labels.append(map_label[person])               # Thêm label tương ứng
```

**Sau vòng lặp**:
```python
faces = [img1, img2, img3, ...]   # 90 ảnh (3 người × 30 ảnh)
labels = [0, 0, 0, ..., 1, 1, ..., 2, 2, ...]  # Labels tương ứng
map_label = {"nguyen_van_a": 0, "tran_thi_b": 1, "le_van_c": 2}
```

**Bước 3: Training** (Dòng 70-71)

*3.1. Tạo recognizer* (Dòng 70)
```python
rec = cv2.face.LBPHFaceRecognizer_create()
```

**LBPH Parameters** (có thể tùy chỉnh):
```python
rec = cv2.face.LBPHFaceRecognizer_create(
    radius=1,        # Bán kính cho LBP
    neighbors=8,     # Số điểm lân cận
    grid_x=8,        # Số cell theo chiều X
    grid_y=8,        # Số cell theo chiều Y
    threshold=80.0   # Ngưỡng confidence
)
```

*3.2. Train model* (Dòng 71)
```python
rec.train(faces, np.array(labels))
```

**Quá trình training**:
1. Với mỗi ảnh:
   - Tính toán LBP histogram
   - Chia ảnh thành grid 8×8 = 64 cells
   - Mỗi cell có histogram 256 bins
   - → Tổng: 64 × 256 = 16,384 features

2. Lưu trữ histograms cho mỗi label

3. So sánh bằng Chi-Square distance

**Bước 4: Lưu model** (Dòng 72-74)

*4.1. Lưu model LBPH* (Dòng 72)
```python
rec.save(os.path.join(TRAINER_DIR, "trainer.yml"))
```
- Format: YAML (human-readable)
- Chứa: Histograms, parameters, labels

*4.2. Lưu label mapping* (Dòng 73-74)
```python
with open(os.path.join(TRAINER_DIR,"labels.pickle"), "wb") as f:
    pickle.dump(map_label, f)
```
- Format: Binary (pickle)
- Cần để convert ngược: ID → tên

**Tại sao lưu riêng labels.pickle?**
- Model LBPH chỉ lưu numeric labels (0, 1, 2, ...)
- Cần mapping để biết 0 = ai, 1 = ai
- Pickle nhanh và đơn giản cho dict Python

---

### 5. recognize() - Dòng 76-108

```python
def recognize():
    cascade = load_cascade()
    model = cv2.face.LBPHFaceRecognizer_create()
    model.read(os.path.join(TRAINER_DIR, "trainer.yml"))

    with open(os.path.join(TRAINER_DIR,"labels.pickle"), "rb") as f:
        map_label = pickle.load(f)

    reverse = {v:k for k,v in map_label.items()}
    cam = get_camera()

    while True:
        ret,frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(gray,1.3,5)

        for(x,y,w,h) in faces:
            roi = cv2.resize(gray[y:y+h, x:x+w],(200,200))
            id_,conf = model.predict(roi)

            name = reverse[id_] if conf < 80 else "Unknown"
            color = (0,255,0) if name!="Unknown" else (0,0,255)

            cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
            cv2.putText(frame,name,(x,y-10),
                        cv2.FONT_HERSHEY_SIMPLEX,0.8,color,2)

        cv2.imshow("Recognition", frame)
        if cv2.waitKey(1)&0xFF==ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
```

**Mục đích**: Nhận diện khuôn mặt realtime từ webcam.

#### **Luồng xử lý chi tiết**:

**Bước 1: Khởi tạo** (Dòng 77-85)

*1.1. Load components* (Dòng 77-79)
```python
cascade = load_cascade()                           # Face detector
model = cv2.face.LBPHFaceRecognizer_create()      # Tạo recognizer
model.read(os.path.join(TRAINER_DIR, "trainer.yml"))  # Load trained model
```

*1.2. Load label mapping* (Dòng 81-82)
```python
with open(os.path.join(TRAINER_DIR,"labels.pickle"), "rb") as f:
    map_label = pickle.load(f)
```
→ `map_label = {"nguyen_van_a": 0, "tran_thi_b": 1, ...}`

*1.3. Tạo reverse mapping* (Dòng 84)
```python
reverse = {v:k for k,v in map_label.items()}
```
→ `reverse = {0: "nguyen_van_a", 1: "tran_thi_b", ...}`

**Tại sao cần reverse?**
- Model predict trả về ID số (0, 1, 2, ...)
- Cần convert ngược → tên người để hiển thị

*1.4. Mở camera* (Dòng 85)
```python
cam = get_camera()
```

**Bước 2: Vòng lặp nhận diện** (Dòng 87-105)

*2.1. Đọc frame và phát hiện mặt* (Dòng 88-90)
```python
ret,frame = cam.read()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
faces = cascade.detectMultiScale(gray,1.3,5)
```
- Tương tự `capture_faces()`

*2.2. Xử lý từng khuôn mặt* (Dòng 92-101)

**2.2.1. Chuẩn bị ROI** (Dòng 93)
```python
roi = cv2.resize(gray[y:y+h, x:x+w],(200,200))
```
- Extract và resize về 200×200 (chuẩn với training)

**2.2.2. Predict** (Dòng 94)
```python
id_, conf = model.predict(roi)
```

**QUAN TRỌNG - Giải thích predict()**:

**Return values**:
- `id_`: Label (ID số) được dự đoán
- `conf`: Confidence score (khoảng cách)

**Confidence Score**:
- **Càng thấp = Càng tự tin**
- 0 = Khớp hoàn hảo (không thực tế)
- < 50 = Rất tự tin
- 50-80 = Tự tin
- 80-100 = Không chắc chắn
- \> 100 = Rất khác biệt

**Cách tính**:
- LBPH sử dụng Chi-Square distance
- So sánh histogram của ROI với histograms đã train
- Distance nhỏ = Giống nhau

**2.2.3. Quyết định tên người** (Dòng 96)
```python
name = reverse[id_] if conf < 80 else "Unknown"
```

**Logic**:
```
if conf < 80:
    name = reverse[id_]  # Lấy tên từ ID
else:
    name = "Unknown"      # Không chắc chắn
```

**Threshold = 80**:
- Có thể tùy chỉnh (70, 90, 100, ...)
- Càng thấp → Ít false positive, nhiều false negative
- Càng cao → Nhiều false positive, ít false negative

**Khuyến nghị**:
- 70: Cho môi trường kiểm soát tốt
- 80: Cân bằng (default)
- 100: Cho môi trường ánh sáng kém

**2.2.4. Chọn màu** (Dòng 97)
```python
color = (0,255,0) if name!="Unknown" else (0,0,255)
```
- Green (0,255,0): Nhận diện thành công
- Red (0,0,255): Unknown

**2.2.5. Vẽ UI** (Dòng 99-101)
```python
cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
cv2.putText(frame, name, (x,y-10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
```

**cv2.putText() parameters**:
- `frame`: Ảnh đích
- `name`: Text cần viết
- `(x,y-10)`: Vị trí (trên bounding box 10px)
- `cv2.FONT_HERSHEY_SIMPLEX`: Font chữ
- `0.8`: Font scale
- `color`: Màu text
- `2`: Độ dày text

*2.3. Hiển thị và check exit* (Dòng 103-105)
```python
cv2.imshow("Recognition", frame)
if cv2.waitKey(1)&0xFF==ord('q'):
    break
```

**Bước 3: Cleanup** (Dòng 107-108)
```python
cam.release()
cv2.destroyAllWindows()
```

---

### 6. menu() - Dòng 110-126

```python
def menu():
    while True:
        print("\n1. Thu ảnh training")
        print("2. Train model")
        print("3. Nhận diện realtime")
        print("0. Thoát")
        c=input("Chọn: ")

        if c=="1":
            name=input("Tên người (không dấu): ")
            capture_faces(name)
        elif c=="2":
            train_model()
        elif c=="3":
            recognize()
        else:
            break
```

**Mục đích**: Giao diện điều khiển chương trình.

**Luồng hoạt động**:
1. Hiển thị menu
2. Nhận input từ user
3. Gọi hàm tương ứng
4. Lặp lại (trừ khi thoát)

**Input handling**:
- String comparison (không dùng int để tránh crash)
- Default case: Thoát (any other key)

**Cải thiện có thể thêm**:
```python
# Xử lý exceptions
try:
    if c=="1":
        name = input("Tên người: ")
        capture_faces(name)
        print("✓ Thu thập ảnh thành công!")
except Exception as e:
    print(f"✗ Lỗi: {e}")

# Xác nhận trước khi train
elif c=="2":
    confirm = input("Bắt đầu training? (y/n): ")
    if confirm.lower() == 'y':
        train_model()
        print("✓ Training hoàn tất!")
```

---

### 7. Main Entry Point - Dòng 128-129

```python
if __name__=="__main__":
    menu()
```

**Mục đích**: Entry point của chương trình.

**`if __name__=="__main__"` là gì?**

Khi Python chạy file:
- Nếu file chạy trực tiếp: `__name__ = "__main__"`
- Nếu file được import: `__name__ = "<module_name>"`

**Ví dụ**:
```python
# Chạy: python main.py
# → __name__ = "__main__" → menu() được gọi

# Import: from main import capture_faces
# → __name__ = "main" → menu() KHÔNG được gọi
```

**Ưu điểm**:
- Cho phép reuse functions
- Không chạy menu khi import
- Best practice trong Python

---

## 🧠 Thuật Toán LBPH

### Local Binary Patterns Histograms

**LBPH** là thuật toán nhận diện khuôn mặt dựa trên texture.

### Cách Hoạt Động

#### **Bước 1: Tính Local Binary Pattern**

Với mỗi pixel (điểm trung tâm):

1. Lấy 8 pixels xung quanh (neighbors)
2. So sánh giá trị với center pixel
3. Nếu neighbor ≥ center → 1, ngược lại → 0
4. Tạo số nhị phân 8-bit từ 8 neighbors
5. Convert sang decimal

**Ví dụ**:
```
Original (3×3):        Comparison với center (51):
  40  50  60             0  0  1
  45  51  62      →      0  X  1
  43  48  55             0  0  1

Binary: 10110001 → Decimal: 177
```

#### **Bước 2: Tạo Histogram**

1. Chia ảnh thành grid (ví dụ 8×8 = 64 cells)
2. Với mỗi cell, tạo histogram của LBP values (256 bins)
3. Concatenate tất cả histograms
4. → Feature vector: 64 cells × 256 bins = 16,384 dimensions

#### **Bước 3: So Sánh**

Sử dụng **Chi-Square distance** để so sánh 2 histograms:

```
χ² = Σ [(H1(i) - H2(i))² / (H1(i) + H2(i))]
```

- `H1`, `H2`: Histograms cần so sánh
- Kết quả nhỏ = Giống nhau
- Kết quả lớn = Khác nhau

### Ưu Điểm LBPH

| Ưu Điểm | Giải Thích |
|---------|-----------|
| **Robust với lighting** | LBP chỉ dựa vào relative intensity |
| **Fast** | Không cần deep learning, chỉ histogram |
| **Simple** | Dễ implement và understand |
| **Incremental training** | Có thể update model không cần retrain all |

### Nhược Điểm LBPH

| Nhược Điểm | Giải Thích |
|-----------|-----------|
| **Pose variation** | Kém với khuôn mặt nghiêng nhiều |
| **Accuracy** | Thấp hơn deep learning (FaceNet, ArcFace) |
| **Scale sensitivity** | Cần chuẩn hóa kích thước |

---

## 📊 Luồng Xử Lý Dữ Liệu

### Pipeline Tổng Thể

```
1. DATA COLLECTION
   Camera → Frames → Face Detection → ROI Extraction → Resize → Save
   
2. TRAINING
   Load Images → Compute LBP → Create Histograms → Train Model → Save

3. RECOGNITION
   Camera → Frame → Face Detection → ROI → Predict → Display Result
```

### Chi Tiết Data Flow

#### **1. Capture Faces**
```
Input: Camera stream, Name
↓
Process:
  - Read frame (BGR, H×W×3)
  - Convert to grayscale (H×W)
  - Detect faces → [(x,y,w,h), ...]
  - For each face:
    - Extract ROI (grayscale, w×h)
    - Resize to (200×200)
    - Save as JPEG
↓
Output: dataset/<name>/<name>_<i>.jpg
```

#### **2. Train Model**
```
Input: dataset/ folder
↓
Process:
  - Walk through dataset
  - Load images (grayscale, 200×200)
  - Create label mapping {name: id}
  - Convert to: faces[] (images), labels[] (ids)
  - Train LBPH:
    - Compute LBP for each image
    - Create histograms
    - Store in model
↓
Output: 
  - trainer/trainer.yml (model)
  - trainer/labels.pickle (mapping)
```

#### **3. Recognition**
```
Input: Camera stream, Trained model
↓
Process:
  - Read frame (BGR)
  - Convert to grayscale
  - Detect faces → [(x,y,w,h), ...]
  - For each face:
    - Extract & resize ROI → (200×200)
    - Predict: model.predict(ROI)
      → (predicted_id, confidence)
    - If confidence < threshold:
        name = reverse_map[predicted_id]
      Else:
        name = "Unknown"
    - Draw rectangle & text
↓
Output: Annotated frame display
```

---

## ⚡ Kỹ Thuật Tối Ưu

### 1. Performance Optimization

#### **A. Giảm Kích Thước Frame**
```python
# Trong recognize()
ret, frame = cam.read()
frame = cv2.resize(frame, (640, 480))  # Giảm từ 1920×1080
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
```
**Lợi ích**: Tăng FPS (frames per second)

#### **B. Skip Frames**
```python
frame_count = 0
while True:
    ret, frame = cam.read()
    frame_count += 1
    
    if frame_count % 2 == 0:  # Process mỗi 2 frames
        continue
        
    # ... detection và recognition
```
**Lợi ích**: Giảm CPU usage, vẫn smooth

#### **C. Multi-threading**
```python
import threading

def capture_thread():
    # Capture frames
    pass

def process_thread():
    # Detect & recognize
    pass

# Run parallel
t1 = threading.Thread(target=capture_thread)
t2 = threading.Thread(target=process_thread)
t1.start()
t2.start()
```
**Lợi ích**: Tách capture và processing

---

### 2. Accuracy Improvement

#### **A. Data Augmentation**
```python
def augment_image(img):
    # Flip horizontal
    flipped = cv2.flip(img, 1)
    
    # Rotate ±5 degrees
    rows, cols = img.shape
    M = cv2.getRotationMatrix2D((cols/2, rows/2), 5, 1)
    rotated = cv2.warpAffine(img, M, (cols, rows))
    
    # Adjust brightness
    brighter = cv2.convertScaleAbs(img, alpha=1.2, beta=10)
    
    return [img, flipped, rotated, brighter]
```
**Lợi ích**: Tăng diversity của training data

#### **B. Ensemble Models**
```python
# Train multiple models với parameters khác nhau
model1 = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8)
model2 = cv2.face.LBPHFaceRecognizer_create(radius=2, neighbors=16)

# Predict với cả 2
id1, conf1 = model1.predict(roi)
id2, conf2 = model2.predict(roi)

# Voting
if conf1 < conf2:
    final_id = id1
else:
    final_id = id2
```
**Lợi ích**: Tăng robustness

#### **C. Confidence Thresholding động**
```python
# Tính average confidence cho mỗi người khi train
confidence_stats = {}  # {person_id: avg_confidence}

# Khi recognize, dùng threshold riêng
threshold = confidence_stats[predicted_id] + 10
if conf < threshold:
    name = reverse[predicted_id]
```
**Lợi ích**: Adaptive cho từng người

---

### 3. User Experience

#### **A. Progress Bar khi Training**
```python
from tqdm import tqdm

for file in tqdm(files, desc="Training"):
    # ... process file
```

#### **B. Confidence Display**
```python
# Hiển thị confidence score
text = f"{name} ({conf:.1f})"
cv2.putText(frame, text, (x,y-10), ...)
```

#### **C. FPS Counter**
```python
import time

prev_time = 0
while True:
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time
    
    cv2.putText(frame, f"FPS: {fps:.1f}", (10,30), ...)
```

---

## 🔍 Debugging Tips

### Common Issues & Solutions

#### **1. Không detect được mặt**
```python
# Thử giảm minNeighbors
faces = cascade.detectMultiScale(gray, 1.1, 3)  # Thay vì 5

# Hoặc tăng scaleFactor search range
faces = cascade.detectMultiScale(gray, 1.05, 5)
```

#### **2. Confidence scores quá cao**
```python
# Check số lượng training samples
print(f"Total training images: {len(faces)}")
# Nên ít nhất 30 ảnh/người

# Check chất lượng ảnh
for img in faces:
    if img.mean() < 50:  # Quá tối
        print("Warning: Dark image")
```

#### **3. Memory leak**
```python
# Đảm bảo luôn release
try:
    cam = get_camera()
    # ... use camera
finally:
    cam.release()
    cv2.destroyAllWindows()
```

---

## 📚 Tài Liệu Tham Khảo

- **OpenCV Documentation**: https://docs.opencv.org/
- **LBPH Paper**: Ahonen et al., "Face Recognition with Local Binary Patterns"
- **Haar Cascade**: Viola-Jones, "Rapid Object Detection using a Boosted Cascade"

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Author**: Facial Recognition Lab Team
