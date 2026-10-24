# Hệ thống log tập trung Loki + Promtail

## 1. Mục đích

Triển khai thu thập, lưu trữ và truy vấn log theo chương 8 và bài lab 8 đã cung cấp. Hệ thống phục vụ riêng project đề 28, không dùng log Lab 7–8 làm minh chứng. Tất cả cấu hình ở `C:\DTC245200404`, tương ứng `/mnt/c/DTC245200404` trong Ubuntu.

Luồng xử lý:

```text
stdout/stderr container đề 28 -> Promtail -> Loki -> Grafana Explore (LogQL)
```

Promtail phát hiện container qua Docker socket và lọc nhãn Compose project `dtc245200404-de28` trước khi gửi log. Loki lưu log vào volume riêng; Grafana sử dụng datasource **Loki De 28** để truy vấn. Không tải image mới vì Loki và Promtail đã có sẵn trên máy.

## 2. Các file và dịch vụ

| Thành phần | File | Vai trò |
|---|---|---|
| Loki | `logging/loki.yml` | Lưu log theo schema v13/TSDB, filesystem, một bản sao, retention 7 ngày |
| Promtail | `logging/promtail.yml` | Lọc project, gắn nhãn và gửi log về Loki |
| Grafana datasource | `monitoring/grafana/provisioning/datasources/loki.yml` | Tự nạp kết nối `http://loki:3100`, UID loki-de28 |
| Compose | `docker-compose.yml` | Hai dịch vụ mới, volume loki-data và promtail-positions |

Loki cục bộ: `http://localhost:3101`. Cổng 3100 của Lab 8 không bị thay đổi. Promtail không publish cổng ra host. Loki và Promtail chỉ tham gia monitor_net, không cần kết nối vào mạng cơ sở dữ liệu.

Nhãn truy vấn: `project`, `service`, `container`, `stream`, `job`. `service` là tên dịch vụ Compose như nginx, app, db. Positions được lưu riêng để theo dõi vị trí đọc khi khởi động lại.

Promtail cần truy cập Docker socket để đọc log. Mount `:ro` không biến Docker API thành API chỉ đọc; đây là quyền kỹ thuật của bộ thu log theo mô hình lab, không cấp cho ứng dụng web. Loki không bật xác thực trong mô hình thực hành và chỉ publish trên loopback.

## 3. Lệnh triển khai đã thực hiện

```bash
cd /mnt/c/DTC245200404
docker compose config --quiet
docker compose run --rm --no-deps loki -config.file=/etc/loki/config.yml -verify-config=true
docker compose up -d --no-build --pull never loki promtail
docker compose restart grafana
```

Grafana cần khởi động lại để nạp datasource từ file provisioning. Không chạy `docker compose down -v`, vì sẽ xóa volume dữ liệu.

## 4. Ba truy vấn LogQL đã kiểm chứng

### Truy vấn 1 — Log toàn project đề 28

```logql
{project="dtc245200404-de28"}
```

Chọn toàn bộ log đã được Promtail gắn nhãn project đề 28, từ nhiều dịch vụ.

### Truy vấn 2 — Lọc yêu cầu kiểm tra sức khỏe qua Nginx

```logql
{project="dtc245200404-de28",service="nginx"} |= "GET /health"
```

Chọn log Nginx rồi giữ các dòng chứa chuỗi GET /health. Đây là log truy cập thật, có thể bao gồm healthcheck định kỳ; không coi mọi dòng là thao tác của người dùng.

### Truy vấn 3 — Log riêng ứng dụng Flask/Gunicorn

```logql
{project="dtc245200404-de28",service="app"}
```

Chỉ xem log của dịch vụ app; có thể đối chiếu với log Nginx để theo dõi luồng yêu cầu.

Không nhập LogQL vào datasource Prometheus. Nếu không thấy log, chọn đúng **Loki De 28**, chế độ **Code**, khoảng **Last 1 hour**, rồi Run query. Khi xem lại vào ngày khác, chọn khoảng chứa thời điểm có log hoặc mở lại website để phát sinh GET mới, không cần sửa dữ liệu nghiệp vụ.

## 5. Kết quả kiểm chứng ngày 25/10/2026 (UTC+7)

- Cấu hình Compose hợp lệ; Loki báo config is valid.
- Endpoint `/ready` của Loki trả HTTP 200 với nội dung `ready` sau giai đoạn khởi động.
- Loki và Promtail đã chạy; Promtail phát hiện container project đề 28.
- Ba truy vấn LogQL đều trả log thật. Với giới hạn kiểm tra 20 dòng, mỗi truy vấn trả 20 dòng; đây là giới hạn truy vấn, không phải tổng số log của hệ thống.
- Truy vấn toàn project trả nhiều stream; truy vấn Nginx và app trả stream tương ứng với nhãn service đúng.
- Datasource Loki trong Grafana báo `status=OK`, `Data source successfully connected`.
- Các GET chỉ đọc tới trang tổng quan, /health và /lich-hen đều trả HTTP 200 trong bước kiểm chứng.
- Kiểm tra SELECT cuối: customers=1, pets=1, services=1, appointments=1. Prometheus vẫn có bốn Targets UP và các panel tiếp tục có dữ liệu.
- Không tạo lỗi giả hoặc ghi dữ liệu nghiệp vụ để sinh log. Minh chứng là log hoạt động, không tuyên bố đã mô phỏng sự cố hoặc cảnh báo.
- Chưa có ảnh nào của phần này được sinh viên xác nhận đã chụp.

## 6. Từng ảnh sinh viên tự chụp

### Hình 19 — Dịch vụ log đang chạy

Trong terminal Ubuntu:

```bash
cd /mnt/c/DTC245200404
docker compose ps loki promtail
curl http://localhost:3101/ready
```

Chờ Loki trả `ready` rồi chụp tên dịch vụ, trạng thái và phản hồi. Nếu mới khởi động, có thể cần đợi vài chục giây.

Chú thích: **Hình 19. Trạng thái Loki, Promtail và kiểm tra sẵn sàng của Loki.**

### Hình 20 — Kết nối datasource Loki

Mở Grafana `http://localhost:3001`. Vào **Connections → Data sources → Loki De 28**, kéo xuống bấm **Save & test** nếu có. Chụp tên datasource, URL nội bộ và thông báo kết nối thành công. Không chụp mật khẩu đăng nhập.

Chú thích: **Hình 20. Grafana kết nối thành công tới datasource Loki của đề 28.**

### Hình 21, 22, 23 — Ba truy vấn LogQL

1. Vào **Explore**, chọn datasource **Loki De 28**.
2. Chọn **Code** để nhập LogQL trực tiếp.
3. Chọn **Last 1 hour**.
4. Nhập truy vấn 1 ở mục 4 và bấm **Run query**.
5. Chụp cả câu truy vấn và những dòng log trả về. Có thể mở rộng một dòng để thấy nhãn project/service.
6. Lặp lại cho truy vấn 2 và 3, mỗi truy vấn một ảnh.

Chú thích:

- **Hình 21. Truy vấn log tập trung của project đề 28 bằng LogQL.**
- **Hình 22. Lọc log yêu cầu GET /health của Nginx.**
- **Hình 23. Truy vấn log của dịch vụ ứng dụng Flask/Gunicorn.**

Không dùng ảnh chỉ có câu truy vấn mà chưa có kết quả làm minh chứng truy vấn thành công. Không tự chụp hay tạo ảnh thay cho sinh viên.

## 7. Nội dung đưa vào báo cáo

> Hệ thống bổ sung Loki và Promtail để quản lý log tập trung. Promtail phát hiện container qua Docker và chỉ thu log thuộc project dtc245200404-de28. Mỗi dòng log được gắn các nhãn như project, service, container và stream trước khi gửi đến Loki. Loki lưu dữ liệu trong volume riêng, còn Grafana Explore hỗ trợ tìm kiếm bằng LogQL.

> Sinh viên thực hiện ba truy vấn: xem log toàn project, lọc log GET /health của Nginx và xem log riêng của ứng dụng. Kết quả kiểm chứng trả về các dòng log thực tế và datasource Loki kết nối thành công. Các yêu cầu GET dùng trong kiểm tra chỉ đọc dữ liệu; không thêm, sửa hoặc xóa bản ghi nghiệp vụ.

Chèn các ảnh thật tương ứng sau từng đoạn. Phần này đáp ứng nội dung log tập trung và ba truy vấn cơ bản; chưa triển khai Alertmanager cho riêng đề 28 và không coi đó là kết quả đã đạt.
