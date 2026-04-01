---
description: Xây dựng tài liệu tính năng từ yêu cầu đến kế hoạch.
---

Hướng dẫn tôi thêm một tính năng mới, từ tài liệu yêu cầu đến sẵn sàng triển khai.

1. **Ghi nhận Yêu cầu** — Nếu chưa được cung cấp, hỏi về: tên feature (kebab-case, ví dụ: `user-authentication`), vấn đề nó giải quyết và ai sẽ sử dụng nó, và các user stories chính.
2. **Sử dụng Bộ nhớ để Lấy Ngữ cảnh** — Trước khi hỏi các câu hỏi làm rõ lặp lại, tìm kiếm bộ nhớ về các quyết định hoặc quy ước liên quan qua `npx ai-devkit@latest memory search --query "<feature/topic>"` và tái sử dụng ngữ cảnh liên quan.
3. **Tạo Cấu trúc Tài liệu Tính năng** — Sao chép nội dung của mỗi template (giữ nguyên YAML frontmatter và section headings) vào các file đặc thù cho feature:
   - `docs/ai/requirements/README.md` → `docs/ai/requirements/feature-{name}.md`
   - `docs/ai/design/README.md` → `docs/ai/design/feature-{name}.md`
   - `docs/ai/planning/README.md` → `docs/ai/planning/feature-{name}.md`
   - `docs/ai/implementation/README.md` → `docs/ai/implementation/feature-{name}.md`
   - `docs/ai/testing/README.md` → `docs/ai/testing/feature-{name}.md`
4. **Giai đoạn Yêu cầu** — Điền vào `docs/ai/requirements/feature-{name}.md`: phát biểu vấn đề, mục tiêu/không-mục-tiêu, user stories, tiêu chí thành công, ràng buộc, câu hỏi mở.
5. **Giai đoạn Thiết kế** — Điền vào `docs/ai/design/feature-{name}.md`: thay đổi kiến trúc, data models, API/interfaces, components, quyết định thiết kế, cân nhắc bảo mật và hiệu năng.
6. **Giai đoạn Kế hoạch** — Điền vào `docs/ai/planning/feature-{name}.md`: phân tách tasks với subtasks, phụ thuộc, ước tính effort, thứ tự triển khai, rủi ro.
7. **Lưu trữ Kiến thức Tái sử dụng** — Khi các quy ước hoặc quyết định quan trọng được hoàn thiện, lưu trữ chúng qua `npx ai-devkit@latest memory store --title "<title>" --content "<knowledge>" --tags "<tags>"`.
8. **Hướng dẫn Lệnh Tiếp theo** — Chạy `/review-requirements` trước, sau đó `/review-design`. Nếu cả hai đều pass, tiếp tục với `/execute-plan`.
