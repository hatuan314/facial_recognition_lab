---
description: Review thiết kế tính năng để đảm bảo đầy đủ.
---

Review tài liệu thiết kế trong `docs/ai/design/feature-{name}.md` (và README cấp dự án nếu liên quan).

1. **Sử dụng Bộ nhớ để Lấy Ngữ cảnh** — Tìm kiếm bộ nhớ về các ràng buộc/patterns kiến trúc trước đây: `npx ai-devkit@latest memory search --query "<feature design architecture>"`.
2. Tóm tắt:
   - Tổng quan kiến trúc (đảm bảo sơ đồ mermaid có mặt và chính xác)
   - Các components chính và trách nhiệm của chúng
   - Lựa chọn công nghệ và lý do
   - Data models và mối quan hệ
   - Hợp đồng API/interface (inputs, outputs, auth)
   - Các quyết định thiết kế chính và đánh đổi
   - Yêu cầu phi chức năng phải được bảo toàn
3. **Làm rõ và khám phá (lặp cho đến khi hội tụ)**:
   - **Đặt câu hỏi làm rõ** cho mọi khoảng trống, không nhất quán, hoặc không đồng bộ giữa yêu cầu và thiết kế. Không chỉ liệt kê vấn đề — chủ động hỏi các câu hỏi cụ thể để giải quyết chúng.
   - **Brainstorm và khám phá các tùy chọn** — Đối với các quyết định kiến trúc chính, đánh đổi, hoặc khu vực có nhiều cách tiếp cận khả thi, chủ động brainstorm các phương án thay thế. Trình bày các tùy chọn với ưu/nhược điểm và đánh đổi. Thách thức các giả định và đưa ra các phương án sáng tạo.
   - **Lặp lại** — Tiếp tục lặp cho đến khi người dùng hài lòng với cách tiếp cận đã chọn và không còn câu hỏi mở.
4. **Lưu trữ Kiến thức Tái sử dụng** — Lưu trữ các patterns/ràng buộc thiết kế đã được phê duyệt với `npx ai-devkit@latest memory store ...` khi chúng sẽ giúp ích cho công việc tương lai.
5. **Hướng dẫn Lệnh Tiếp theo** — Nếu phát hiện khoảng trống yêu cầu, quay lại `/review-requirements`; nếu thiết kế vững chắc, tiếp tục với `/execute-plan`.
