---
description: Review yêu cầu tính năng để đảm bảo đầy đủ.
---

Review `docs/ai/requirements/feature-{name}.md` và template cấp dự án `docs/ai/requirements/README.md` để đảm bảo cấu trúc và nội dung đồng bộ.

1. **Sử dụng Bộ nhớ để Lấy Ngữ cảnh** — Tìm kiếm bộ nhớ về các quyết định yêu cầu/domain liên quan trước khi bắt đầu: `npx ai-devkit@latest memory search --query "<feature requirements>"`.
2. Tóm tắt:
   - Phát biểu vấn đề cốt lõi và người dùng bị ảnh hưởng
   - Mục tiêu, không-mục-tiêu, và tiêu chí thành công
   - User stories chính & luồng quan trọng
   - Ràng buộc, giả định, câu hỏi mở
   - Bất kỳ phần thiếu hoặc sai lệch nào so với template
3. **Làm rõ và khám phá (lặp cho đến khi hội tụ)**:
   - **Đặt câu hỏi làm rõ** cho mọi khoảng trống, mâu thuẫn, hoặc mơ hồ. Không chỉ liệt kê vấn đề — chủ động hỏi các câu hỏi cụ thể để giải quyết chúng.
   - **Brainstorm và khám phá các tùy chọn** — Đối với các quyết định chính, đánh đổi, hoặc khu vực có nhiều cách tiếp cận khả thi, chủ động brainstorm các phương án thay thế. Trình bày các tùy chọn với ưu/nhược điểm và đánh đổi. Thách thức các giả định và đưa ra các phương án sáng tạo.
   - **Lặp lại** — Tiếp tục lặp cho đến khi người dùng hài lòng với cách tiếp cận đã chọn và không còn câu hỏi mở.
4. **Lưu trữ Kiến thức Tái sử dụng** — Nếu các quy ước yêu cầu tái sử dụng mới được thống nhất, lưu trữ chúng với `npx ai-devkit@latest memory store ...`.
5. **Hướng dẫn Lệnh Tiếp theo** — Nếu thiếu các yếu tố cơ bản, quay lại `/new-requirement`; nếu không thì tiếp tục với `/review-design`.
