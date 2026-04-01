---
description: Tài liệu hóa điểm vào code trong tài liệu kiến thức.
---

Hướng dẫn tôi tạo hiểu biết có cấu trúc về điểm vào code và lưu vào tài liệu kiến thức.

1. **Thu thập & Xác thực Điểm vào** — Nếu chưa được cung cấp, hỏi về: điểm vào (file, folder, function, API), tại sao nó quan trọng (tính năng, bug, điều tra), và độ sâu hoặc khu vực tập trung mong muốn. Xác nhận điểm vào tồn tại; nếu mơ hồ hoặc không tìm thấy, làm rõ hoặc đề xuất phương án thay thế.
2. **Sử dụng Bộ nhớ để Lấy Ngữ cảnh** — Tìm kiếm bộ nhớ về kiến thức trước đây về module/domain này: `npx ai-devkit@latest memory search --query "<entry point or subsystem>"`.
3. **Thu thập Ngữ cảnh Nguồn** — Đọc file/module chính và tóm tắt mục đích, exports, các pattern chính. Đối với folders: liệt kê cấu trúc, làm nổi bật các module chính. Đối với functions/APIs: ghi lại signature, parameters, return values, xử lý lỗi. Trích xuất các đoạn code thiết yếu (tránh dump lớn).
4. **Phân tích Phụ thuộc** — Xây dựng view phụ thuộc đến độ sâu 3, theo dõi các node đã truy cập để tránh vòng lặp. Phân loại: imports, function calls, services, external packages. Ghi chú các hệ thống bên ngoài hoặc code được tạo tự động để loại trừ.
5. **Tổng hợp Giải thích** — Soạn thảo tổng quan (mục đích, ngôn ngữ, hành vi cấp cao). Chi tiết logic cốt lõi, luồng thực thi, các pattern chính. Làm nổi bật xử lý lỗi, hiệu năng, các cân nhắc bảo mật. Xác định các cải tiến tiềm năng hoặc rủi ro.
6. **Tạo Tài liệu** — Chuẩn hóa tên thành kebab-case (`calculateTotalPrice` → `calculate-total-price`). Tạo `docs/ai/implementation/knowledge-{name}.md` với các phần: Tổng quan, Chi tiết Triển khai, Phụ thuộc, Sơ đồ Trực quan, Thông tin Bổ sung, Metadata, Các Bước Tiếp theo. Bao gồm sơ đồ mermaid khi chúng làm rõ luồng hoặc mối quan hệ. Thêm metadata (ngày phân tích, độ sâu, các file liên quan).
7. **Lưu trữ Kiến thức Tái sử dụng** — Nếu thông tin cần tồn tại qua các phiên làm việc, lưu trữ chúng bằng `npx ai-devkit@latest memory store ...`.
8. **Xem xét & Hành động Tiếp theo** — Tóm tắt các thông tin chính và câu hỏi mở. Đề xuất các khu vực liên quan để đào sâu hơn, xác nhận đường dẫn file, và đề xuất `/remember` cho các quy tắc quan trọng lâu dài.
