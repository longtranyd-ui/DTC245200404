# Tích hợp Prometheus và Grafana — Đề 28

## Mục đích và phạm vi

Áp dụng mô hình thu thập metrics và dashboard trong chương 7/bài lab 7 vào ứng dụng đề 28. Giám sát đủ container, web server Nginx và PostgreSQL theo yêu cầu chung của đề tài. Vì đề 28 dùng PostgreSQL, exporter DB tương ứng được dùng thay cho MySQL exporter trong ví dụ lab.

Mọi cấu hình được lưu tại `C:\DTC245200404` (`/mnt/c/DTC245200404` trong Ubuntu). Không sửa stack Lab 7–8. Không thêm, sửa hoặc xóa dữ liệu nghiệp vụ. Có bổ sung tài khoản kỹ thuật chỉ đọc thống kê PostgreSQL và tài khoản quản trị Grafana; thông tin bí mật chỉ lưu trong `.env`, không commit.

## Kiến trúc dễ hiểu

```text
cAdvisor -----------> metrics container ----+
Nginx -> exporter --> metrics web ----------+--> Prometheus --> Grafana
PostgreSQL -> exporter -> metrics DB -------+
```

Prometheus chủ động kéo metrics mỗi 15 giây. Grafana truy vấn Prometheus để vẽ biểu đồ. Exporter là dịch vụ chuyển thông tin thống kê thành định dạng Prometheus đọc được.

| Thành phần | Vai trò | Địa chỉ |
|---|---|---|
| Prometheus | Thu thập và lưu metrics 7 ngày | http://localhost:9091 |
| Grafana | Dashboard đề 28 | http://localhost:3001/d/de28-overview |
| cAdvisor | CPU/RAM các container | Chỉ trong mạng Docker |
| Nginx exporter | Đọc stub_status của Nginx | Chỉ trong mạng Docker |
| PostgreSQL exporter | Đọc thống kê bằng vai trò pg_monitor | Chỉ trong mạng Docker |

Prometheus không tham gia mạng DB. PostgreSQL exporter nối `db_net` và `monitor_net`. Nginx exporter nối `web_net` và `monitor_net`. Cổng thống kê Nginx 8081 chỉ mở bên trong Docker, không publish ra host. Cổng 9090 và 3000 của Lab 7–8 giữ nguyên.

cAdvisor dùng quyền đặc biệt và mount chỉ đọc các thư mục hệ thống theo mô hình bài lab. Nó nhìn thấy thông tin container của Docker host; cấu hình Prometheus chỉ giữ metrics container có nhãn project `dtc245200404-de28`. Đây không phải quyền dành cho ứng dụng web.

## File cấu hình

- `docker-compose.yml`: bổ sung năm dịch vụ giám sát và hai volume lưu metrics/cấu hình Grafana.
- `monitoring/prometheus.yml`: bốn job prometheus, cadvisor, nginx, postgres.
- `monitoring/grafana/provisioning`: tự nạp datasource và dashboard từ file.
- `monitoring/grafana/dashboards/de28.json`: tám biểu đồ/trạng thái, không tải dashboard mẫu bên ngoài.
- `monitoring/setup-monitor-user.sh`: tạo tài khoản kỹ thuật nếu chưa có, cấp pg_monitor và CONNECT; không cấp SELECT dữ liệu nghiệp vụ hoặc quyền ghi.
- `.env.example`: tên biến cần điền; `.env` thật không đưa vào Git.

Không sửa tay dashboard rồi coi là đã lưu vào Git. Nguồn cấu hình dashboard là file JSON trong repository.

## Các lệnh cấu hình đã thực hiện

```bash
cd /mnt/c/DTC245200404
docker compose config --quiet
bash monitoring/setup-monitor-user.sh
docker compose exec nginx nginx -t
docker compose exec nginx nginx -s reload
docker compose run --rm --no-deps --entrypoint promtool prometheus check config /etc/prometheus/prometheus.yml
docker compose up -d --no-build --pull never prometheus grafana cadvisor nginx-exporter postgres-exporter
```

Hai image exporter cần thiết đã được tải. Các image Prometheus, Grafana và cAdvisor có sẵn. Lệnh trên là nhật ký thao tác cho môi trường hiện tại, không phải yêu cầu chạy lại để tạo ảnh. Không chạy `down -v` vì sẽ xóa volume.

## Đọc dashboard

1. **Nguồn giám sát UP:** bốn job có giá trị 1 là scrape thành công; cần xem thêm pg_up/nginx_up để xác nhận backend.
2. **PostgreSQL sẵn sàng:** pg_up=1 cho biết exporter kết nối DB được.
3. **CPU từng container:** phần trăm một lõi CPU theo tốc độ tăng bộ đếm; có thể lớn hơn 100% nếu dùng nhiều lõi.
4. **RAM từng container:** working set theo byte, hiển thị đơn vị dung lượng.
5. **Nginx yêu cầu/giây:** tốc độ yêu cầu, gồm cả truy cập kiểm tra health.
6. **Nginx kết nối đang mở:** số kết nối hiện tại.
7. **PostgreSQL kết nối petshop:** số backend kết nối tới DB.
8. **PostgreSQL giao dịch/giây:** tốc độ commit và rollback, bao gồm hoạt động giám sát.

Các biểu đồ rate cần ít nhất hai lần scrape; lúc vừa khởi động nên chờ khoảng 1 phút. Giá trị CPU thấp khi ít thao tác là bình thường; không tạo số liệu giả hoặc ghi thêm nghiệp vụ để tăng biểu đồ.

## Hướng dẫn tự chụp ảnh

Không có ảnh nào được hệ thống tự chụp. Số hình dưới đây nối tiếp phần Nginx; sinh viên điều chỉnh số nếu bố cục báo cáo khác.

### Hình 14 — Các container giám sát

Mở terminal Ubuntu:

```bash
cd /mnt/c/DTC245200404
docker compose ps
```

Kéo rộng cửa sổ, chụp bảng có các dịch vụ đề 28. Chú thích: **Hình 14. Các dịch vụ ứng dụng và giám sát được triển khai bằng Docker Compose.**

### Hình 15 — Prometheus Targets

Mở `http://localhost:9091/targets`. Chờ bốn job prometheus, cadvisor, nginx, postgres đều UP rồi tự chụp. Nếu một job DOWN, báo lỗi để xử lý trước khi ghi thành công.

Chú thích: **Hình 15. Prometheus thu thập metrics từ bốn nguồn giám sát của đề 28.**

### Hình 16 — Truy vấn PromQL

Mở `http://localhost:9091/query`, nhập `up`, bấm Execute, chọn dạng bảng nếu cần. Chụp truy vấn và bốn kết quả bằng 1.

Chú thích: **Hình 16. Truy vấn PromQL kiểm tra trạng thái các nguồn giám sát.**

### Hình 17 — Dashboard container

Mở `http://localhost:3001`, đăng nhập bằng tài khoản `GRAFANA_ADMIN_USER` và mật khẩu `GRAFANA_ADMIN_PASSWORD` trong `.env` cục bộ. Không chụp file `.env` hoặc mật khẩu.

Vào **Dashboards → De 28 → De 28 - Container, Nginx va PostgreSQL**, hoặc mở thẳng `http://localhost:3001/d/de28-overview` sau khi đăng nhập. Chọn Last 15 minutes, đợi dữ liệu rồi chụp phần trạng thái và CPU/RAM container.

Chú thích: **Hình 17. Dashboard Grafana hiển thị trạng thái nguồn giám sát và tài nguyên các container đề 28.**

### Hình 18 — Dashboard Nginx và PostgreSQL

Cuộn xuống, tự chụp bốn biểu đồ web và DB, giữ tên panel và trục đơn vị rõ ràng. Có thể chia hai hình nếu chữ quá nhỏ.

Chú thích: **Hình 18. Theo dõi yêu cầu Nginx, kết nối và giao dịch PostgreSQL trên Grafana.**

## Đoạn viết vào báo cáo

> Hệ thống bổ sung Prometheus, Grafana và các exporter để giám sát ba lớp container, web server và cơ sở dữ liệu. Prometheus kéo metrics theo chu kỳ 15 giây từ cAdvisor, Nginx exporter, PostgreSQL exporter và chính Prometheus. Grafana được cấu hình datasource Prometheus và tự nạp dashboard từ các file được quản lý trên GitHub.

> cAdvisor cung cấp CPU và RAM container, Nginx exporter cung cấp số yêu cầu và kết nối web, PostgreSQL exporter cung cấp trạng thái và thống kê cơ sở dữ liệu. Tài khoản giám sát PostgreSQL có vai trò pg_monitor, không dùng tài khoản superuser của ứng dụng để thu thập metrics. Dịch vụ DB vẫn nằm trong mạng nội bộ, các exporter không công bố cổng ra máy host.

## Kết quả đã kiểm chứng

- Cấu hình Prometheus qua promtool hợp lệ; cấu hình Nginx kiểm tra thành công.
- Bốn Targets cadvisor, nginx, postgres và prometheus đều UP; truy vấn up trả bốn giá trị 1.
- pg_up=1; các truy vấn CPU và RAM trả dữ liệu cho chín dịch vụ của project đề 28.
- Tám truy vấn của dashboard đều trả chuỗi số liệu, bao gồm tốc độ yêu cầu Nginx và tốc độ giao dịch PostgreSQL.
- API Grafana báo database=ok; datasource health=OK; dashboard de28-overview được provision thành công.
- Website /health vẫn trả database=connected và status=ok sau tích hợp.
- Kiểm tra cuối: customers=1, pets=1, services=1, appointments=1. Không thay đổi dữ liệu nghiệp vụ.
- Chưa có ảnh giám sát nào được sinh viên xác nhận đã chụp. Chưa đánh giá hình thức biểu đồ bằng ảnh chụp; kết quả trên dựa trên API, cấu hình và truy vấn thực tế.

Đoạn kết quả có thể viết:

> Kiểm tra cho thấy bốn nguồn giám sát đều có trạng thái UP. Dashboard được nạp tự động và cả tám truy vấn đều có dữ liệu, bao gồm CPU/RAM container, hoạt động Nginx và thống kê PostgreSQL. Website vẫn kết nối cơ sở dữ liệu thành công; dữ liệu nghiệp vụ được giữ nguyên sau khi bổ sung giám sát.

Chèn ảnh thật do sinh viên chụp. Ảnh giám sát chưa thay thế minh chứng log Loki/Promtail.
