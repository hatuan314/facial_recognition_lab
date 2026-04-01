---
description: Debug vấn đề với phân tích nguyên nhân gốc rễ có cấu trúc trước khi thay đổi code.
---

Giúp tôi debug một vấn đề. Làm rõ kỳ vọng, xác định khoảng trống, và thống nhất kế hoạch sửa chữa trước khi thay đổi code.

1. **Thu thập Ngữ cảnh** — Nếu chưa được cung cấp, hỏi về: mô tả vấn đề (điều gì đang xảy ra so với điều gì nên xảy ra), error messages/logs/screenshots, các thay đổi hoặc deployments liên quan gần đây, và phạm vi tác động.
2. **Sử dụng Bộ nhớ để Lấy Ngữ cảnh** — Tìm kiếm bộ nhớ về các sự cố/sửa chữa tương tự trước khi điều tra sâu: `npx ai-devkit@latest memory search --query "<issue symptoms or error>"`.
3. **Làm rõ Thực tế vs Kỳ vọng** — Phát biểu lại hành vi quan sát được so với kỳ vọng. Xác nhận các yêu cầu hoặc tài liệu liên quan định nghĩa kỳ vọng. Định nghĩa tiêu chí chấp nhận cho bản sửa.
4. **Tái tạo & Cô lập** — Xác định khả năng tái tạo (luôn luôn, không thường xuyên, đặc thù môi trường). Ghi lại các bước tái tạo. Liệt kê các components hoặc modules nghi ngờ.
5. **Phân tích Nguyên nhân Tiềm năng** — Brainstorm nguyên nhân gốc rễ (dữ liệu, config, code regressions, phụ thuộc bên ngoài). Thu thập bằng chứng hỗ trợ (logs, metrics, traces). Làm nổi bật những điều chưa biết cần điều tra.
6. **Giải quyết** — Trình bày các tùy chọn giải quyết (quick fix, refactor, rollback, v.v.) với ưu/nhược điểm và rủi ro. Hỏi tùy chọn nào để theo đuổi. Tóm tắt cách tiếp cận đã chọn, công việc chuẩn bị, tiêu chí thành công, và các bước xác thực.
7. **Lưu trữ Kiến thức Tái sử dụng** — Lưu nguyên nhân gốc rễ và các patterns sửa chữa qua `npx ai-devkit@latest memory store ...`.
8. **Hướng dẫn Lệnh Tiếp theo** — Sau khi chọn đường đi sửa chữa, tiếp tục với `/execute-plan`; khi đã triển khai, sử dụng `/check-implementation` và `/writing-test`.
