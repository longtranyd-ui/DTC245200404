# Quy tắc làm việc Đề 28

- Sinh viên đã yêu cầu bổ sung đăng nhập và phân vai quản trị/nhân viên cho website. Tài khoản kỹ thuật được tạo cục bộ; không thay đổi bốn bảng nghiệp vụ để kiểm thử quyền.

- Thư mục làm việc duy nhất: `C:\DTC245200404`, tương ứng `/mnt/c/DTC245200404` trong Ubuntu WSL2. Chỉnh sửa, Git và Docker Compose đều thực hiện từ đây; giữ nguyên Docker volumes hiện có.

- Làm theo yêu cầu trực tiếp của người dùng trong chat; ghi lại các thay đổi phạm vi được người dùng chấp thuận.
- Không tự chụp ảnh màn hình, không sinh hoặc thay thế ảnh minh chứng. Khi đến bước cần ảnh, mở đúng trang, hướng dẫn nội dung cần chụp và chờ người dùng tự chụp.
- Chỉ dựa trên tài liệu người dùng đã cung cấp: đề tài K23, giáo trình/slide chương 1–9, Lab 7–8. Không tự lấy mẫu dự án, bài viết, hình ảnh hoặc dữ liệu bên ngoài.
- Không tự thêm dữ liệu mẫu, hồ sơ khách hàng, thú cưng, dịch vụ, lịch hẹn hoặc số liệu báo cáo. Dữ liệu do người dùng nhập/cung cấp hoặc được đồng ý rõ ràng trước khi tạo.
- Đề 28 yêu cầu website quản lý thú cưng, dịch vụ spa, khách hàng, lịch hẹn; PostgreSQL + pgAdmin. Không tự đổi DB hoặc thêm chức năng ngoài phạm vi.
- Hoàn thành toàn bộ tiêu chí trong PDF: GitHub/README, ứng dụng/DB tool, Nginx, giám sát container/web/DB, Loki/Promtail/LogQL, hardening và báo cáo ít nhất 10 trang.
- Giải thích thao tác cho người mới học và cập nhật hướng dẫn viết báo cáo trong quá trình thực hành. Chỉ ghi kết quả đã kiểm chứng.
- Nếu cần thêm công cụ, tải phụ thuộc, dữ liệu, tài khoản hoặc yêu cầu chưa có trong phạm vi đã thống nhất, báo người dùng trước khi thực hiện phần phụ thuộc đó.
- Mỗi nhiệm vụ hoàn thành phải có commit có ý nghĩa và push lên https://github.com/longtranyd-ui/DTC245200404.git. Không force-push hoặc sửa lịch sử cũ.
- Không commit mật khẩu/token, .env thật, khóa riêng, bản sao DB hoặc thông tin cá nhân ngoài phạm vi người dùng cho phép công khai.
- Không thay đổi/xóa hệ thống và dữ liệu Lab 7–8 để làm Đề 28 khi chưa được người dùng đồng ý.
