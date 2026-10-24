# Áp dụng và kiểm chứng Hardening — Đề 28

## 1. Mục đích và phạm vi

Áp dụng nguyên tắc quyền tối thiểu, tách mạng và bảo vệ cấu hình theo các chương Docker, quản trị DB, Nginx và bảo mật trong tài liệu đã cung cấp. Tiêu chí đề tài yêu cầu ít nhất 3–4 biện pháp; bước này kiểm chứng nhiều biện pháp riêng biệt trên môi trường đề 28.

Mọi thao tác tại `C:\DTC245200404` (`/mnt/c/DTC245200404` trong Ubuntu). Không thêm, sửa hoặc xóa bản ghi nghiệp vụ, không thay đổi hệ thống Lab 7–8. Không đổi mật khẩu hiện có ở bước này.

## 2. Các biện pháp được áp dụng

| Biện pháp | Cấu hình / kết quả thực tế | Ý nghĩa |
|---|---|---|
| Non-root ứng dụng | UID/GID 10001 | Giới hạn quyền tiến trình ứng dụng |
| Filesystem chỉ đọc | App `read_only: true`; /tmp là tmpfs 16 MB, noexec, nosuid | Giới hạn vùng ghi; không thực thi trực tiếp file tại /tmp, vẫn cho phép chương trình dùng tệp tạm |
| Hạn chế capabilities / nâng quyền | App bỏ ALL capabilities và có no-new-privileges; bổ sung tương tự cho sáu dịch vụ giám sát/log | Giảm quyền hệ điều hành mà tiến trình có thể sử dụng |
| Tách mạng DB | db_net internal; DB và app không publish cổng; Nginx không nối db_net | Không mở DB trực tiếp ra host, chỉ các dịch vụ cần thiết được nối mạng DB |
| Cổng quản trị giới hạn cục bộ | Nginx, pgAdmin, Prometheus, Grafana, Loki bind 127.0.0.1 | Chỉ công bố trên loopback máy thực hành |
| Quyền DB tối thiểu | App không superuser/CREATEDB/CREATEROLE, không CREATE schema; có CRUD bảng nghiệp vụ | Phân biệt tài khoản chạy ứng dụng với tài khoản quản trị |
| Quyền exporter DB | pg_monitor, không superuser và không có quyền đọc/ghi bảng nghiệp vụ | Thu thập thống kê mà không dùng tài khoản quản trị DB |
| Mật khẩu và Git | Các mật khẩu/khóa riêng biệt, mỗi giá trị ít nhất 16 ký tự; .env bị ignore và không tracked | Không dùng chung bí mật, không đưa .env thật vào source Git hiện tại |
| Nginx bảo mật | Bốn security headers, ẩn phiên bản, giới hạn body 64 KB và timeout | Hạn chế một số hành vi trình duyệt và yêu cầu không phù hợp |
| Chặn tệp ẩn | `/.env`, `/.git/config` trả 403 | Nginx không chuyển các đường dẫn tệp ẩn này tới ứng dụng |

Phân biệt cấu hình có từ bước trước và thay đổi mới: non-root, read-only, quyền DB, mạng và headers đã có; bước này kiểm chứng tập trung, bổ sung noexec/nosuid/giới hạn /tmp, giới hạn quyền cho sáu dịch vụ giám sát/log, timeout Nginx và chặn đường dẫn tệp ẩn.

Không kết luận mọi container đều non-root hoặc bỏ capabilities. cAdvisor giữ quyền đặc biệt theo mô hình lab để đọc tài nguyên host; Promtail có Docker socket để thu log (mount :ro không biến API thành chỉ đọc). Website hiện dùng HTTP với security headers, chưa có TLS. Kiểm tra độ dài và tính riêng biệt không phải chứng minh toàn bộ chất lượng mật khẩu hoặc lịch sử Git chưa từng có bí mật.

## 3. Script kiểm chứng chỉ đọc

`scripts/check-hardening.py` dùng các công cụ sẵn có: Python chuẩn, Docker, Git. Nó đọc trạng thái container, metadata mạng, quyền PostgreSQL và gửi GET kiểm tra HTTP. Không gọi INSERT/UPDATE/DELETE; không in mật khẩu hoặc khóa bí mật.

Chạy đầy đủ trong Ubuntu:

```bash
cd /mnt/c/DTC245200404
python3 scripts/check-hardening.py
```

Kết quả phải kết thúc bằng `RESULT: PASS`. Nếu FAIL, giữ nguyên màn hình và báo để xử lý trước khi đưa kết luận vào báo cáo. Có thể chạy từng nhóm bằng tùy chọn `--section` ở mục chụp ảnh.

## 4. Kết quả kiểm chứng ngày 25/10/2026

- App chạy UID 10001; read-only root filesystem, tmpfs hạn chế thực thi; bỏ ALL capabilities và no-new-privileges.
- Sáu dịch vụ prometheus, grafana, nginx-exporter, postgres-exporter, loki, promtail có cấu hình bỏ capabilities và no-new-privileges.
- db_net internal; DB/app không công bố cổng; Nginx không tham gia db_net; các cổng công bố của đề 28 bind loopback.
- Kiểm tra quyền app và monitor đạt các điều kiện ở bảng trên.
- GET /health trả 200; GET /.env và /.git/config trả 403; đường dẫn không tồn tại trả 404. Các phản hồi kiểm tra đều có security headers và không lộ phiên bản Nginx.
- Bí mật đều vượt ngưỡng kiểm tra độ dài, riêng biệt; .env không bị Git theo dõi. Giá trị không được in vào kết quả.
- customers=1, pets=1, services=1, appointments=1 sau thay đổi.
- Kiểm tra lại Prometheus: bốn Targets UP, tám panel có dữ liệu. Ba truy vấn LogQL vẫn trả log và datasource Grafana kết nối thành công.
- Chưa có ảnh hardening nào được sinh viên xác nhận đã chụp.

Các kiểm tra trên chứng minh trạng thái cấu hình/quyền tại thời điểm chạy; không thay thế rà quét lỗ hổng toàn diện hoặc kiểm thử tấn công.

## 5. Hướng dẫn chụp ảnh và chú thích

Mở terminal Ubuntu tại thư mục dự án. Chạy từng nhóm riêng để ảnh gọn và chữ dễ đọc. Không dùng `docker inspect` không kèm lọc hoặc `cat .env` để chụp vì có thể làm lộ bí mật.

### Hình 24 — Non-root và giới hạn quyền container

```bash
cd /mnt/c/DTC245200404
python3 scripts/check-hardening.py --section app
```

Chụp UID 10001, các dòng PASS và RESULT: PASS. Chú thích: **Hình 24. Kiểm chứng ứng dụng chạy non-root, filesystem chỉ đọc và giới hạn quyền container.**

Đoạn giải thích: Ứng dụng chạy bằng tài khoản có UID 10001. Cấu hình filesystem chỉ đọc, tmpfs có giới hạn và bỏ Linux capabilities giúp giảm quyền và vùng ghi của tiến trình.

### Hình 25 — Tách mạng và hạn chế cổng

```bash
python3 scripts/check-hardening.py --section network
```

Chụp các dòng PASS cho mạng DB internal, không publish cổng DB/app và các cổng loopback. Chú thích: **Hình 25. Kiểm chứng cô lập mạng cơ sở dữ liệu và giới hạn cổng công bố.**

Đoạn giải thích: PostgreSQL không được công bố trực tiếp ra host. Dịch vụ Nginx không tham gia mạng DB, trong khi các cổng giao diện và quản trị chỉ bind trên địa chỉ 127.0.0.1 của môi trường thực hành.

### Hình 26 — Phân quyền PostgreSQL

```bash
python3 scripts/check-hardening.py --section db
```

Chụp tên hai role, các dòng kiểm tra quyền và số bản ghi. Không có mật khẩu trong kết quả. Chú thích: **Hình 26. Kiểm chứng quyền tối thiểu của tài khoản ứng dụng và tài khoản giám sát PostgreSQL.**

Đoạn giải thích: Tài khoản ứng dụng có quyền CRUD cần thiết nhưng không có quyền quản trị DB hoặc tạo schema. Tài khoản giám sát có pg_monitor và không có quyền đọc/ghi bảng nghiệp vụ. Truy vấn đếm chỉ đọc xác nhận dữ liệu hiện có.

### Hình 27 — Security headers và chặn tệp ẩn

```bash
python3 scripts/check-hardening.py --section http
```

Chụp các mã HTTP 200, 403, 404 và kết quả kiểm tra header. Có thể bổ sung ảnh header thật bằng:

```bash
curl -i http://localhost:8088/.env
```

Đây là yêu cầu GET bị chặn, không đọc file .env trên máy. Chú thích: **Hình 27. Nginx chặn đường dẫn tệp ẩn và duy trì security headers trên phản hồi.**

Đoạn giải thích: Các đường dẫn /.env và /.git/config bị Nginx từ chối bằng mã 403. Security headers vẫn được thêm vào các phản hồi lỗi nhờ cấu hình always.

### Hình 28 — Kiểm tra bí mật không lộ giá trị

```bash
python3 scripts/check-hardening.py --section secrets
```

Chụp kết quả PASS; không mở .env để chụp. Chú thích: **Hình 28. Kiểm tra độ dài, tính riêng biệt của bí mật và việc loại .env khỏi Git.**

Đoạn giải thích: Script xác nhận mật khẩu và khóa đạt ngưỡng độ dài, có giá trị riêng biệt và file .env không được Git theo dõi. Giá trị bí mật không hiển thị trong minh chứng.

## 6. Đoạn tổng hợp cho báo cáo

> Hệ thống áp dụng nhiều lớp hardening gồm chạy ứng dụng non-root, filesystem chỉ đọc, giới hạn capabilities, ngăn nâng quyền, cô lập mạng DB, phân quyền PostgreSQL và thiết lập security headers Nginx. Các mật khẩu và khóa được lưu trong .env cục bộ, không đưa vào Git. Nginx chặn đường dẫn tệp ẩn và chỉ công bố website trên loopback môi trường thực hành.

> Các biện pháp được kiểm chứng bằng script chỉ đọc kết hợp kiểm tra metadata Docker, quyền DB và phản hồi HTTP. Sau thay đổi, website hoạt động, Prometheus/Grafana có số liệu và LogQL vẫn truy vấn được log. Dữ liệu nghiệp vụ giữ nguyên. Các quyền đặc biệt cần cho cAdvisor và Docker socket của Promtail được ghi nhận riêng, không coi là quyền của ứng dụng web.

Chèn ảnh thật do sinh viên chụp vào từng mục tương ứng; không ghi đã chụp khi chưa thực hiện.
