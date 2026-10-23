# Bước 2A — Kiểm chứng ứng dụng và kết nối PostgreSQL

## Mục đích

Kiểm tra ba dịch vụ đề 28 hiện có trong `/home/longtranyd/de-tai-28` trên Ubuntu WSL2. Không thay đổi dữ liệu và không ảnh hưởng stack Lab 7–8.

## Kết quả đã kiểm chứng

- Ubuntu WSL2 có systemd, Docker Engine và Docker Compose hoạt động.
- `docker compose ps`: app và db running/healthy; pgadmin running.
- `GET /health`: HTTP 200, `database=connected`, `status=ok`.
- Trang tổng quan, khách hàng, thú cưng, dịch vụ và lịch hẹn: HTTP 200.
- pgAdmin `/misc/ping`: phản hồi `PING`.
- Cấu hình ứng dụng chạy UID/GID 10001, filesystem chỉ đọc, bỏ Linux capabilities; DB nằm trong mạng `internal` và không công bố cổng PostgreSQL ra host.

Các kết quả trên chưa chứng minh thêm/sửa/xóa hoạt động hoặc đăng nhập pgAdmin truy vấn DB thành công. Chưa đánh dấu hoàn thành toàn bộ nhiệm vụ ứng dụng + DB.

## Người mới thực hành kiểm tra

Trong terminal Ubuntu:

```bash
cd ~/de-tai-28
docker compose ps
curl http://localhost:8088/health
```

`ps` cho biết dịch vụ đang chạy; `health` kiểm tra ứng dụng thực sự kết nối DB. Mở http://localhost:8088 để xem bốn nhóm chức năng; mở http://localhost:8089 để vào pgAdmin.

## Phần viết vào báo cáo

“Hệ thống bước đầu gồm ba dịch vụ app, db và pgadmin được khai báo trong Docker Compose. Dịch vụ app sử dụng Python/Flask và kết nối PostgreSQL qua tên dịch vụ db trong mạng Docker. Công cụ pgAdmin phục vụ quản trị cơ sở dữ liệu. Kiểm tra endpoint /health cho kết quả database=connected và status=ok. Các trang quản lý khách hàng, thú cưng, dịch vụ spa và lịch hẹn truy cập thành công. Chưa kiểm chứng thao tác ghi dữ liệu tại bước này.”

## Ảnh sinh viên tự chụp

1. Trang tổng quan website: thấy tên đề tài và bốn nhóm chức năng. Chú thích: “Giao diện tổng quan hệ thống đề 28”.
2. Terminal `docker compose ps`: thấy ba dịch vụ đề 28 và trạng thái. Chú thích: “Trạng thái ba dịch vụ ứng dụng, PostgreSQL và pgAdmin”.

Ảnh pgAdmin kết nối DB và ảnh thao tác dữ liệu sẽ bổ sung sau khi thực hiện, không dùng màn hình đăng nhập làm bằng chứng kết nối DB. Chưa có ảnh nào được xác nhận đã chụp.

## Việc còn chờ

Sinh viên cung cấp hoặc tự nhập bộ dữ liệu được phép dùng để kiểm chứng thêm/sửa/xóa và quan hệ giữa các bảng. Không tự tạo bản ghi mẫu.
