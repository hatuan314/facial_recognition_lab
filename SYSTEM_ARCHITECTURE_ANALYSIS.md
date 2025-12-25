# PHÂN TÍCH KIẾN TRÚC HỆ THỐNG VÀ CÔNG NGHỆ AI
## Facial Recognition Lab - Ứng Dụng AI Nhận Diện Khuôn Mặt

---

## 📋 MỤC LỤC

### PHẦN 1: KIẾN TRÚC HỆ THỐNG
1. [Tổng Quan Kiến Trúc AI](#1-tổng-quan-kiến-trúc-ai)
2. [Kiến Trúc AI Pipeline](#2-kiến-trúc-ai-pipeline)
3. [Các Thành Phần AI Core](#3-các-thành-phần-ai-core)
4. [Luồng Xử Lý AI](#4-luồng-xử-lý-ai)

### PHẦN 2: CÁC TÍNH NĂNG CHÍNH
5. [Tính Năng 1: Face Detection với Haar Cascade](#5-tính-năng-1-face-detection-với-haar-cascade)
6. [Tính Năng 2: Face Recognition với LBPH](#6-tính-năng-2-face-recognition-với-lbph)
7. [Tính Năng 3: Training Pipeline](#7-tính-năng-3-training-pipeline)
8. [Kết Luận](#8-kết-luận)

---

# PHẦN 1: KIẾN TRÚC HỆ THỐNG

## 1. TỔNG QUAN KIẾN TRÚC AI

### 1.1. Giới Thiệu

**Facial Recognition Lab** là hệ thống AI nhận diện khuôn mặt realtime được xây dựng trên **Classical Machine Learning** và **Traditional Computer Vision**. Hệ thống kết hợp 2 thuật toán AI chính:

1. **Haar Cascade Classifier** (2001) - Face Detection
2. **LBPH** (Local Binary Patterns Histograms, 2006) - Face Recognition

### 1.2. AI Technology Stack

| Tầng | Công Nghệ | Loại AI | Vai Trò |
|-------|-----------|---------|---------|
| **Detection** | Haar Cascade Classifier | Classical ML | Phát hiện khuôn mặt (Viola-Jones 2001) |
| **Recognition** | LBPH | Texture Analysis | Nhận diện khuôn mặt (Ahonen 2006) |
| **Framework** | OpenCV (cv2) | Computer Vision | Triển khai thuật toán AI |
| **Computation** | NumPy | Numerical | Tính toán ma trận, vector đặc trưng |
| **Preprocessing** | Grayscale, Resize | Image Processing | Chuẩn hóa dữ liệu |
| **Training** | AdaBoost (Haar) | Ensemble Learning | Kết hợp bộ phân loại yếu → mạnh |
| **Comparison** | Chi-Square Distance | Statistical | Đo độ tương đồng histogram |

### 1.3. Phân Loại Công Nghệ AI

```
┌─────────────────────────────────────────────────────────────┐
│                PHÂN LOẠI CÔNG NGHỆ AI                       │
└─────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  CLASSICAL MACHINE LEARNING (Thời kỳ trước Deep Learning)  │
├────────────────────────────────────────────────────────────┤
│  • Haar Cascade (2001): AdaBoost + Cascade                 │
│  • LBPH (2006): Khớp mẫu dựa trên kết cấu                  │
│  • Đặc trưng thủ công (hand-crafted features)              │
│  • Không dùng mạng neural                                  │
│  • Không dùng backpropagation                              │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  TRADITIONAL COMPUTER VISION                               │
├────────────────────────────────────────────────────────────┤
│  • Chuyển đổi ảnh xám (grayscale)                         │
│  • Thay đổi kích thước & chuẩn hóa                         │
│  • Trích xuất vùng quan tâm (ROI)                          │
│  • Các phép toán histogram                                 │
└────────────────────────────────────────────────────────────┘
```

**Nhận xét**: Hệ thống **KHÔNG** sử dụng:
- ❌ Deep Learning (CNN, Neural Networks)
- ❌ Tăng tốc GPU
- ❌ Transfer Learning
- ❌ Học end-to-end

---

## 2. KIẾN TRÚC AI PIPELINE

### 2.1. AI Processing Pipeline Tổng Thể

```
┌─────────────────────────────────────────────────────────────────┐
│                 PIPELINE AI NHẬN DIỆN KHUÔN MẶT                 │
└─────────────────────────────────────────────────────────────────┘

                          ĐẦU VÀO: Video Stream
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  GIAI ĐOẠN 1: TIỀN XỬ LÝ ẢNH                                    │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  • Chuyển đổi BGR → Grayscale                          │     │
│  │  • Giảm không gian màu: 3 kênh → 1 kênh                │     │
│  │  • Công thức: Gray = 0.299R + 0.587G + 0.114B         │     │
│  │  • Mục đích: Giảm dữ liệu, tăng tốc độ                │     │
│  └────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  GIAI ĐOẠN 2: PHÁT HIỆN KHUÔN MẶT AI (Haar Cascade)            │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  Thuật toán: Viola-Jones (2001)                        │     │
│  │  ┌──────────────────────────────────────────────┐      │     │
│  │  │  1. Tính toán Integral Image                 │      │     │
│  │  │     • Tính đặc trưng nhanh O(1)              │      │     │
│  │  │                                               │      │     │
│  │  │  2. Trích xuất Haar-like Features            │      │     │
│  │  │     • Đặc trưng cạnh                          │      │     │
│  │  │     • Đặc trưng đường                         │      │     │
│  │  │     • Đặc trưng tâm-vùng xung quanh          │      │     │
│  │  │                                               │      │     │
│  │  │  3. Phân loại AdaBoost                       │      │     │
│  │  │     • Kết hợp bộ phân loại yếu               │      │     │
│  │  │     • ~200 đặc trưng chọn từ hàng nghìn     │      │     │
│  │  │                                               │      │     │
│  │  │  4. Cấu trúc Cascade                         │      │     │
│  │  │     • Loại bỏ đa giai đoạn                   │      │     │
│  │  │     • Loại nhanh các vùng không phải mặt     │      │     │
│  │  └──────────────────────────────────────────────┘      │     │
│  │                                                         │     │
│  │  Đầu ra: Bounding boxes [(x,y,w,h), ...]               │     │
│  └────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  GIAI ĐOẠN 3: TRÍCH XUẤT ROI & CHUẨN HÓA                        │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  • Trích xuất vùng khuôn mặt từ bounding box           │     │
│  │  • Thay đổi kích thước chuẩn: 200×200 pixels           │     │
│  │  • Phép nội suy: INTER_LINEAR                          │     │
│  │  • Mục đích: Chuẩn hóa đầu vào cho nhận diện          │     │
│  └────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  GIAI ĐOẠN 4: NHẬN DIỆN KHUÔN MẶT AI (LBPH)                    │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  Thuật toán: Local Binary Patterns Histograms (2006)   │     │
│  │  ┌──────────────────────────────────────────────┐      │     │
│  │  │  1. Trích xuất đặc trưng LBP                 │      │     │
│  │  │     • So sánh mỗi pixel với 8 láng giềng     │      │     │
│  │  │     • Tạo mẫu nhị phân                        │      │     │
│  │  │     • Công thức: LBP = Σ s(pi-pc) × 2^i     │      │     │
│  │  │                                               │      │     │
│  │  │  2. Chia lưới                                │      │     │
│  │  │     • Chia ảnh thành lưới 8×8                │      │     │
│  │  │     • Bảo toàn thông tin không gian          │      │     │
│  │  │                                               │      │     │
│  │  │  3. Tính toán Histogram                      │      │     │
│  │  │     • 256 bins mỗi ô                         │      │     │
│  │  │     • 64 ô × 256 bins = 16,384 đặc trưng    │      │     │
│  │  │                                               │      │     │
│  │  │  4. Khớp khoảng cách Chi-Square              │      │     │
│  │  │     • So sánh histogram test vs đã lưu       │      │     │
│  │  │     • χ² = Σ[(H1-H2)²/(H1+H2)]              │      │     │
│  │  │     • Khoảng cách thấp = khớp tốt           │      │     │
│  │  └──────────────────────────────────────────────┘      │     │
│  │                                                         │     │
│  │  Đầu ra: (person_id, confidence_score)                 │     │
│  └────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  GIAI ĐOẠN 5: LOGIC QUYẾT ĐỊNH                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  NẾU confidence < 80:                                   │     │
│  │      → Đã nhận diện (ánh xạ ID sang tên)               │     │
│  │  NGƯỢC LẠI:                                             │     │
│  │      → Người lạ                                         │     │
│  └────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
                    ĐẦU RA: Video Stream có chú thích
```

### 2.2. Kiến Trúc MVC với AI Components

```
┌─────────────────────────────────────────────────────────────┐
│                    KIẾN TRÚC ỨNG DỤNG                       │
│                         (Mô hình MVC)                        │
└─────────────────────────────────────────────────────────────┘

                         main.py (Điểm vào)
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    TẦNG CONTROLLER                          │
│              FaceRecognitionController                      │
│  • Điều phối luồng xử lý AI                                 │
│  • Phối hợp Model ↔ View                                    │
└──────┬──────────────────────────────────┬───────────────────┘
       │                                  │
       ▼                                  ▼
┌──────────────────────┐         ┌──────────────────────┐
│   TẦNG MODEL         │         │    TẦNG VIEW         │
│   (NHÂN AI)          │         │                      │
│                      │         │ • ConsoleView        │
│ ┌──────────────────┐ │         │ • VideoView          │
│ │  THÀNH PHẦN AI   │ │         │                      │
│ ├──────────────────┤ │         └──────────────────────┘
│ │ FaceDetector     │ │
│ │ • Haar Cascade   │ │
│ │ • AdaBoost       │ │
│ ├──────────────────┤ │
│ │ FaceRecognizer   │ │
│ │ • LBPH           │ │
│ │ • Chi-Square     │ │
│ └──────────────────┘ │
│                      │
│ ┌──────────────────┐ │
│ │ DỊCH VỤ HỖ TRỢ   │ │
│ ├──────────────────┤ │
│ │ CameraService    │ │
│ │ DataManager      │ │
│ └──────────────────┘ │
└──────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│                  TẦNG CẤU HÌNH                               │
│  • Tham số thuật toán AI                                     │
│  • CONFIDENCE_THRESHOLD = 80                                 │
│  • DETECTION_SCALE_FACTOR = 1.3                              │
│  • FACE_SIZE = (200, 200)                                    │
└──────────────────────────────────────────────────────────────┘
```

### 2.3. AI Components Mapping

| Thành phần | Công nghệ AI | Triển khai | Mục đích |
|-----------|---------------|----------------|----------|
| **FaceDetector** | Haar Cascade | `cv2.CascadeClassifier` | Phát hiện bounding box khuôn mặt |
| **FaceRecognizer** | LBPH | `cv2.face.LBPHFaceRecognizer_create()` | Nhận diện người |
| **DataManager** | - | File I/O | Lưu trữ dữ liệu huấn luyện & mô hình |
| **CameraService** | - | `cv2.VideoCapture` | Đầu vào video stream |
| **Preprocessing** | Computer Vision | `cv2.cvtColor`, `cv2.resize` | Chuẩn hóa dữ liệu đầu vào |

---

## 3. CÁC THÀNH PHẦN AI CORE

### 3.1. FaceDetector - Haar Cascade Implementation

**AI Technology**: Viola-Jones Face Detection (2001)

#### **3.1.1. Thuật Toán Chi Tiết**

**Haar-like Features**:
```
Phát hiện cạnh:        Phát hiện đường:      Tâm-Xung quanh:
┌───┬───┐             ┌───┬───┬───┐         ┌───────┐
│   │███│             │   │███│   │         │ ┌───┐ │
│   │███│             │   │███│   │         │ │███│ │
└───┴───┘             └───┴───┴───┘         │ └───┘ │
                                             └───────┘

Giá trị = Σ(trắng) - Σ(đen)
```

**Integral Image**:
```python
# Tính toán nhanh O(1) mỗi đặc trưng
II(x,y) = Σ(i≤x, j≤y) I(i,j)

# Tổng hình chữ nhật trong thời gian hằng số
sum = II(x2,y2) - II(x1,y2) - II(x2,y1) + II(x1,y1)
```

**Quy trình huấn luyện AdaBoost**:
```
1. Khởi tạo trọng số: w₁ = 1/N cho tất cả mẫu
2. Với t = 1 đến T:
   a. Huấn luyện bộ phân loại yếu hₜ trên mẫu có trọng số
   b. Tính lỗi: εₜ = Σ wᵢ × I(hₜ(xᵢ) ≠ yᵢ)
   c. Tính trọng số bộ phân loại: αₜ = ½ ln((1-εₜ)/εₜ)
   d. Cập nhật trọng số mẫu:
      wᵢ = wᵢ × exp(-αₜ × yᵢ × hₜ(xᵢ))
   e. Chuẩn hóa trọng số
3. Cuối cùng: H(x) = sign(Σ αₜ × hₜ(x))
```

**Cấu trúc Cascade**:
```
Giai đoạn 1 (2 đặc trưng)  Giai đoạn 2 (10 đặc trưng)  Giai đoạn 3 (25 đặc trưng)
    ↓ Loại 50%                 ↓ Loại 30%                  ↓ Loại 15%
    Qua                        Qua                         Qua
                                                            ↓
                                                    PHÁT HIỆN MẶT
```

#### **3.1.2. Implementation Code**

```python
class FaceDetector:
    def __init__(self, cascade_path=None):
        self._cascade_path = cascade_path or Config.CASCADE_PATH
        self._cascade = cv2.CascadeClassifier(self._cascade_path)
    
    def detect_faces(self, gray_image, scale_factor=None, min_neighbors=None):
        """Phát hiện khuôn mặt bằng Haar Cascade
        
        Args:
            gray_image: Ảnh xám
            scale_factor: Tỷ lệ kim tự tháp ảnh (mặc định 1.3)
            min_neighbors: Số láng giềng tối thiểu để xác nhận (mặc định 5)
        
        Returns:
            Danh sách các bounding box (x, y, w, h)
        """
        scale_factor = scale_factor or Config.DETECTION_SCALE_FACTOR
        min_neighbors = min_neighbors or Config.DETECTION_MIN_NEIGHBORS
        
        faces = self._cascade.detectMultiScale(
            gray_image,
            scaleFactor=scale_factor,
            minNeighbors=min_neighbors
        )
        return faces
```

#### **3.1.3. AI Parameters**

| Tham số | Giá trị | Tác động |
|-----------|-------|--------|
| **scaleFactor** | 1.3 | Tỷ lệ kim tự tháp ảnh. Thấp hơn = chính xác hơn nhưng chậm hơn |
| **minNeighbors** | 5 | Số phát hiện tối thiểu để xác nhận mặt. Cao hơn = ít dương tính giả |
| **minSize** | (30, 30) | Kích thước mặt tối thiểu để phát hiện |
| **maxSize** | - | Kích thước mặt tối đa (không giới hạn) |

**Hiệu năng**:
- Thời gian phát hiện: ~20-30ms mỗi frame (640×480)
- FPS: 30-50 trên CPU
- Độ chính xác: 70-80% (mặt chính diện)

### 3.2. FaceRecognizer - LBPH Implementation

**AI Technology**: Local Binary Patterns Histograms (2006)

#### **3.2.1. Thuật Toán Chi Tiết**

**Bước 1: Tính toán Local Binary Pattern**
```
Cửa sổ 3×3 gốc:            Ngưỡng với tâm (51):
  40  50  60                    0   0   1
  45  51  62         →          0   X   1
  43  48  55                    0   0   1

Nhị phân (theo chiều kim đồng hồ từ trên-trái): 10110001
Thập phân: 177

Công thức: LBP(xc,yc) = Σ(p=0 to 7) s(ip - ic) × 2^p
           trong đó s(x) = 1 nếu x ≥ 0, ngược lại 0
```

**Bước 2: Chia lưới & Histogram**
```
Ảnh 200×200 → lưới 8×8 = 64 ô (mỗi ô 25×25)

┌───┬───┬───┬───┬───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │
├───┼───┼───┼───┼───┼───┼───┼───┤
│ 9 │10 │11 │12 │13 │14 │15 │16 │
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │   │   │ ... (64 ô)        │
└───┴───┴───┴───┴───┴───┴───┴───┘

Mỗi ô → histogram 256 bin
Tổng đặc trưng: 64 × 256 = 16,384 chiều
```

**Bước 3: Khoảng cách Chi-Square**
```
χ²(H₁, H₂) = Σ(i=0 to n-1) [(H₁(i) - H₂(i))² / (H₁(i) + H₂(i))]

Khoảng cách thấp = Khớp tốt hơn
< 50: Rất tự tin
50-80: Tự tin (ngưỡng)
> 80: Không xác định
```

#### **3.2.2. Implementation Code**

```python
class FaceRecognizer:
    def __init__(self):
        self._model = cv2.face.LBPHFaceRecognizer_create()
        self._is_trained = False
    
    def train(self, faces, labels):
        """Huấn luyện mô hình LBPH
        
        Quy trình:
        1. Tính LBP cho mỗi pixel trong mỗi ảnh
        2. Chia thành lưới 8×8
        3. Tính histogram 256-bin cho mỗi ô
        4. Nối tất cả histogram → vector đặc trưng 16,384 chiều
        5. Lưu vector đặc trưng với nhãn
        
        Args:
            faces: Danh sách ảnh xám (200×200)
            labels: Danh sách nhãn số nguyên
        """
        self._model.train(faces, np.array(labels))
        self._is_trained = True
    
    def predict(self, face_image):
        """Dự đoán danh tính
        
        Args:
            face_image: Ảnh xám 200×200
        
        Returns:
            (label_id, confidence): Confidence thấp = khớp tốt hơn
        """
        if not self._is_trained:
            raise Exception("Model not trained")
        
        label, confidence = self._model.predict(face_image)
        return label, confidence
    
    def is_confident(self, confidence, threshold=None):
        """Kiểm tra dự đoán có tự tin không
        
        Args:
            confidence: Khoảng cách Chi-square
            threshold: Ngưỡng confidence (mặc định 80)
        
        Returns:
            True nếu confidence < threshold
        """
        threshold = threshold or Config.CONFIDENCE_THRESHOLD
        return confidence < threshold
```

#### **3.2.3. AI Parameters & Tuning**

| Tham số | Mặc định | Khoảng | Tác động |
|-----------|---------|-------|--------|
| **radius** | 1 | 1-3 | Bán kính vùng lân cận LBP |
| **neighbors** | 8 | 4-16 | Số điểm lấy mẫu |
| **grid_x** | 8 | 4-16 | Số chia lưới ngang |
| **grid_y** | 8 | 4-16 | Số chia lưới dọc |
| **threshold** | 80 | 50-150 | Ngưỡng confidence |

**Số chiều đặc trưng**:
```
Đặc trưng = grid_x × grid_y × 2^neighbors
          = 8 × 8 × 256
          = 16,384 chiều
```

**Hiệu năng**:
- Thời gian huấn luyện: ~1ms mỗi ảnh
- Thời gian dự đoán: ~10ms mỗi mặt
- Độ chính xác: 85-90% (môi trường kiểm soát)
- Độ chính xác (Ánh sáng): 80-85% (ánh sáng thay đổi)
- Độ chính xác (Góc): 50-60% (xoay ±15°)
- Kích thước mô hình: ~200KB mỗi người (30 ảnh)
- Số chiều đặc trưng: 16,384 (histogram 64×256)

### 3.3. Pipeline Tiền Xử Lý Ảnh

**Các bước tiền xử lý liên quan đến AI**:

#### **3.3.1. Chuyển Đổi Ảnh Xám**

```python
# Chuyển đổi có trọng số (theo cảm nhận)
gray = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)

# Công thức
Gray = 0.299 × R + 0.587 × G + 0.114 × B
```

**Tại sao có trọng số?**
- Mắt người nhạy nhất với màu xanh lá
- Ít nhạy nhất với màu xanh dương
- Phù hợp với cảm nhận của con người

**Lợi ích cho AI**:
- ✅ Giảm dữ liệu: 3 kênh → 1 kênh (giảm 66%)
- ✅ Xử lý nhanh hơn: Ít tính toán hơn
- ✅ Đặc trưng tốt hơn: Haar & LBPH hoạt động tốt với ảnh xám
- ✅ Bất biến ánh sáng: Loại bỏ thiên lệch màu sắc

#### **3.3.2. Chuẩn Hóa Ảnh**

```python
# Thay đổi kích thước về chuẩn
face_normalized = cv2.resize(face_roi, (200, 200), 
                             interpolation=cv2.INTER_LINEAR)
```

**Tại sao 200×200?**
- Đủ lớn: Bảo toàn chi tiết khuôn mặt
- Đủ nhỏ: Xử lý nhanh
- Kích thước chuẩn: Yêu cầu cho huấn luyện LBPH
- Thân thiện với lưới: 200÷8 = 25 pixel mỗi ô

**Phương pháp nội suy**:
- `INTER_LINEAR`: Nhanh, chất lượng tốt (mặc định)
- `INTER_CUBIC`: Chậm hơn, chất lượng tốt hơn
- `INTER_AREA`: Tốt nhất cho giảm kích thước

### 3.4. Tham Số Cấu Hình AI

**Tham số AI tập trung** trong `config.py`:

```python
class Config:
    # Phát hiện khuôn mặt (Haar Cascade)
    CASCADE_PATH = "haarcascades/haarcascade_frontalface_default.xml"
    DETECTION_SCALE_FACTOR = 1.3      # Tỷ lệ kim tự tháp ảnh
    DETECTION_MIN_NEIGHBORS = 5       # Số phát hiện tối thiểu để xác nhận
    
    # Nhận diện khuôn mặt (LBPH)
    FACE_SIZE = (200, 200)            # Kích thước mặt chuẩn
    CONFIDENCE_THRESHOLD = 80         # Ngưỡng nhận diện
    
    # Huấn luyện
    DEFAULT_SAMPLES = 30              # Số ảnh mỗi người
    
    # Lưu trữ dữ liệu
    DATASET_DIR = "dataset/"
    TRAINER_DIR = "trainer/"
    TRAINER_MODEL_FILE = "trainer.yml"     # Mô hình LBPH
    LABELS_PICKLE_FILE = "labels.pickle"   # Ánh xạ nhãn
```

**Hướng dẫn điều chỉnh**:

| Trường hợp | SCALE_FACTOR | MIN_NEIGHBORS | THRESHOLD |
|----------|--------------|---------------|------------|
| **Độ chính xác cao** | 1.1 | 7 | 70 |
| **Cân bằng** | 1.3 | 5 | 80 |
| **Tốc độ cao** | 1.5 | 3 | 90 |
| **Bảo mật nghiêm ngặt** | 1.1 | 8 | 60 |

---

## 4. LUỒNG XỬ LÝ DỮ LIỆU

### 4.1. Luồng Dữ Liệu - Thu Thập Khuôn Mặt

```
Đầu vào người dùng (tên)
    ↓
Controller.capture_faces(name)
    ↓
CameraService.open() → Camera stream
    ↓
Vòng lặp:
    ├─ CameraService.read() → Frame (BGR, H×W×3)
    ├─ cv2.cvtColor() → Grayscale (H×W)
    ├─ FaceDetector.detect_faces() → [(x,y,w,h), ...]
    ├─ Với mỗi khuôn mặt:
    │   ├─ FaceDetector.extract_face_roi() → ROI (200×200)
    │   ├─ DataManager.save_face_image() → Đĩa
    │   └─ VideoView.draw_face_rectangle() → Phản hồi trực quan
    └─ VideoView.show_frame() → Hiển thị
    ↓
CameraService.release()
VideoView.close_all_windows()
```

### 4.2. Luồng Dữ Liệu - Huấn Luyện Mô Hình

```
Controller.train_model()
    ↓
DataManager.load_training_data()
    ├─ os.walk(DATASET_DIR)
    ├─ Với mỗi ảnh:
    │   ├─ cv2.imread() → Grayscale
    │   ├─ cv2.resize() → (200×200)
    │   ├─ Thêm vào faces[]
    │   └─ Thêm nhãn vào labels[]
    └─ Tạo label_map {name: id}
    ↓
FaceRecognizer.train(faces, labels)
    ├─ Tính LBP cho mỗi ảnh
    ├─ Tạo histogram
    └─ Huấn luyện mô hình LBPH
    ↓
DataManager.save_model(model, label_map)
    ├─ model.save() → trainer.yml
    └─ pickle.dump() → labels.pickle
    ↓
ConsoleView.show_success()
```

### 4.3. Luồng Dữ Liệu - Nhận Diện

```
Controller.recognize_faces()
    ↓
DataManager.load_model_and_labels()
    ├─ Tải trainer.yml
    └─ Tải labels.pickle
    ↓
FaceRecognizer.load_model(model_path)
    ↓
Tạo reverse_map {id: name}
    ↓
CameraService.open()
    ↓
Vòng lặp:
    ├─ CameraService.read() → Frame
    ├─ cv2.cvtColor() → Grayscale
    ├─ FaceDetector.detect_faces() → Faces
    ├─ Với mỗi khuôn mặt:
    │   ├─ Trích xuất ROI (200×200)
    │   ├─ FaceRecognizer.predict(ROI) → (id, confidence)
    │   ├─ Nếu confidence < 80:
    │   │   └─ name = reverse_map[id]
    │   ├─ Ngược lại:
    │   │   └─ name = "Unknown"
    │   ├─ VideoView.draw_face_rectangle(color)
    │   └─ VideoView.draw_text(name)
    └─ VideoView.show_frame()
    ↓
Dọn dẹp
```

---

# PHẦN 2: CÁC TÍNH NĂNG CHÍNH

## 5. TÍNH NĂNG 1: FACE DETECTION VỚI HAAR CASCADE

### 5.1. Mô Tả Tính Năng

**Chức năng**: Phát hiện khuôn mặt trong video stream realtime

**AI Technology**: Viola-Jones Haar Cascade Classifier (2001)

### 5.2. AI Workflow Chi Tiết

```
┌─────────────────────────────────────────────────────────────┐
│           LUỒNG XỬ LÝ AI PHÁT HIỆN KHUÔN MẶT               │
└─────────────────────────────────────────────────────────────┘

Đầu vào: BGR Frame (H×W×3)
    ↓
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 1: Tiền xử lý                                          │
│ • Chuyển đổi BGR → Grayscale                                │
│ • Công thức: Gray = 0.299R + 0.587G + 0.114B               │
│ • Đầu ra: Ảnh xám (H×W)                                     │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 2: Phát hiện đa tỷ lệ                                  │
│ • Tạo kim tự tháp ảnh (scale = 1.3)                         │
│ • Các tỷ lệ: 1.0, 1.3, 1.69, 2.20, ...                     │
│ • Phát hiện ở mỗi tỷ lệ                                     │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 3: Cửa sổ trượt                                        │
│ • Kích thước cửa sổ: 24×24 pixels                           │
│ • Bước nhảy: Thay đổi theo tỷ lệ                            │
│ • Quét toàn bộ ảnh                                          │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 4: Trích xuất đặc trưng (Integral Image)               │
│ • Tính integral image: O(W×H)                               │
│ • Trích xuất đặc trưng Haar: O(1) mỗi đặc trưng            │
│ • ~2000 đặc trưng mỗi cửa sổ                                │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 5: Phân loại Cascade                                   │
│ ┌─────────────────────────────────────────────────────┐     │
│ │ Giai đoạn 1 (2 đặc trưng)                           │     │
│ │ • Loại bỏ nhanh các vùng rõ ràng không phải mặt     │     │
│ │ • Loại ~50% cửa sổ                                  │     │
│ └─────────────────────────────────────────────────────┘     │
│                        ↓ Qua                                 │
│ ┌─────────────────────────────────────────────────────┐     │
│ │ Giai đoạn 2 (10 đặc trưng)                          │     │
│ │ • Phân tích chi tiết hơn                            │     │
│ │ • Loại ~30% còn lại                                 │     │
│ └─────────────────────────────────────────────────────┘     │
│                        ↓ Qua                                 │
│ ┌─────────────────────────────────────────────────────┐     │
│ │ Giai đoạn 3-N (25+ đặc trưng mỗi giai đoạn)        │     │
│ │ • Xác minh cuối cùng                                │     │
│ │ • Phát hiện mặt với độ tin cậy cao                  │     │
│ └─────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 6: Loại bỏ tối đa không cực đại                        │
│ • Gộp các phát hiện chồng lấp                               │
│ • minNeighbors = 5 (số chồng lấp tối thiểu để xác nhận)    │
│ • Đầu ra: Bounding box cuối cùng                            │
└─────────────────────────────────────────────────────────────┘
    ↓
Đầu ra: [(x, y, w, h), ...] - Danh sách bounding box khuôn mặt
```

### 5.3. Chỉ Số Hiệu Năng

| Chỉ số | Giá trị | Ghi chú |
|--------|-------|-------|
| **Thời gian phát hiện** | 20-30ms | Mỗi frame (640×480) |
| **FPS** | 30-50 | Trên CPU |
| **Độ chính xác (Chính diện)** | 70-80% | Ánh sáng tốt |
| **Độ chính xác (Nghiêng)** | 20-30% | Xoay ±45° |
| **Tỷ lệ dương tính giả** | 10-20% | Phụ thuộc minNeighbors |
| **Kích thước mặt tối thiểu** | 30×30 px | Có thể cấu hình |

### 5.4. Use Cases & Limitations

**✅ Tốt cho**:
- Phát hiện mặt chính diện (xoay 0-15°)
- Ánh sáng kiểm soát
- Môi trường trong nhà
- Ứng dụng thời gian thực (chỉ CPU)

**❌ Hạn chế**:
- Kém với mặt nghiêng (xoay >30°)
- Nhạy cảm với thay đổi ánh sáng
- Dương tính giả với các mẫu giống mặt
- Không thể phát hiện điểm đặc trưng khuôn mặt

---

## 6. TÍNH NĂNG 2: FACE RECOGNITION VỚI LBPH

### 6.1. Mô Tả Tính Năng

**Chức năng**: Nhận diện danh tính khuôn mặt

**AI Technology**: Local Binary Patterns Histograms (2006)

### 6.2. AI Workflow Chi Tiết

#### **6.2.1. Giai Đoạn Huấn Luyện**

```
┌─────────────────────────────────────────────────────────────┐
│              LUỒNG HUẤN LUYỆN LBPH                          │
└─────────────────────────────────────────────────────────────┘

Đầu vào: Thư mục dataset với ảnh đã gán nhãn
    ↓
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 1: Tải dữ liệu                                          │
│ • Quét thư mục dataset/                                    │
│ • Tải tất cả ảnh (.jpg, .png, .jpeg)                      │
│ • Tạo ánh xạ nhãn: {name → ID}                            │
│ • Ví dụ: {"john": 0, "mary": 1, "bob": 2}                  │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 2: Chuẩn hóa ảnh                                       │
│ • Thay đổi kích thước tất cả ảnh về 200×200                │
│ • Đảm bảo định dạng grayscale                            │
│ • Chuẩn hóa kích thước đầu vào                           │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 3: Trích xuất đặc trưng LBP (Mỗi ảnh)                 │
│ ┌─────────────────────────────────────────────────────┐     │
│ │ 3a. Tính LBP cho mỗi pixel                        │     │
│ │     • So sánh với 8 láng giềng                      │     │
│ │     • Tạo mã nhị phân 8-bit                       │     │
│ │     • Chuyển sang thập phân (0-255)                │     │
│ │     • Thời gian: ~5ms mỗi ảnh 200×200             │     │
│ └─────────────────────────────────────────────────────┘     │
│                        ↓                                     │
│ ┌─────────────────────────────────────────────────────┐     │
│ │ 3b. Chia lưới                                      │     │
│ │     • Chia 200×200 thành lưới 8×8                 │     │
│ │     • Mỗi ô: 25×25 pixels                         │     │
│ │     • Tổng: 64 ô                                   │     │
│ └─────────────────────────────────────────────────────┘     │
│                        ↓                                     │
│ ┌─────────────────────────────────────────────────────┐     │
│ │ 3c. Tính toán Histogram                           │     │
│ │     • Histogram 256-bin mỗi ô                    │     │
│ │     • Đếm tần suất mỗi giá trị LBP                │     │
│ │     • 64 ô × 256 bins = 16,384 đặc trưng         │     │
│ └─────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 4: Huấn luyện mô hình                                   │
│ • Lưu tất cả vector đặc trưng với nhãn                      │
│ • Không cần tối ưu hóa (khớp mẫu)                         │
│ • Thời gian huấn luyện: ~1ms mỗi ảnh                       │
│ • Tổng: ~100ms cho 100 ảnh                                  │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 5: Lưu trữ mô hình                                      │
│ • Lưu vào trainer/trainer.yml (định dạng YAML)              │
│ • Lưu ánh xạ nhãn vào trainer/labels.pickle                │
│ • Kích thước mô hình: ~200KB mỗi người (30 ảnh)           │
└─────────────────────────────────────────────────────────────┘
```

#### **6.2.2. Giai Đoạn Dự Đoán**

```
┌─────────────────────────────────────────────────────────────┐
│            LUỒNG DỰ ĐOÁN LBPH                               │
└─────────────────────────────────────────────────────────────┘

Đầu vào: Ảnh khuôn mặt test (200×200 grayscale)
    ↓
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 1: Trích xuất đặc trưng                                │
│ • Giống như huấn luyện: LBP → Lưới → Histogram              │
│ • Đầu ra: Vector đặc trưng 16,384 chiều                     │
│ • Thời gian: ~5ms                                            │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 2: Tính toán khoảng cách                               │
│ • So sánh với tất cả mẫu đã lưu                             │
│ • Sử dụng khoảng cách Chi-Square:                           │
│   χ²(H₁,H₂) = Σ[(H₁(i)-H₂(i))²/(H₁(i)+H₂(i))]             │
│ • Khoảng cách thấp = Khớp tốt hơn                           │
│ • Thời gian: ~5ms cho 100 người                             │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 3: Tìm khớp tốt nhất                                   │
│ • Chọn khoảng cách tối thiểu                                │
│ • Lấy ID nhãn tương ứng                                     │
│ • Trả về (label_id, confidence_score)                       │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 4: Quyết định ngưỡng                                   │
│ • NẾU confidence < 80:                                      │
│     → Đã nhận diện (ánh xạ ID sang tên)                     │
│ • NGƯỢC LẠI:                                                │
│     → Người lạ                                              │
└─────────────────────────────────────────────────────────────┘
    ↓
Đầu ra: (person_name, confidence) hoặc ("Unknown", confidence)
```

### 6.3. Chỉ Số Hiệu Năng

| Chỉ số | Giá trị | Ghi chú |
|--------|-------|-------|
| **Thời gian huấn luyện** | ~1ms/ảnh | Chỉ CPU |
| **Thời gian dự đoán** | ~10ms | Mỗi mặt |
| **Độ chính xác** | 85-90% | Môi trường kiểm soát |
| **Độ chính xác (Ánh sáng)** | 80-85% | Ánh sáng thay đổi |
| **Độ chính xác (Góc)** | 50-60% | Xoay ±15° |
| **Kích thước mô hình** | ~200KB/người | 30 ảnh mỗi người |
| **Số chiều đặc trưng** | 16,384 | Histogram 64×256 |

### 6.4. Giải Thích Điểm Confidence

```
Phân tích khoảng Confidence:

< 30:  ████████████████████ Khớp xuất sắc (95%+ đúng)
30-50: ███████████████      Khớp rất tốt (90%+ đúng)
50-70: ██████████           Khớp tốt (85%+ đúng)
70-80: ████                 Chấp nhận được (ngưỡng)
80-100:██                   Khớp kém (có thể sai)
> 100: ▓                    Rất kém (chắc chắn sai)
```

### 6.5. Use Cases & Limitations

**✅ Tốt cho**:
- Môi trường ánh sáng kiểm soát
- Mặt chính diện (xoay ±15°)
- Quy mô nhỏ (< 100 người)
- Nhận diện thời gian thực (chỉ CPU)
- Học tăng dần (thêm người mới dễ dàng)

**❌ Hạn chế**:
- Độ chính xác thấp hơn deep learning (85-90% vs 99%)
- Kém với thay đổi góc (xoay >15°)
- Không xử lý được che khuất (khẩu trang, kính)
- Độ phức tạp tuyến tính (chậm với > 100 người)
- Nhạy cảm với căn chỉnh

---

## 7. TÍNH NĂNG 3: TRAINING PIPELINE

### 7.1. Quy Trình Thu Thập Dữ Liệu

**Các yếu tố AI cần xem xét**:

```
┌─────────────────────────────────────────────────────────────┐
│         CHẤT LƯỢNG DỮ LIỆU CHO HUẤN LUYỆN AI                │
└─────────────────────────────────────────────────────────────┘

CÁC YẾU TỐ QUAN TRỌNG:

1. Số lượng:
   • Tối thiểu: 30 ảnh mỗi người
   • Khuyến nghị: 50-100 ảnh
   • Nhiều dữ liệu hơn = Tổng quát hóa tốt hơn

2. Đa dạng:
   • Biểu cảm khuôn mặt: trung tính, cười, nghiêm túc
   • Góc đầu: xoay ±10°
   • Ánh sáng: các góc độ khác nhau
   • Khoảng cách: biến đổi nhẹ

3. Chất lượng:
   • Độ phân giải: Ít nhất 200×200 pixels
   • Lấy nét: Sắc nét, không mờ
   • Ánh sáng: Đủ sáng, tránh bóng đổ
   • Nền: Ít phân tâm nhất có thể

4. Nhất quán:
   • Cùng camera
   • Môi trường tương tự
   • Tiền xử lý nhất quán
```

### 7.2. Thực Hành Tốt Nhất Khi Huấn Luyện

**Để đạt hiệu năng AI tối ưu**:

| Thực hành | Tác động | Lý do |
|----------|--------|--------|
| **Thu thập 50+ ảnh** | +5-10% độ chính xác | Bao phủ đặc trưng tốt hơn |
| **Đa dạng biểu cảm** | +3-5% độ chính xác | Tổng quát hóa |
| **Ánh sáng tốt** | +10-15% độ chính xác | Giảm nhiễu |
| **Mặt chính diện** | +15-20% độ chính xác | Thuật toán tối ưu cho điều này |
| **Khoảng cách nhất quán** | +5% độ chính xác | Chuẩn hóa tỷ lệ |
| **Nền sạch** | +3% độ chính xác | Giảm đặc trưng giả |

### 7.3. Đánh Giá Mô Hình

**Các chỉ số cần theo dõi**:

```python
# Pseudo-code cho đánh giá
def evaluate_model(test_set):
    metrics = {
        'accuracy': 0,
        'precision': 0,
        'recall': 0,
        'f1_score': 0,
        'avg_confidence': 0
    }
    
    for test_image, true_label in test_set:
        pred_label, confidence = model.predict(test_image)
        
        if pred_label == true_label:
            metrics['accuracy'] += 1
        
        # Theo dõi phân bố confidence
        metrics['avg_confidence'] += confidence
    
    return metrics
```

---

## 8. KẾT LUẬN

### 8.1. Tổng Kết Công Nghệ AI

**Hệ thống sử dụng Classical Machine Learning**:

| Khía cạnh | Đánh giá |
|--------|------------|
| **Thời kỳ AI** | Trước Deep Learning (2001-2006) |
| **Độ phức tạp** | Thấp - Không có mạng neural |
| **Huấn luyện** | Nhanh - Vài giây đến vài phút |
| **Suy luận** | Thời gian thực - 30-50 FPS |
| **Phần cứng** | Chỉ CPU - Không cần GPU |
| **Độ chính xác** | Trung bình - 85-90% |
| **Khả năng mở rộng** | Hạn chế - < 100 người |

### 8.2. Phù Hợp Cho

✅ **Xuất sắc cho**:
- Học các khái niệm AI/ML
- Tạo nguyên mẫu hệ thống nhận diện khuôn mặt
- Triển khai quy mô nhỏ (< 50 người)
- Môi trường hạn chế tài nguyên (không có GPU)
- Ứng dụng thời gian thực trên CPU

⚠️ **Không khuyến nghị cho**:
- Hệ thống production yêu cầu độ chính xác > 95%
- Triển khai quy mô lớn (> 100 người)
- Môi trường không kiểm soát (ngoài trời, góc đa dạng)
- Ứng dụng quan trọng về bảo mật
- Hệ thống cần xử lý che khuất

### 8.3. Lộ Trình Nâng Cấp Lên AI Hiện Đại

**Lộ trình phát triển**:

```
Hiện tại (Classical ML)
    ↓
Giai đoạn 1: Cải tiến
    • Căn chỉnh khuôn mặt
    • Tiền xử lý CLAHE
    • Tăng cường dữ liệu
    ↓
Giai đoạn 2: Kết hợp
    • LBPH + Đặc trưng sâu (VGGFace)
    • Phương pháp ensemble
    ↓
Giai đoạn 3: Deep Learning hoàn toàn
    • FaceNet (độ chính xác 99.6%)
    • ArcFace (độ chính xác 99.8%)
    • Tăng tốc GPU
```

---

**Phiên bản**: 2.0 (Tập trung AI)  
**Ngày cập nhật**: 25/12/2024  
**Tác giả**: Nhóm Phân Tích Công Nghệ AI