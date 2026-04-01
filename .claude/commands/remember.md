---
description: Lưu trữ hướng dẫn tái sử dụng trong dịch vụ bộ nhớ kiến thức.
---

Giúp tôi lưu trữ nó trong dịch vụ bộ nhớ kiến thức.

1. **Ghi nhận Kiến thức** — Nếu chưa được cung cấp, hỏi về: tiêu đề ngắn gọn rõ ràng (5-12 từ), nội dung chi tiết (markdown, khuyến khích ví dụ), tags tùy chọn (từ khóa như "api", "testing"), và scope tùy chọn (`global`, `project:<name>`, `repo:<name>`). Nếu mơ hồ, hỏi thêm để làm cho nó cụ thể và có thể hành động.
2. **Tìm kiếm Trước khi Lưu** — Kiểm tra các mục tương tự hiện có trước với `npx ai-devkit@latest memory search --query "<topic>"` để tránh trùng lặp.
3. **Xác thực Chất lượng** — Đảm bảo nó cụ thể và có thể tái sử dụng (không phải lời khuyên chung chung). Tránh lưu trữ secrets hoặc dữ liệu nhạy cảm.
4. **Lưu trữ** — Gọi `memory.storeKnowledge` với title, content, tags, scope. Nếu công cụ MCP không khả dụng, sử dụng `npx ai-devkit@latest memory store` thay thế.
5. **Xác nhận** — Tóm tắt những gì đã được lưu và đề xuất truy xuất các mục bộ nhớ liên quan khi hữu ích.
6. **Hướng dẫn Lệnh Tiếp theo** — Tiếp tục với lệnh giai đoạn vòng đời hiện tại (`/execute-plan`, `/check-implementation`, `/writing-test`, v.v.) khi cần thiết.
