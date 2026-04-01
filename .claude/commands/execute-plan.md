---
description: Thực thi kế hoạch tính năng từng task một.
---

Giúp tôi thực hiện kế hoạch tính năng từng task một.

1. **Thu thập Ngữ cảnh** — Nếu chưa được cung cấp, hỏi về: tên feature (kebab-case, ví dụ: `user-authentication`), mô tả ngắn gọn feature/branch, đường dẫn tài liệu kế hoạch (mặc định `docs/ai/planning/feature-{name}.md`), và bất kỳ tài liệu hỗ trợ nào (thiết kế, yêu cầu, triển khai).
2. **Sử dụng Bộ nhớ để Lấy Ngữ cảnh** — Tìm kiếm các ghi chú/patterns triển khai trước đây trước khi bắt đầu: `npx ai-devkit@latest memory search --query "<feature implementation plan>"`.
3. **Tải & Trình bày Kế hoạch** — Đọc tài liệu kế hoạch và phân tích danh sách tasks (headings + checkboxes). Trình bày hàng đợi tasks được sắp xếp theo nhóm section, với trạng thái: `todo`, `in-progress`, `done`, `blocked`.
4. **Thực thi Task Tương tác** — Đối với mỗi task theo thứ tự: hiển thị ngữ cảnh và văn bản bullet đầy đủ, tham chiếu các tài liệu thiết kế/yêu cầu liên quan, đề xuất phác thảo các bước phụ trước khi bắt đầu, nhắc cập nhật trạng thái (`done`, `in-progress`, `blocked`, `skipped`) với ghi chú ngắn sau khi làm việc, và nếu bị chặn ghi lại blocker và chuyển sang danh sách "Blocked".
5. **Cập nhật Tài liệu Kế hoạch** — Sau mỗi task hoàn thành hoặc thay đổi trạng thái, chạy `/update-planning` để giữ `docs/ai/planning/feature-{name}.md` chính xác.
6. **Lưu trữ Kiến thức Tái sử dụng** — Lưu hướng dẫn/quyết định triển khai tái sử dụng với `npx ai-devkit@latest memory store ...`.
7. **Tóm tắt Phiên làm việc** — Tạo tóm tắt: Đã hoàn thành, Đang tiến hành (với các bước tiếp theo), Bị chặn (với blockers), Bỏ qua/Hoãn lại, và Tasks Mới.
8. **Hướng dẫn Lệnh Tiếp theo** — Tiếp tục `/execute-plan` cho đến khi hoàn thành kế hoạch; sau đó chạy `/check-implementation`.
