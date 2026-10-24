# Đề 28 — Hệ thống Quản lý Cửa hàng Thú cưng

Website quản lý **khách hàng, thú cưng, dịch vụ spa và lịch hẹn**. Ứng dụng dùng Python/Flask, PostgreSQL và pgAdmin; triển khai bằng Docker Compose, có Nginx reverse proxy, Prometheus/Grafana, Loki/Promtail và các biện pháp hardening.

Repository: https://github.com/longtranyd-ui/DTC245200404

## 1. Môi trường và thư mục

- Môi trường thực hành hiện tại: Windows, Ubuntu WSL2, Docker Engine và Docker Compose plugin trong Ubuntu.
- Cần Git, Python 3 và Docker Compose hỗ trợ `up --wait`. Docker phải đang chạy và tài khoản Ubuntu có quyền sử dụng Docker.
- Cần Internet khi tải image và build ứng dụng lần đầu. Không tải dữ liệu nghiệp vụ hoặc dashboard mẫu từ bên ngoài.
- cAdvisor sử dụng các đường dẫn hệ thống Linux và Docker storage `overlay2` như bài lab. Không đổi storage driver hoặc cấu hình Docker host đang có chỉ để thử chạy dự án.
- Các lệnh Docker bên dưới chạy trong **terminal Ubuntu**, không chạy trực tiếp trong PowerShell.

Thư mục làm việc duy nhất trên máy thực hành:

```text
Windows: C:\DTC245200404
Ubuntu:  /mnt/c/DTC245200404
```

Đây là cùng một thư mục. Không tiếp tục dùng bản mã nguồn cũ tại `~/de-tai-28` hoặc `tmp/github-readme-push`.

Kiểm tra công cụ trong Ubuntu:

```bash
cd /mnt/c/DTC245200404
docker version
docker compose version
python3 --version
```

**Chỉ trên máy mới, khi chưa có thư mục dự án:** có thể lấy source bằng Git trong PowerShell:

```powershell
git clone https://github.com/longtranyd-ui/DTC245200404.git C:\DTC245200404
```

Máy thực hành đã có source thì bỏ qua bước clone; không clone đè lên thư mục hiện tại.

## 2. Khởi động lại hệ thống đã cấu hình

Nếu máy đã có `.env`, image, volume và role giám sát từ các bước thực hành trước, chạy:

```bash
cd /mnt/c/DTC245200404
docker compose config --quiet
docker compose up -d --no-build --pull never
docker compose ps
curl http://localhost:8088/health
```

`config --quiet` không in nội dung cấu hình chứa mật khẩu. Nếu chưa có image hoặc chưa cấu hình môi trường, thực hiện mục 3 trước. Việc khởi động lại giữ nguyên dữ liệu trong các named volume.

## 3. Cài đặt lần đầu trên môi trường mới

Không thực hiện lại bước tạo bí mật trên máy đang có dữ liệu. Thay mật khẩu trong `.env` không tự đổi mật khẩu đã lưu trong volume PostgreSQL, pgAdmin hoặc Grafana.

### 3.1. Chuẩn bị file .env

Tại thư mục dự án trong Ubuntu, chạy khối sau. Khối lệnh chỉ tạo `.env` nếu chưa tồn tại; mật khẩu ngẫu nhiên không được in ra terminal:

```bash
python3 - <<'PY'
from pathlib import Path
import secrets

target = Path('.env')
if target.exists():
    print('.env da ton tai: giu nguyen, khong ghi de.')
else:
    keys = {
        'POSTGRES_PASSWORD', 'APP_DB_PASSWORD', 'SECRET_KEY',
        'PGADMIN_DEFAULT_PASSWORD', 'MONITOR_DB_PASSWORD',
        'GRAFANA_ADMIN_PASSWORD',
    }
    lines = []
    for line in Path('.env.example').read_text().splitlines():
        key = line.split('=', 1)[0]
        lines.append(key + '=' + secrets.token_hex(24) if key in keys else line)
    with target.open('x', encoding='utf-8', newline='\n') as output:
        output.write('\n'.join(lines) + '\n')
    print('Da tao .env cuc bo voi cac bi mat rieng biet.')
PY
```

Giữ tên DB/user mặc định trong `.env.example` để khớp cấu hình pgAdmin và dashboard. Không commit, chụp ảnh hoặc đưa `.env` thật vào báo cáo. Muốn xem thông tin đăng nhập, chỉ mở file này cục bộ và đóng trước khi chụp minh chứng.

| Biến | Công dụng |
|---|---|
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | DB và tài khoản quản trị PostgreSQL |
| `APP_DB_USER`, `APP_DB_PASSWORD` | Tài khoản DB có quyền CRUD cho ứng dụng |
| `SECRET_KEY` | Khóa bảo vệ phiên Flask |
| `PGADMIN_DEFAULT_EMAIL`, `PGADMIN_DEFAULT_PASSWORD` | Đăng nhập giao diện pgAdmin |
| `MONITOR_DB_USER`, `MONITOR_DB_PASSWORD` | Tài khoản đọc thống kê cho PostgreSQL exporter |
| `GRAFANA_ADMIN_USER`, `GRAFANA_ADMIN_PASSWORD` | Đăng nhập Grafana |

### 3.2. Tải image và build ứng dụng

```bash
docker compose config --quiet
docker compose pull db pgadmin nginx prometheus grafana cadvisor nginx-exporter postgres-exporter loki promtail
docker compose build app
```

### 3.3. Khởi tạo PostgreSQL và tài khoản giám sát

```bash
docker compose up -d --wait db
bash monitoring/setup-monitor-user.sh
```

Khi volume PostgreSQL còn trống, các file trong `database/` tạo bốn bảng và tài khoản ứng dụng. Chúng **không chèn dữ liệu mẫu**. Script giám sát tạo role nếu chưa tồn tại, cấp `pg_monitor` và quyền kết nối; không sửa dữ liệu nghiệp vụ và không đổi mật khẩu role đã có.

Không xóa volume để ép chạy lại script khởi tạo. Nếu DB cũ thiếu cấu trúc/role, kiểm tra nguyên nhân trước khi thay đổi.

### 3.4. Khởi chạy toàn bộ dịch vụ

```bash
docker compose up -d --no-build --pull never
docker compose ps
```

Chờ khoảng một phút để Prometheus có ít nhất hai lần scrape và Loki hoàn tất khởi động. Grafana tự nạp datasource, dashboard từ file trong Git. Trên môi trường mới, website hiển thị danh sách trống là đúng; chỉ nhập dữ liệu đã được sinh viên cho phép.

## 4. Địa chỉ và cách đăng nhập

| Thành phần | Địa chỉ | Thông tin |
|---|---|---|
| Website qua Nginx | http://localhost:8088 | Bốn nhóm chức năng, không có trang đăng nhập riêng |
| Kiểm tra kết nối DB | http://localhost:8088/health | Mong đợi database=connected, status=ok |
| pgAdmin | http://localhost:8089 | Email/mật khẩu từ `PGADMIN_DEFAULT_*` |
| Prometheus Targets | http://localhost:9091/targets | Bốn job UP |
| Grafana | http://localhost:3001 | Tài khoản từ `GRAFANA_ADMIN_*` |
| Dashboard | http://localhost:3001/d/de28-overview | CPU/RAM container, Nginx và PostgreSQL |
| Grafana Explore | http://localhost:3001/explore | Chọn Loki De 28 để truy vấn log |
| Loki readiness | http://localhost:3101/ready | Mong đợi ready |

Trong pgAdmin, mở server **De 28 - PostgreSQL** rồi **Databases → petshop → Schemas → public → Tables**. Nếu cần khai báo server thủ công: host `db`, port `5432`, database `petshop`, username lấy từ `POSTGRES_USER`. Hộp thoại kết nối server dùng **POSTGRES_PASSWORD**, khác mật khẩu đăng nhập pgAdmin. Không nhập `localhost` làm host DB trong pgAdmin container.

Các cổng chỉ bind `127.0.0.1` để thực hành trên máy cục bộ. Không công bố PostgreSQL hoặc exporter ra host. Prometheus/Grafana/Loki dùng cổng 9091/3001/3101 để tách khỏi Lab 7–8. Website hiện dùng HTTP và security headers; chưa cấu hình HTTPS/TLS.

## 5. Kiểm tra sau khởi động

```bash
docker compose ps
docker compose exec nginx nginx -t
curl -i http://localhost:8088/health
curl http://localhost:3101/ready
python3 scripts/check-hardening.py
```

- `/health`: HTTP 200, JSON xác nhận kết nối DB và bốn security headers.
- Nginx: kiểm tra cú pháp thành công.
- Loki: trả ready; vừa khởi động có thể tạm trả 503, chờ rồi thử lại.
- Script hardening: kết thúc bằng `RESULT: PASS`, không in bí mật hoặc ghi dữ liệu nghiệp vụ.
- Trên Prometheus Targets: cadvisor, nginx, postgres, prometheus đều UP.
- Dashboard Grafana có dữ liệu; biểu đồ tốc độ cần vài lần scrape. CPU thấp hoặc tốc độ bằng 0 có thể bình thường khi hệ thống ít hoạt động.

Các file hướng dẫn ghi nhận kết quả đã kiểm chứng trên máy thực hành. Quy trình cài mới được đối chiếu cấu hình/script nhưng chưa thử trên một Docker host sạch; không xóa dữ liệu hiện có để kiểm thử lại từ đầu.

## 6. Ba truy vấn LogQL

Trong Grafana **Explore**, chọn datasource **Loki De 28**, chế độ **Code**, thời gian **Last 1 hour**, nhập từng truy vấn rồi bấm **Run query**:

```logql
{project="dtc245200404-de28"}
```

```logql
{project="dtc245200404-de28",service="nginx"} |= "GET /health"
```

```logql
{project="dtc245200404-de28",service="app"}
```

Nếu không thấy log, mở website hoặc /health để tạo yêu cầu GET mới, đợi khoảng 10 giây rồi truy vấn lại. Không nhập LogQL vào datasource Prometheus và không tạo dữ liệu nghiệp vụ giả để có log.

## 7. Hardening và giới hạn thực hành

- App non-root UID/GID 10001, filesystem chỉ đọc, `/tmp` giới hạn 16 MB/noexec/nosuid, bỏ capabilities và ngăn nâng quyền.
- Mạng DB internal; app và DB không có cổng host. Tài khoản app không superuser; exporter DB dùng role thống kê riêng.
- Nginx có security headers, giới hạn body/timeout, ẩn phiên bản và chặn đường dẫn tệp ẩn.
- `.env` không được Git theo dõi; bí mật riêng biệt, kiểm tra ngưỡng độ dài mà không in giá trị.
- cAdvisor vẫn cần quyền đặc biệt và mount hệ thống theo mô hình lab; Promtail cần Docker socket. Không coi mọi container đều có cùng quyền hạn chế như app. Loki không bật xác thực trong mô hình cục bộ.

Xem [hướng dẫn hardening](docs/07-hardening.md) và script `scripts/check-hardening.py` để kiểm chứng từng nhóm.

## 8. Dừng và xem lỗi

```bash
# Dung rieng project, giu container va volume
docker compose stop

# Khoi dong lai
docker compose up -d --no-build --pull never

# Xem log khi co loi; khong chia se noi dung chua kiem tra bi mat
docker compose logs --tail 50 app nginx
docker compose logs --tail 50 prometheus grafana
docker compose logs --tail 50 loki promtail
```

Không dùng `docker compose down -v`, `docker volume prune` hoặc xóa dữ liệu Docker để sửa lỗi. Không dừng hoặc đổi cấu hình Lab 7–8.

| Hiện tượng | Kiểm tra |
|---|---|
| Compose báo thiếu biến | Đang ở đúng thư mục? `.env` có đủ biến của `.env.example`? Không dùng `docker compose config` không có `--quiet` khi chụp vì có thể lộ bí mật. |
| Bash báo `$'\r'` | Lưu `.env` và script shell với xuống dòng LF; repository có `.gitattributes` cho mã nguồn. |
| Website 502 sau tạo lại app | Chờ app healthy, chạy `docker compose exec nginx nginx -t`, rồi `docker compose exec nginx nginx -s reload`. |
| PostgreSQL exporter không kết nối | Kiểm tra DB healthy, role giám sát đã tạo và mật khẩu khớp; không đổi `.env` để tự đặt lại mật khẩu DB cũ. |
| pgAdmin/Grafana báo sai mật khẩu | Volume cũ giữ tài khoản đã khởi tạo; biến môi trường khởi tạo không tự đặt lại mật khẩu. |
| Grafana No data | Kiểm tra Targets, datasource, khoảng thời gian và đợi vài chu kỳ scrape. |
| Cổng bị chiếm | Kiểm tra `docker compose ps` và `ss -ltn`; không tự dừng hệ thống khác. |

## 9. Cấu trúc và tài liệu báo cáo

```text
app/                 Ung dung Flask, giao dien va Dockerfile
database/            Cau truc PostgreSQL va role ung dung
pgadmin/             Khai bao server DB
nginx/               Reverse proxy va security headers
monitoring/          Prometheus, exporter setup, Grafana provisioning/dashboard
logging/             Loki va Promtail
scripts/             Kiem chung hardening chi doc
docs/                Huong dan bao cao, chup anh, doi chieu tieu chi
docker-compose.yml   Khai bao toan bo dich vu
.env.example         Ten bien mau, khong co mat khau that
```

- [Hướng dẫn báo cáo tổng hợp](docs/huong-dan-bao-cao.md).
- [Ứng dụng và DB](docs/02a-kiem-chung-ung-dung.md); [hồ sơ kiểm thử dữ liệu trước đây](docs/02b-du-lieu-va-kiem-thu.md).
- [Nginx](docs/04-nginx-reverse-proxy.md).
- [Prometheus và Grafana](docs/05-prometheus-grafana.md).
- [Loki, Promtail và LogQL](docs/06-loki-promtail.md).
- [Hardening](docs/07-hardening.md).
- [Biên bản rà soát trước khi bổ sung README](docs/08-doi-chieu-tieu-chi.md).

Các mốc kỹ thuật đã push: Nginx `b8b41dd`, giám sát `00d2d32`, log `e01441b`, hardening `0a50647`. README được bổ sung sau biên bản rà soát; nhận xét README rỗng trong tài liệu cũ mô tả trạng thái tại thời điểm đó.

Báo cáo yêu cầu tối thiểu 10 trang, có thông tin thật, giải thích và ảnh minh chứng. Sinh viên tự chụp ảnh sau khi kiểm tra; không đưa mật khẩu hoặc `.env` vào hình. Mã nguồn/hướng dẫn không thay thế bản báo cáo và phần demo của sinh viên.
