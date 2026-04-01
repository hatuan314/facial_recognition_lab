---
description: Thêm tests cho một tính năng mới.
---

Review `docs/ai/testing/feature-{name}.md` và đảm bảo nó phản ánh template cơ sở trước khi viết tests.

1. **Thu thập Ngữ cảnh** — Nếu chưa được cung cấp, hỏi về: tên feature/branch, tóm tắt các thay đổi (link đến tài liệu thiết kế & yêu cầu), môi trường mục tiêu, các test suites hiện có, và bất kỳ tests flaky/slow nào cần tránh.
2. **Sử dụng Bộ nhớ để Lấy Ngữ cảnh** — Tìm kiếm bộ nhớ về các patterns testing hiện có và edge cases trước đây: `npx ai-devkit@latest memory search --query "<feature testing strategy>"`.
3. **Phân tích Template Testing** — Xác định các phần bắt buộc từ `docs/ai/testing/feature-{name}.md`. Xác nhận tiêu chí thành công và edge cases từ tài liệu yêu cầu & thiết kế. Ghi chú các mocks/stubs/fixtures có sẵn.
4. **Unit Tests (mục tiêu 100% coverage)** — Đối với mỗi module/function: liệt kê các kịch bản hành vi (happy path, edge cases, xử lý lỗi), tạo test cases với assertions sử dụng utilities/mocks hiện có, và làm nổi bật các branches thiếu ngăn cản full coverage.
5. **Integration Tests** — Xác định các luồng cross-component quan trọng. Định nghĩa các bước setup/teardown và test cases cho interaction boundaries, data contracts, và failure modes.
6. **Chiến lược Coverage** — Đề xuất các lệnh công cụ coverage. Chỉ ra các files/functions vẫn cần coverage và đề xuất các tests bổ sung nếu <100%.
7. **Lưu trữ Kiến thức Tái sử dụng** — Lưu các patterns testing tái sử dụng hoặc fixtures phức tạp với `npx ai-devkit@latest memory store ...`.
8. **Cập nhật Tài liệu** — Tóm tắt các tests đã thêm hoặc vẫn còn thiếu. Cập nhật `docs/ai/testing/feature-{name}.md` với links đến test files và kết quả. Đánh dấu các tests hoãn lại như các tasks follow-up.
9. **Hướng dẫn Lệnh Tiếp theo** — Nếu tests phơi bày vấn đề thiết kế, quay lại `/review-design`; nếu không thì tiếp tục với `/code-review`.
