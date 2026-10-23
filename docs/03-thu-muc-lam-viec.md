# Thống nhất thư mục làm việc

Theo yêu cầu sinh viên, từ bước này toàn bộ mã nguồn, checkout Git, cấu hình, hướng dẫn và các tệp báo cáo được làm việc tại `C:\DTC245200404`.

Trong Ubuntu WSL2, cùng thư mục này có đường dẫn `/mnt/c/DTC245200404`. Đây là hai cách truy cập cùng một thư mục, không phải hai bản mã nguồn.

## Cách mở dự án

Trong PowerShell:

```powershell
cd C:\DTC245200404
git status
```

Trong Ubuntu:

```bash
cd /mnt/c/DTC245200404
docker compose ps
curl http://localhost:8088/health
```

Không tiếp tục chỉnh sửa ở checkout cũ `tmp/github-readme-push` hoặc thư mục triển khai cũ `~/de-tai-28`. Các tài liệu ở bước trước có nhắc đường dẫn cũ phải sử dụng đường dẫn mới ở trên.

## Kết quả kiểm chứng ngày 23/10/2026

- Đã chuyển checkout Git và mã nguồn về thư mục gốc yêu cầu; mã nguồn được đối chiếu khớp với bản triển khai trước khi chuyển.
- Compose được chạy lại từ `/mnt/c/DTC245200404`, dùng image sẵn có và volume dữ liệu hiện có.
- Container app và db healthy; pgAdmin đang chạy và endpoint `/misc/ping` trả PING.
- `/health` trả `database=connected`, `status=ok`.
- Truy vấn chỉ đọc sau chuyển đổi: customers=1, pets=1, services=1, appointments=1. Không thêm, sửa hoặc xóa dữ liệu nghiệp vụ.
- File `.env` được giữ cục bộ và bị Git bỏ qua. Tệp tạm trong `tmp/` không được đưa lên GitHub.

Dữ liệu PostgreSQL và pgAdmin vẫn nằm trong Docker named volumes do Docker quản lý. Thư mục làm việc của dự án không phải thư mục lưu trữ vật lý của Docker; không di chuyển volume vì cần bảo toàn dữ liệu hiện có.

## Viết vào báo cáo

> Mã nguồn, cấu hình Docker Compose và tài liệu thực hành được quản lý tập trung tại C:\DTC245200404. Ubuntu WSL2 truy cập cùng thư mục qua /mnt/c/DTC245200404. Sau khi thống nhất đường dẫn, các dịch vụ hoạt động và ứng dụng vẫn kết nối được PostgreSQL. Bốn bảng nghiệp vụ giữ nguyên số lượng một bản ghi mỗi bảng.

Không cần chụp ảnh bổ sung ở bước chuyển thư mục. Các lệnh chụp minh chứng tiếp theo dùng đường dẫn mới.
