# Đối chiếu tiêu chí đề 28 — 25/10/2026

## Kết luận

Hệ thống kỹ thuật hiện chạy và các kiểm tra Nginx, metrics, log, hardening đạt. Chưa thể kết luận đủ toàn bộ điều kiện nộp bài vì README rỗng, chưa có báo cáo tổng hợp tối thiểu 10 trang được kiểm tra và chưa xác nhận đủ ảnh/demo. Không tự chấm điểm thay giảng viên.

Căn cứ: tài liệu đề tài K23 trang 1–2 (yêu cầu chung, thang điểm) và trang 8 (đề 28). Đã đọc lại các trang này khi kiểm tra.

## Bảng đối chiếu

| Tiêu chí | Điểm | Trạng thái và bằng chứng |
|---|---:|---|
| GitHub | 1,5 | Source/cấu hình được theo dõi, GitHub main khớp commit 0a50647 tại thời điểm kiểm tra. Có ba mốc riêng Nginx b8b41dd, giám sát 00d2d32, log e01441b. **Thiếu README hướng dẫn chạy: README hiện 0 byte.** |
| Ứng dụng + DB | 1,5 | Bốn nhóm chức năng có mã nguồn, website và /health hoạt động. PostgreSQL/pgAdmin chạy; người dùng đã cung cấp ảnh truy vấn appointments và dashboard pgAdmin. Lần rà soát này chỉ đọc, không kiểm thử lại thao tác thêm/sửa/xóa. |
| Nginx | 1,5 | Reverse proxy hoạt động, có security headers; /health 200, đường dẫn tệp ẩn 403, đường dẫn không tồn tại 404. Chưa có HTTPS nhưng đề cho phép HTTPS **hoặc** security headers. |
| Prometheus + Grafana | 1,5 | Bốn Targets UP; tám truy vấn panel có dữ liệu, bao gồm container, Nginx và PostgreSQL. Datasource/dashboard Grafana hoạt động. |
| Loki + Promtail | 1,5 | Loki ready; ba truy vấn LogQL trả log thật; datasource Loki trong Grafana OK. |
| Hardening | 1,5 | Script kiểm chứng PASS: non-root app, read-only, giới hạn quyền, tách mạng, quyền DB, bí mật và headers; vượt số lượng 3–4 biện pháp yêu cầu. |
| Tổng thể / trình bày | 1,0 | 11 dịch vụ đề 28 chạy bằng Compose. **Chưa xác nhận đủ ảnh minh chứng, demo toàn bộ và khả năng giải thích của sinh viên.** |

## Các yêu cầu nộp bài còn cần hoàn thiện

1. **README hướng dẫn chạy:** hiện rỗng theo yêu cầu trước của sinh viên. Các hướng dẫn rời trong docs không thay thế README mà đề đòi hỏi. Cần hướng dẫn môi trường, .env không có mật khẩu thật, build/start, tạo role giám sát cho môi trường mới, URL và các bước kiểm tra. Chưa thử tái triển khai trên môi trường sạch; không xóa volume hiện tại để thử.
2. **Báo cáo tối thiểu 10 trang:** hiện có các file Markdown hướng dẫn, chưa tìm thấy bản báo cáo tổng hợp DOCX/PDF trong workspace để kiểm tra số trang, bìa và hình minh họa. Báo cáo có thể đang được sinh viên soạn ngoài workspace; chưa có căn cứ đánh giá bản đó. Cần bìa thông tin thật, cấu trúc/cách hoạt động và kết quả sáu nội dung kỹ thuật.
3. **Ảnh minh chứng:** đã nhận hai ảnh pgAdmin trong chat. Chưa xác nhận đủ ảnh Docker, website, Nginx, Targets, Grafana, ba LogQL, hardening và GitHub. Không tự chụp hoặc tạo ảnh thay sinh viên.
4. **Demo và giải thích:** cần thực hiện trình tự website -> DB tool -> Nginx -> Grafana -> LogQL -> hardening và giải thích ý nghĩa kết quả. Kiểm tra API không thay thế phần trình bày của sinh viên.
5. **Tên tài khoản:** PDF viết tạo tài khoản và đặt tên theo mã SV. Tài khoản hiện là longtranyd-ui, repository là DTC245200404. Chưa thể xác nhận cách đặt tên này được giảng viên chấp nhận. Không tự đổi tên tài khoản, repository hoặc remote; sinh viên cần đối chiếu yêu cầu đặt tên với giảng viên.

Đề không yêu cầu riêng CI/CD, Alertmanager, chứng chỉ công khai hay tên miền trả phí cho phần yêu cầu chung. Không coi chúng là phần thiếu bắt buộc của đề 28.

## Bằng chứng kiểm tra trực tiếp

- `scripts/check-hardening.py`: RESULT PASS; mỗi bảng nghiệp vụ một bản ghi, không thay đổi dữ liệu.
- Prometheus: cadvisor/nginx/postgres/prometheus UP; dashboard có 11 chuỗi CPU/RAM tương ứng các dịch vụ hiện tại và dữ liệu web/DB.
- LogQL: ba truy vấn trong tài liệu phần log đều trả kết quả; giới hạn 20 dòng mỗi truy vấn trong phép kiểm tra, không phải tổng số log.
- pgAdmin /misc/ping trả PING; Loki /ready trả ready.
- Git working tree sạch trước khi tạo biên bản này; không phát hiện tệp báo cáo DOCX/PDF hoặc ảnh được lưu trong workspace tại lần kiểm tra.

## Hướng xử lý tiếp theo

Hoàn thiện README theo phạm vi được sinh viên cho phép, tập hợp bản báo cáo và ảnh thật để đối chiếu từng mục, kiểm tra bìa/số trang, rồi tập demo. Chỉ đánh dấu hoàn tất hồ sơ khi các phần này đã có và được kiểm tra.
