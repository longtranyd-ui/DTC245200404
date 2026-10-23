# Nhiệm vụ 1 — Chuẩn bị báo cáo thực hành đề 28

## 1. Mục đích và căn cứ

Đề 28 triển khai website quản lý cửa hàng thú cưng với bốn nhóm chức năng: khách hàng, thú cưng, dịch vụ spa và lịch hẹn. Cơ sở dữ liệu là PostgreSQL, công cụ quản trị là pgAdmin. Căn cứ: tài liệu đề tài trang 1–2 và trang 8, cùng giáo trình và các bài lab sinh viên đã cung cấp. Không sử dụng dữ liệu nghiệp vụ từ nguồn bên ngoài.

## 2. Quy tắc thực hành

- Sinh viên đã xác nhận giữ nguyên dữ liệu hiện có và chỉ đọc. Không thực hiện thêm, sửa, xóa để thử chức năng khi chưa được phép.
- Không tự chụp ảnh. Đến mốc minh chứng thì mở màn hình để sinh viên tự chụp.
- Không ghi đã có ảnh, đã demo hoặc đạt tiêu chí nếu chưa có bằng chứng.
- Mỗi nhiệm vụ hoàn thành có commit và push GitHub. Ba mốc kỹ thuật riêng là Nginx, giám sát và log theo đề.
- Khi phát sinh yêu cầu mới hoặc cần thay đổi dữ liệu, thông báo cho sinh viên trước.

## 3. Hiện trạng kiểm tra ngày 23/10/2026

Repository: https://github.com/longtranyd-ui/DTC245200404

Mã nguồn hiện có dùng Python/Flask; không cần chọn lại ngôn ngữ. Hệ thống đang chạy trong Ubuntu WSL2 tại `~/de-tai-28`. Checkout Git dùng để chuẩn bị và push nằm trên Windows; thư mục chạy trong Ubuntu hiện không phải checkout Git. Không sao chép đè hoặc tạo lại cơ sở dữ liệu.

Kết quả kiểm tra trực tiếp:

- `docker compose ps`: app và db healthy, pgadmin đang chạy.
- `http://localhost:8088/health`: trả `database=connected`, `status=ok`.
- Truy vấn SELECT: customers=1, pets=1, services=1, appointments=1.
- Chưa xác minh trong nhiệm vụ này: đăng nhập pgAdmin và thực hiện truy vấn bằng giao diện; thao tác thêm/sửa/xóa; Nginx, giám sát và log của riêng đề 28.

Các ghi chép kiểm thử trước đây trong `02a` và `02b` là hồ sơ cũ, không thay thế kiểm chứng hiện tại. Không dùng kết quả của stack Lab 7–8 khác làm minh chứng cho đề 28.

## 4. Bảng theo dõi đủ 10 điểm

| Tiêu chí | Điểm | Công việc / minh chứng cần hoàn thiện |
|---|---:|---|
| GitHub | 1,5 | Source và cấu hình đầy đủ; README hướng dẫn chạy; ít nhất ba commit có ý nghĩa. README hiện rỗng, sẽ bổ sung khi có quy trình chạy được kiểm chứng. |
| Ứng dụng + DB | 1,5 | Website hoạt động, kết nối PostgreSQL; đăng nhập pgAdmin và xem dữ liệu. Chụp giao diện bốn chức năng và kết quả truy vấn. |
| Nginx | 1,5 | Website đi qua reverse proxy; HTTPS tự ký hoặc security headers; commit riêng. |
| Giám sát | 1,5 | Prometheus thu metrics; Grafana có dữ liệu container, web và DB; commit riêng. |
| Log | 1,5 | Loki + Promtail thu log đề 28; ba truy vấn LogQL có kết quả; commit riêng. |
| Hardening | 1,5 | Kiểm chứng tối thiểu bốn biện pháp: non-root ứng dụng, mạng DB nội bộ, quyền DB tối thiểu, security headers. Kiểm tra thêm cách lưu bí mật. |
| Tổng thể / trình bày | 1,0 | Chạy bằng Compose, demo đủ thành phần, ảnh thật do sinh viên chụp, giải thích được kết quả. |

Báo cáo tối thiểu 10 trang là yêu cầu bắt buộc dù không có dòng điểm riêng.

## 5. Hướng dẫn viết phần đầu báo cáo ngay bây giờ

Tạo tài liệu báo cáo của bạn và đặt tên: **Báo cáo thực hành — Đề 28: Hệ thống Quản lý Cửa hàng Thú cưng**.

**Bìa:** điền thông tin thật của trường, khoa, học phần, giảng viên, họ tên, mã sinh viên, lớp và thời gian. Chưa biết thông tin nào thì để chỗ trống, không tự điền dữ liệu giả.

**Mục Giới thiệu đề tài**, có thể viết:

> Đề tài xây dựng và triển khai website quản lý cửa hàng thú cưng, gồm quản lý khách hàng, thú cưng, dịch vụ spa và lịch hẹn. Ứng dụng hiện có sử dụng Python/Flask, PostgreSQL lưu trữ dữ liệu và pgAdmin hỗ trợ quản trị cơ sở dữ liệu. Các dịch vụ được tổ chức bằng Docker Compose. Phần thực hành tiếp tục cấu hình Nginx reverse proxy, giám sát bằng Prometheus và Grafana, thu thập log bằng Loki và Promtail, đồng thời kiểm chứng các biện pháp củng cố bảo mật theo yêu cầu học phần.

**Mục Môi trường thực hành**, có thể viết:

> Hệ thống được thực hành trên Windows với Ubuntu WSL2. Trong Ubuntu, thư mục triển khai là ~/de-tai-28. Ở bước kiểm tra ban đầu, Docker Compose có ba dịch vụ app, db và pgadmin. Hai dịch vụ app và db báo healthy. Endpoint /health cho biết ứng dụng kết nối cơ sở dữ liệu thành công. Truy vấn đếm ghi nhận mỗi bảng nghiệp vụ có một bản ghi; dữ liệu được giữ nguyên trong bước này.

Không ghi các thành phần dự kiến như Nginx, Grafana hoặc Loki là đã hoàn thành.

## 6. Mốc tự chụp ảnh đầu tiên

1. Mở `http://localhost:8088`: tự chụp trang tổng quan. Chú thích: **Hình 1. Giao diện tổng quan ứng dụng quản lý cửa hàng thú cưng ở bước kiểm tra ban đầu.**
2. Mở `http://localhost:8088/lich-hen`: tự chụp dữ liệu hiện có. Chú thích: **Hình 2. Danh sách lịch hẹn đang lưu trong hệ thống.**

Mỗi hình cần một đoạn giải thích bạn đang quan sát điều gì. Hai ảnh này chưa chứng minh đã kiểm thử thêm/sửa/xóa hoặc đăng nhập DB thành công. Chưa có ảnh nào được xác nhận đã chụp.

Nhiệm vụ kế tiếp: kiểm chứng PostgreSQL qua giao diện pgAdmin, sau đó triển khai Nginx theo bài lab 1 và yêu cầu chung. Không thay đổi dữ liệu nghiệp vụ.
