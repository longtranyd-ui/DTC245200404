# Đề 28 — Quản lý Cửa hàng Thú cưng

Python (Flask), PostgreSQL và pgAdmin; triển khai bằng Docker Compose trên Ubuntu WSL2.

## Phạm vi hiện tại

Mã nguồn có bốn nhóm chức năng: khách hàng, thú cưng, dịch vụ spa và lịch hẹn. Đã kiểm chứng truy cập các trang, kết nối DB và phản hồi pgAdmin. Chưa kiểm chứng thao tác ghi dữ liệu vì đang chờ dữ liệu được sinh viên cho phép. Không có dữ liệu mẫu trong mã nguồn.

Nginx, giám sát và log riêng của đề 28 chưa được triển khai trong repository này.

## Chạy trên Ubuntu WSL2 đã có Docker và Compose

```bash
git clone https://github.com/longtranyd-ui/DTC245200404.git
cd DTC245200404
cp .env.example .env
nano .env
```

Điền mật khẩu PostgreSQL, mật khẩu tài khoản ứng dụng, SECRET_KEY, email và mật khẩu pgAdmin do bạn chọn. Không đưa `.env` lên GitHub. Tên DB và tên tài khoản PostgreSQL cần khớp cấu hình trong `pgadmin/servers.json` nếu thay đổi.

```bash
docker compose up -d --build
docker compose ps
curl http://localhost:8088/health
```

- Website: http://localhost:8088
- pgAdmin: http://localhost:8089 — đăng nhập bằng thông tin đã điền trong `.env`; kết nối server `De 28 - PostgreSQL` bằng mật khẩu PostgreSQL.
- Kết quả health đúng: `database: connected`, `status: ok`.

Đây là hướng dẫn cho lần dựng mới; chưa kiểm chứng dựng lại từ checkout sạch. Không chạy chồng lên stack đề 28 đang có. Không dùng `docker compose down -v` vì thao tác đó xóa volume dữ liệu. Thay mật khẩu trong `.env` không tự thay mật khẩu đã lưu trong volume PostgreSQL.

## Báo cáo

Xem [khung báo cáo](docs/huong-dan-bao-cao.md) và [kết quả kiểm tra bước 2A](docs/02a-kiem-chung-ung-dung.md). Ảnh minh chứng do sinh viên tự chụp. Không công khai mật khẩu trong ảnh hoặc báo cáo.
