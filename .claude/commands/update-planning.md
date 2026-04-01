---
description: Cập nhật tài liệu kế hoạch để phản ánh tiến độ triển khai.
---

Giúp tôi đối chiếu tiến độ triển khai hiện tại với tài liệu kế hoạch.

1. **Thu thập Ngữ cảnh** — Nếu chưa được cung cấp, hỏi về: tên feature/branch và trạng thái ngắn gọn, các tasks đã hoàn thành kể từ lần cập nhật cuối, tasks mới được phát hiện, blockers hoặc rủi ro hiện tại, và đường dẫn tài liệu kế hoạch (mặc định `docs/ai/planning/feature-{name}.md`).
2. **Sử dụng Bộ nhớ để Lấy Ngữ cảnh** — Tìm kiếm bộ nhớ về các quyết định trước đây ảnh hưởng đến ưu tiên/phạm vi: `npx ai-devkit@latest memory search --query "<feature planning updates>"`.
3. **Review & Đối chiếu** — Tóm tắt các milestones hiện có, phân tách tasks, và phụ thuộc từ tài liệu kế hoạch. Đối với mỗi task đã lập kế hoạch: đánh dấu trạng thái (done / in progress / blocked / not started), ghi chú thay đổi phạm vi, ghi lại blockers, xác định các tasks bỏ qua hoặc thêm vào.
4. **Tạo Danh sách Task Đã cập nhật** — Tạo checklist được cập nhật nhóm theo: Done, In Progress, Blocked, Newly Discovered Work — với ghi chú ngắn cho mỗi task.
5. **Lưu trữ Kiến thức Tái sử dụng** — Nếu các quy ước kế hoạch mới hoặc quy tắc xử lý rủi ro xuất hiện, lưu trữ chúng với `npx ai-devkit@latest memory store ...`.
6. **Các Bước Tiếp theo & Tóm tắt** — Đề xuất 2-3 tasks có thể hành động tiếp theo và chuẩn bị đoạn tóm tắt cho tài liệu kế hoạch.
7. **Hướng dẫn Lệnh Tiếp theo** — Quay lại `/execute-plan` cho công việc còn lại. Khi tất cả các tasks triển khai hoàn thành, chạy `/check-implementation`.
