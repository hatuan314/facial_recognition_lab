---
description: Đơn giản hóa code hiện có để giảm độ phức tạp.
---

Giúp tôi đơn giản hóa một triển khai hiện có trong khi duy trì hoặc cải thiện chức năng của nó.

1. **Thu thập Ngữ cảnh** — Nếu chưa được cung cấp, hỏi về: file(s) hoặc component(s) mục tiêu để đơn giản hóa, các điểm đau hiện tại (khó hiểu, bảo trì, hoặc mở rộng?), vấn đề hiệu năng hoặc khả năng mở rộng, ràng buộc (tương thích ngược, ổn định API, deadline), và các tài liệu thiết kế hoặc yêu cầu liên quan.
2. **Sử dụng Bộ nhớ để Lấy Ngữ cảnh** — Tìm kiếm bộ nhớ về các patterns đã thiết lập và refactors trước đây trong khu vực này: `npx ai-devkit@latest memory search --query "<component simplification pattern>"`.
3. **Phân tích Độ phức tạp Hiện tại** — Đối với mỗi mục tiêu: xác định nguồn gốc độ phức tạp (nesting sâu, trùng lặp, abstractions không rõ ràng, coupling chặt, over-engineering, magic values), đánh giá cognitive load cho người bảo trì tương lai, và xác định các blocker khả năng mở rộng (single points of failure, sync-where-async-needed, thiếu caching, thuật toán không hiệu quả).
4. **Đề xuất Đơn giản hóa** — Ưu tiên khả năng đọc hơn ngắn gọn; áp dụng kiểm tra 30 giây: liệu một thành viên mới có thể hiểu nhanh mỗi thay đổi không? Đối với mỗi vấn đề, đề xuất các cải tiến cụ thể (extract, consolidate, flatten, decouple, xóa dead code, thay thế bằng built-ins). Cung cấp các đoạn code trước/sau.
5. **Ưu tiên & Lập kế hoạch** — Xếp hạng theo tác động vs rủi ro: (1) tác động cao, rủi ro thấp — làm trước, (2) tác động cao, rủi ro cao hơn — lập kế hoạch cẩn thận, (3) tác động thấp, rủi ro thấp — quick wins nếu có thời gian, (4) tác động thấp, rủi ro cao — bỏ qua hoặc hoãn lại. Đối với mỗi thay đổi chỉ định mức độ rủi ro, yêu cầu testing, và effort. Tạo kế hoạch hành động được ưu tiên với thứ tự thực thi được đề xuất.
6. **Lưu trữ Kiến thức Tái sử dụng** — Lưu các patterns đơn giản hóa tái sử dụng và đánh đổi qua `npx ai-devkit@latest memory store ...`.
7. **Hướng dẫn Lệnh Tiếp theo** — Sau khi triển khai, chạy `/check-implementation` và `/writing-test`.
