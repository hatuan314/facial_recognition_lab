---
description: Review code trước khi push dựa trên tài liệu thiết kế.
---

Thực hiện review code cục bộ **trước khi** push thay đổi.

1. **Thu thập Ngữ cảnh** — Nếu chưa được cung cấp, hỏi về: mô tả feature/branch, danh sách các file đã sửa đổi, tài liệu thiết kế liên quan (ví dụ: `docs/ai/design/feature-{name}.md`), các ràng buộc đã biết hoặc khu vực rủi ro, và các tests đã chạy. Cũng xem xét diff mới nhất qua `git status` và `git diff --stat`.
2. **Sử dụng Bộ nhớ để Lấy Ngữ cảnh** — Tìm kiếm bộ nhớ về tiêu chuẩn review dự án và các lỗi thường gặp: `npx ai-devkit@latest memory search --query "code review checklist project conventions"`.
3. **Hiểu Đồng bộ Thiết kế** — Đối với mỗi tài liệu thiết kế, tóm tắt ý định kiến trúc và các ràng buộc quan trọng.
4. **Review Từng File** — Đối với mỗi file đã sửa đổi: kiểm tra đồng bộ với thiết kế/yêu cầu và đánh dấu sai lệch, phát hiện vấn đề logic/edge cases/code dư thừa, đánh dấu các vấn đề bảo mật (validation đầu vào, secrets, auth, xử lý dữ liệu), kiểm tra xử lý lỗi/hiệu năng/observability, và xác định các tests thiếu hoặc lỗi thời.
5. **Các Vấn đề Xuyên suốt** — Xác minh tính nhất quán đặt tên và quy ước dự án. Xác nhận docs/comments được cập nhật nơi hành vi thay đổi. Xác định các tests thiếu (unit, integration, E2E). Kiểm tra các cập nhật configuration/migration cần thiết.
6. **Lưu trữ Kiến thức Tái sử dụng** — Lưu các phát hiện/checklists review bền vững với `npx ai-devkit@latest memory store ...`.
7. **Tóm tắt Phát hiện** — Phân loại mỗi phát hiện là **blocking**, **important**, hoặc **nice-to-have** với: file, vấn đề, tác động, đề xuất, và tham chiếu thiết kế.
8. **Hướng dẫn Lệnh Tiếp theo** — Nếu còn vấn đề blocking, quay lại `/execute-plan` (sửa code) hoặc `/writing-test` (khoảng trống test); nếu sạch, tiến hành quy trình push/PR.
