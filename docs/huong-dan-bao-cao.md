# Báo cáo thực hành — Đề 28: Quản lý Cửa hàng Thú cưng

Tài liệu đang soạn. Bắt đầu tại [Nhiệm vụ 1 — Chuẩn bị và tiêu chí](01-chuan-bi-va-tieu-chi.md), có kết quả kiểm tra ngày 23/10/2026 và nội dung viết báo cáo cho người mới. Các phần kết quả chỉ được hoàn thiện sau khi thực hành và kiểm chứng. Không coi kế hoạch dưới đây là kết quả đã đạt.

## Phạm vi

Xây dựng website quản lý thú cưng, dịch vụ spa, khách hàng và lịch hẹn. Sử dụng PostgreSQL và pgAdmin; triển khai toàn bộ dịch vụ bằng Docker Compose. Mã nguồn hiện có sử dụng Python/Flask theo gợi ý đề bài.

Không tự thêm dữ liệu nghiệp vụ mẫu. Sinh viên cung cấp hoặc duyệt dữ liệu trước khi nhập. Ảnh minh chứng do sinh viên tự chụp, không tạo ảnh minh chứng giả.

## Nội dung có thể viết ở bước mở đầu

“Đề tài triển khai hệ thống quản lý cửa hàng thú cưng với các nhóm chức năng quản lý thú cưng, dịch vụ spa, khách hàng và lịch hẹn. Hệ thống sử dụng PostgreSQL để lưu dữ liệu và pgAdmin để quản trị cơ sở dữ liệu. Các dịch vụ được khai báo bằng Docker Compose. Nội dung thực hành bao gồm quản lý mã nguồn trên GitHub, cấu hình Nginx reverse proxy, giám sát bằng Prometheus và Grafana, thu thập log bằng Loki và Promtail, cùng các biện pháp củng cố bảo mật.”

Đây là mục tiêu và phạm vi dự kiến, không phải tuyên bố đã triển khai thành công.

## Bố cục báo cáo tối thiểu 10 trang

1. Bìa theo định dạng báo cáo thực tập: thông tin sinh viên và tên đề tài; chờ sinh viên cung cấp thông tin.
2. Giới thiệu đề tài, mục tiêu và phạm vi.
3. Môi trường thực hành và kiến trúc hệ thống thực tế đã triển khai.
4. Mã nguồn, cấu hình GitHub, lịch sử commit và cách chạy.
5. Website, PostgreSQL và pgAdmin: chức năng và kết quả kiểm chứng.
6. Nginx reverse proxy và HTTPS tự ký hoặc security headers.
7. Prometheus và Grafana: metrics của container, web server và database.
8. Loki, Promtail và ít nhất 2–3 truy vấn LogQL có kết quả thực tế.
9. Ít nhất 3–4 biện pháp hardening và cách kiểm chứng từng biện pháp.
10. Kết quả tổng hợp, lỗi thực tế gặp phải, cách xử lý và kết luận.

Đây là các mục nội dung, không quy định mỗi mục đúng một trang. Chèn ảnh thật và giải thích để hoàn thành yêu cầu tối thiểu 10 trang.

## Các nhiệm vụ và minh chứng dự kiến

| Nhiệm vụ | Điều kiện hoàn thành | Phần sinh viên tự chụp |
|---|---|---|
| Chuẩn bị | Xác định môi trường, công nghệ và danh tính Git | Chưa cần ảnh |
| Website và DB | Các chức năng đề 28 chạy, kết nối PostgreSQL, pgAdmin hoạt động | Giao diện chức năng và công cụ DB với dữ liệu đã duyệt |
| Reverse proxy | Truy cập website qua Nginx; có HTTPS tự ký hoặc security headers | Website và kết quả kiểm tra cấu hình |
| Giám sát | Prometheus thu thập metrics; Grafana hiển thị container/web/DB | Targets và dashboard thực tế |
| Log | Loki + Promtail hoạt động; ít nhất 2–3 query LogQL | Truy vấn và kết quả thực tế |
| Hardening | Kiểm chứng ít nhất 3–4 biện pháp bảo mật | Kết quả kiểm tra từng biện pháp, che thông tin bí mật |
| Tổng hợp | README chạy lại được, báo cáo đủ nội dung, demo toàn bộ | Lịch sử commit và các minh chứng còn thiếu |

Mỗi nhiệm vụ hoàn tất phải có commit có ý nghĩa và push GitHub. Giữ rõ ba mốc theo đề: Nginx, giám sát và log. Các commit bổ sung theo yêu cầu của sinh viên không thay thế ba mốc này.

## Quy trình ghi báo cáo ở mỗi nhiệm vụ

Hướng dẫn các phần đã triển khai:

- [Nginx Reverse Proxy và security headers](04-nginx-reverse-proxy.md).
- [Prometheus, Grafana và minh chứng giám sát container/web/DB](05-prometheus-grafana.md).
- [Loki, Promtail và ba truy vấn LogQL](06-loki-promtail.md).
- [Hardening và các bước kiểm chứng chỉ đọc](07-hardening.md).
- [Đăng nhập và phân quyền website theo yêu cầu bổ sung](09-phan-quyen-website.md).

- Ghi mục đích của bước thực hành.
- Ghi file cấu hình, lệnh đã thực hiện và giải thích ngắn gọn.
- Ghi cách kiểm tra, kết quả quan sát thật và lỗi đã xử lý nếu có.
- Khi được mở đúng màn hình, tự chụp ảnh; chèn ảnh vào mục tương ứng và ghi chú ảnh.
- Ghi mã commit sau khi push thành công.

## Tình trạng cập nhật ngày 23/10/2026

- Repository đích: https://github.com/longtranyd-ui/DTC245200404
- README.md rỗng đã được push lên main ở commit 7b742ba; sẽ bổ sung hướng dẫn chạy sau khi kiểm chứng.
- Đã xác nhận Ubuntu WSL2, ba dịch vụ app/db/pgadmin đang chạy và ứng dụng kết nối PostgreSQL.
- Sinh viên cho phép giữ nguyên và chỉ đọc bộ dữ liệu hiện có. Mỗi bảng nghiệp vụ hiện có một bản ghi.
- Chưa xác nhận sinh viên đã chụp ảnh. Các tiêu chí còn lại được theo dõi trong tài liệu nhiệm vụ 1.

## Căn cứ

- Đề tài thực hành TKQT HTPM K23: trang 1–2 (yêu cầu chung và thang điểm), trang 8 (đề 28).
- Các chương 1–9, slide và bài lab 1–8 do sinh viên cung cấp trong cuộc trò chuyện.
