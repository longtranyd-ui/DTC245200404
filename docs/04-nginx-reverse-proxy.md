# Nhiệm vụ Nginx Reverse Proxy và bảo mật cơ bản

## 1. Mục đích

Đưa website đề 28 ra sau Nginx, theo chương 1, bài lab Nginx và yêu cầu chung trang 1–2 của tài liệu đề tài. Tiêu chí cho phép HTTPS tự ký **hoặc** security headers cơ bản. Bước này sử dụng HTTP với security headers; chưa cấu hình HTTPS, chưa có mã hóa TLS.

Toàn bộ thao tác từ `C:\DTC245200404`, tương ứng `/mnt/c/DTC245200404` trong Ubuntu. Không thay đổi dữ liệu nghiệp vụ hoặc stack Lab 7–8.

## 2. Luồng hoạt động

```text
Trình duyệt -> localhost:8088 -> Nginx:8080 -> app:8000 -> PostgreSQL:5432
```

Trước bước này, cổng 8088 chuyển trực tiếp vào ứng dụng Flask. Sau bước này, cổng 8088 chuyển vào Nginx. Nginx dùng `proxy_pass http://app:8000` để chuyển yêu cầu cho ứng dụng qua mạng Docker `web_net`. Ứng dụng kết nối PostgreSQL qua `db_net` như trước. Nginx không tham gia mạng DB. pgAdmin vẫn tại `http://localhost:8089`.

Địa chỉ web không đổi nên ảnh giao diện đơn thuần không chứng minh đã có reverse proxy. Cần ảnh cấu hình, trạng thái dịch vụ và HTTP headers.

## 3. Các file và cấu hình

- `docker-compose.yml`: thêm dịch vụ nginx; bỏ ánh xạ cổng trực tiếp của app; công bố `127.0.0.1:8088:8080` ở nginx. DB và volume được giữ nguyên.
- `nginx/default.conf`: khai báo server, proxy và security headers. File được mount chỉ đọc vào container.
- Image: `nginx:stable-alpine` chính thức. Image đã được tải để triển khai.

| Cấu hình | Ý nghĩa |
|---|---|
| `listen 8080` | Nginx nhận yêu cầu ở cổng 8080 bên trong container |
| `proxy_pass http://app:8000` | Chuyển yêu cầu đến dịch vụ ứng dụng trong mạng Docker |
| `Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto` | Chuyển tiếp thông tin host, địa chỉ và giao thức đến backend; địa chỉ có thể là địa chỉ mạng Docker/WSL |
| `server_tokens off` | Không công bố phiên bản Nginx trong phản hồi |
| `client_max_body_size 64k` | Giới hạn kích thước nội dung yêu cầu ở mức phù hợp với ứng dụng |
| `proxy_hide_header` | Tránh lặp các security headers đã có từ Flask |
| `always` | Thêm security headers cả khi phản hồi có mã lỗi |

| Header | Vai trò |
|---|---|
| `X-Content-Type-Options: nosniff` | Yêu cầu trình duyệt không tự đoán loại nội dung |
| `X-Frame-Options: DENY` | Ngăn trang bị nhúng vào frame |
| `Referrer-Policy: same-origin` | Giới hạn thông tin referrer khi truy cập khác nguồn |
| `Content-Security-Policy` | Hạn chế nguồn tài nguyên, form và frame theo chính sách khai báo |

Các header này không mã hóa đường truyền. Website hiện chỉ công bố trên loopback máy thực hành, chưa triển khai công khai.

## 4. Kết quả kiểm chứng ngày 24/10/2026

- `docker compose config --quiet`: cấu hình Compose hợp lệ.
- `nginx -t`: `syntax is ok`, `test is successful`.
- App, DB và Nginx healthy; pgAdmin đang chạy.
- Trang `/`, `/khach-hang`, `/thu-cung`, `/dich-vu`, `/lich-hen` và `/static/style.css` trả HTTP 200 qua Nginx, kiểm tra từ cả Ubuntu và Windows.
- `/health`: HTTP 200, `database=connected`, `status=ok`.
- Phản hồi có `Server: nginx`, không chứa số phiên bản; có đủ bốn security headers.
- Đường dẫn không tồn tại trả HTTP 404 và vẫn có security header `X-Frame-Options: DENY`.
- Log truy cập Nginx ghi nhận các yêu cầu thực tế.
- Kiểm tra SELECT: customers=1, pets=1, services=1, appointments=1. Không thêm, sửa hoặc xóa dữ liệu.

## 5. Tự chụp minh chứng

Chưa có ảnh nào của bước Nginx được xác nhận đã chụp. Mở terminal Ubuntu, chạy từng nhóm dưới đây rồi tự chụp; không chụp file `.env`.

### Hình 10 — Cấu hình Reverse Proxy

```bash
cd /mnt/c/DTC245200404
cat nginx/default.conf
```

Kéo rộng terminal để đọc rõ `listen`, `proxy_pass`, các header và thông tin chuyển tiếp. Nếu không vừa, chia thành hai ảnh thay vì thu nhỏ chữ quá mức.

Chú thích: **Hình 10. Cấu hình Nginx reverse proxy và security headers cho ứng dụng đề 28.**

### Hình 11 — Cú pháp và dịch vụ

```bash
docker compose exec nginx nginx -t
docker compose ps
```

Ảnh cần thấy kiểm tra cú pháp thành công, bốn dịch vụ và ánh xạ cổng 8088 ở nginx. Dịch vụ app chỉ còn cổng nội bộ 8000/tcp.

Chú thích: **Hình 11. Kiểm tra cấu hình Nginx và trạng thái các dịch vụ Docker Compose.**

### Hình 12 — Phản hồi qua proxy và bảo mật

```bash
curl -i http://localhost:8088/health
```

Ảnh cần thấy HTTP 200, `Server: nginx`, bốn security headers và JSON kết nối DB. Dùng `-i` vì `-I` chỉ hiển thị header, không hiển thị nội dung JSON.

Chú thích: **Hình 12. Phản hồi HTTP qua Nginx có security headers và kết nối PostgreSQL thành công.**

### Hình 13 — Website sau Reverse Proxy

Mở `http://localhost:8088/`, tải lại trang và tự chụp giao diện. Giữ thanh địa chỉ và nội dung trang trong ảnh. Chụp sau bước kiểm tra header để liên hệ đúng với kết quả proxy.

Chú thích: **Hình 13. Website quản lý cửa hàng thú cưng được truy cập qua Nginx reverse proxy.**

## 6. Nội dung viết vào báo cáo

> Hệ thống bổ sung dịch vụ Nginx trong Docker Compose làm reverse proxy. Trình duyệt truy cập localhost:8088, yêu cầu được chuyển đến Nginx ở cổng nội bộ 8080, sau đó Nginx chuyển tiếp tới app:8000. Ứng dụng không còn công bố cổng trực tiếp ra host. Nginx chỉ tham gia mạng web_net, trong khi PostgreSQL được giữ trong mạng db_net nội bộ.

> Bước thực hành sử dụng security headers theo lựa chọn được cho phép trong đề bài. Nginx thiết lập X-Content-Type-Options, X-Frame-Options, Referrer-Policy và Content-Security-Policy; đồng thời ẩn số phiên bản Nginx. Chưa cấu hình HTTPS nên đường truyền tại bước này chưa có mã hóa TLS.

> Kiểm tra nginx -t thành công. Các trang chức năng và tài nguyên CSS trả HTTP 200 qua Nginx. Endpoint /health trả database=connected và status=ok. Phản hồi có các security headers đã cấu hình. Dữ liệu nghiệp vụ được giữ nguyên, mỗi bảng còn một bản ghi.

Sau từng đoạn, chèn ảnh thật tương ứng do sinh viên tự chụp. Không ghi đã chụp nếu chưa thực hiện. Nhiệm vụ này hoàn thành phần Nginx và security headers; chưa thay thế tiêu chí giám sát Prometheus/Grafana hoặc Loki/Promtail.
