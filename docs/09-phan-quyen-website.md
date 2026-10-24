# Đăng nhập và phân quyền website

## 1. Phạm vi sinh viên yêu cầu bổ sung

Sinh viên đã chọn thêm đăng nhập và phân vai **quản trị/nhân viên** cho website. Đây là phần mở rộng được yêu cầu trực tiếp, ngoài việc tách tài khoản PostgreSQL đã có. Không thêm bảng dữ liệu hoặc thay đổi dữ liệu khách hàng, thú cưng, dịch vụ và lịch hẹn.

| Chức năng | Chưa đăng nhập | Quản trị viên | Nhân viên |
|---|---|---|---|
| Tổng quan và bốn danh sách | Chuyển đến đăng nhập | Được xem | Được xem |
| Thêm và sửa | Không được truy cập | Được phép | Được phép |
| Xóa | Không được truy cập | Được phép, vẫn kiểm tra ràng buộc DB | Bị chặn HTTP 403 |
| /health | Được kiểm tra | Được kiểm tra | Được kiểm tra |

Việc thêm/sửa/xóa chỉ được thao tác với dữ liệu khi sinh viên cho phép; có quyền không đồng nghĩa phải dùng dữ liệu thật để thử.

## 2. Tài khoản và lưu mật khẩu

- Địa chỉ: `http://localhost:8088/dang-nhap`.
- Tên tài khoản quản trị mặc định: `admin`.
- Tên tài khoản nhân viên mặc định: `nhanvien`.
- Mật khẩu ngẫu nhiên riêng được lưu trong `.web-credentials` tại thư mục gốc, chỉ trên máy thực hành.
- Ứng dụng nhận password hash PBKDF2-SHA256 600.000 vòng, mỗi mật khẩu có salt riêng, qua `.env`; không nhận mật khẩu rõ từ file thông tin đăng nhập.
- `.env` và `.web-credentials` được Git bỏ qua. Không đưa hash hay mật khẩu vào ảnh báo cáo, Git hoặc log.

Để xem mật khẩu, mở `.web-credentials` cục bộ trong trình soạn thảo; đóng file trước khi chụp. Tài khoản website khác tài khoản pgAdmin và Grafana.

Khởi tạo trên môi trường mới, sau khi có `.env`:

```bash
cd /mnt/c/DTC245200404
python3 scripts/setup-web-auth.py
docker compose config --quiet
docker compose build app
docker compose up -d --no-deps --no-build --pull never app
docker compose exec nginx nginx -s reload
```

Script chạy lại sẽ giữ nguyên hash/tài khoản đã cấu hình; không tự đổi mật khẩu. Không xóa `.env` để đặt lại tài khoản. Trên máy hiện tại đã thực hiện các bước này, không cần tạo lại.

## 3. Cách bảo vệ ở phía máy chủ

- Mỗi yêu cầu nghiệp vụ phải có phiên đăng nhập hợp lệ; request GET chưa đăng nhập chuyển đến trang đăng nhập, thao tác POST bị chặn HTTP 401.
- Vai trò được tra từ cấu hình tài khoản trên máy chủ, không tin trường role do người dùng gửi hoặc thêm vào phiên.
- Route xóa kiểm tra admin trước khi kết nối DB. Ẩn nút chỉ là hỗ trợ giao diện, không phải cơ chế bảo vệ duy nhất.
- Login, logout và mọi biểu mẫu POST dùng CSRF token.
- Đăng nhập thành công xóa phiên cũ, đăng xuất xóa phiên; phiên có thời hạn 30 phút và được gia hạn theo hoạt động.
- Cookie có HttpOnly, SameSite=Lax; các trang động có Cache-Control: no-store. Hệ thống hiện dùng HTTP cục bộ, chưa có TLS và chưa đặt Secure cookie.
- /health vẫn công khai để healthcheck không bị chuyển đến đăng nhập; không hiển thị bản ghi nghiệp vụ.

Đây là hai tài khoản cấu hình phục vụ thực hành. Chưa bổ sung quản lý tài khoản qua giao diện, đăng ký tự do, MFA hoặc quy trình quên mật khẩu.

## 4. Kiểm chứng đã thực hiện

Sáu kiểm thử tự động với Flask test client và DB giả lập đã đạt:

1. Người chưa đăng nhập không vào được các trang nghiệp vụ hoặc gọi xóa.
2. Nhân viên bị chặn xóa ở cả bốn nhóm dữ liệu, kể cả giả trường role=admin trong phiên.
3. Quản trị được qua bước kiểm tra quyền xóa; thao tác DB trong phép thử được mock, không xóa dữ liệu thật.
4. Nhân viên mở được biểu mẫu thêm/sửa.
5. Đăng nhập đúng/sai, làm mới phiên và đăng xuất hoạt động.
6. /health công khai; thao tác nhạy cảm thiếu CSRF bị chặn trước DB.

Chạy lại bằng:

```bash
docker compose exec -T app python - < scripts/test-web-auth.py
```

Tài khoản và bản ghi mock trong test chỉ tồn tại trong bộ nhớ tiến trình kiểm thử; không được lưu vào PostgreSQL. Script không ghi log kiểm thử vào logger ứng dụng.

Kiểm tra HTTP thực tế qua Nginx: hai tài khoản đăng nhập được, xem bốn danh sách và biểu mẫu thêm; admin thấy nút Xóa, staff không thấy; đăng xuất mất quyền truy cập. Không gửi biểu mẫu thêm/sửa/xóa tới dữ liệu thật. Hardening vẫn PASS, số bản ghi bốn bảng vẫn bằng 1.

## 5. Hướng dẫn tự chụp ảnh

Không tự chụp ảnh thay sinh viên. Chưa xác nhận có ảnh của bước này.

### Hình 29 — Trang đăng nhập

Mở `http://localhost:8088/dang-nhap` khi chưa đăng nhập. Chụp tiêu đề và biểu mẫu, để trống ô mật khẩu.

Chú thích: **Hình 29. Giao diện đăng nhập website quản lý cửa hàng thú cưng.**

### Hình 30 — Vai trò quản trị

Đăng nhập `admin`, mở danh sách khách hàng. Chụp thanh trên có tên và vai trò Quản trị viên cùng các nút Thêm, Sửa, Xóa. Không bấm xóa bản ghi.

Chú thích: **Hình 30. Quản trị viên có các thao tác xem, thêm, sửa và xóa trên giao diện.**

### Hình 31 — Vai trò nhân viên

Bấm Đăng xuất, đăng nhập `nhanvien`, mở cùng danh sách. Chụp thanh vai trò Nhân viên, nút Thêm/Sửa và phần thao tác không có nút Xóa.

Chú thích: **Hình 31. Nhân viên được thao tác thêm/sửa và không được cung cấp nút xóa.**

### Hình 32 — Chặn quyền phía máy chủ

Trong Ubuntu chạy lệnh kiểm thử ở mục 4. Chụp câu lệnh và kết quả `Ran 6 tests ... OK`. Không thực hiện xóa bản ghi thật để tạo ảnh.

Chú thích: **Hình 32. Kiểm thử đăng nhập, CSRF và phân quyền phía máy chủ bằng dữ liệu giả lập trong bộ nhớ.**

Ảnh 30–31 chứng minh giao diện theo vai trò; ảnh kiểm thử hỗ trợ chứng minh route xóa bị kiểm soát ở máy chủ, không chỉ ẩn nút.

## 6. Đoạn viết báo cáo

> Website bổ sung xác thực bằng tên đăng nhập và mật khẩu, phân thành hai vai trò quản trị viên và nhân viên. Quản trị viên được xem, thêm, sửa, xóa; nhân viên được xem, thêm, sửa nhưng không được xóa. Mọi route nghiệp vụ yêu cầu phiên đăng nhập hợp lệ, còn route xóa kiểm tra vai trò trên máy chủ trước khi truy cập cơ sở dữ liệu.

> Mật khẩu được kiểm tra bằng password hash PBKDF2-SHA256 có salt. Các biểu mẫu POST có CSRF token, phiên cũ được xóa khi đăng nhập hoặc đăng xuất. Kiểm thử tự động dùng DB giả lập xác nhận nhân viên bị chặn xóa và không thể nâng quyền bằng trường role trong phiên. Kiểm tra trên hệ thống thật chỉ đọc các trang; dữ liệu nghiệp vụ được giữ nguyên.
