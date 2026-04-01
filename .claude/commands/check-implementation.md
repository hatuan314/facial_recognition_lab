---
description: So sánh triển khai với tài liệu thiết kế và yêu cầu để đảm bảo đồng bộ.
---

So sánh triển khai hiện tại với thiết kế trong `docs/ai/design/` và yêu cầu trong `docs/ai/requirements/`.

1. Nếu chưa được cung cấp, hỏi về: mô tả feature/branch, danh sách các file đã sửa đổi, tài liệu thiết kế liên quan, và bất kỳ ràng buộc hoặc giả định nào đã biết.
2. **Sử dụng Bộ nhớ để Lấy Ngữ cảnh** — Tìm kiếm bộ nhớ về các ràng buộc đã biết và quyết định trước đây trước khi đánh giá sự không khớp: `npx ai-devkit@latest memory search --query "<feature implementation alignment>"`.
3. Đối với mỗi tài liệu thiết kế: tóm tắt các quyết định kiến trúc và ràng buộc chính, làm nổi bật các components, interfaces, và data flows phải được tôn trọng.
4. So sánh từng file: xác nhận triển khai khớp với ý định thiết kế, ghi chú các sai lệch hoặc phần thiếu, đánh dấu các khoảng trống logic, edge cases, hoặc vấn đề bảo mật, đề xuất đơn giản hóa hoặc refactor, và xác định các tests hoặc cập nhật tài liệu còn thiếu.
5. **Lưu trữ Kiến thức Tái sử dụng** — Lưu các bài học/patterns đồng bộ lặp lại với `npx ai-devkit@latest memory store ...`.
6. Tóm tắt phát hiện với các bước tiếp theo được đề xuất.
7. **Hướng dẫn Lệnh Tiếp theo** — Nếu phát hiện vấn đề thiết kế lớn, quay lại `/review-design` hoặc `/execute-plan`; nếu đã đồng bộ, tiếp tục với `/writing-test`.
