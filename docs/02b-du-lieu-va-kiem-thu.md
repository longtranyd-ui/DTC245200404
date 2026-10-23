# Bước 2B — Dữ liệu được duyệt và kiểm thử thêm/sửa/xóa

## Phạm vi được sinh viên cho phép

Sinh viên đã đồng ý dùng bộ dữ liệu giả lập được đề xuất trong chat, đổi giờ lịch hẹn và tạo/xóa bản ghi thử riêng. Không nhập dữ liệu ngoài bộ đã duyệt.

| Nhóm | Bản ghi chính giữ lại |
|---|---|
| Khách hàng | Nguyễn Văn An; điện thoại giả lập 0900000000 |
| Thú cưng | Mít; Mèo; chủ sở hữu Nguyễn Văn An |
| Dịch vụ | Tắm và vệ sinh; 150.000 VNĐ; 45 phút |
| Lịch hẹn | Mít; Tắm và vệ sinh; 24/10/2026 lúc 10:00 UTC+7; Đã đặt |

## Cách kiểm chứng và kết quả thực tế

Kiểm tra ban đầu xác nhận bốn bảng đều trống. Dùng Flask test client trong container ứng dụng gọi các route biểu mẫu, có CSRF token; kết nối đến PostgreSQL đang chạy. Đây là kiểm tra chức năng phía máy chủ, chưa phải kiểm thử thao tác bằng chuột trên trình duyệt.

1. Tạo khách hàng, thú cưng, dịch vụ và lịch hẹn qua các route `/them`: đều trả HTTP 302 sau khi lưu.
2. Lịch hẹn ban đầu 09:00 ngày 24/10/2026; gọi route sửa để đổi thành 10:00 cùng ngày. Truy vấn DB theo múi giờ Asia/Bangkok xác nhận giờ mới là 10.
3. Tạo một khách hàng thử trùng tên và điện thoại bộ đã duyệt; xóa bản ghi thử qua route `/xoa`. Truy vấn theo ID xác nhận bản ghi thử không còn; bản ghi khách hàng chính giữ nguyên.
4. Kiểm tra cuối: customers=1, pets=1, services=1, appointments=1. Các trang danh sách, trang tổng quan và `/health` đều trả HTTP 200.

Chưa kiểm chứng đăng nhập pgAdmin và truy vấn DB bằng giao diện. Chưa kiểm thử cập nhật/xóa riêng cho mọi loại bản ghi hoặc mọi tình huống lỗi. Chưa hoàn tất các tiêu chí Nginx, giám sát và log của đề 28.

## Sinh viên tự chụp ảnh

Mở http://localhost:8088/lich-hen để chụp danh sách có tên thú cưng, chủ, dịch vụ, giờ 10:00 và trạng thái. Chú thích: “Lịch hẹn sau khi cập nhật, dữ liệu được lưu trong PostgreSQL”.

Mở trang tổng quan để chụp bốn bộ đếm bằng 1. Chú thích: “Dữ liệu thực hành sau kiểm thử, mỗi nhóm có một bản ghi chính”.

Ảnh danh sách cuối chỉ chứng minh trạng thái sau kiểm tra, không phải ảnh trước/sau thao tác. Không ghi đã chụp hoặc đã đưa vào báo cáo khi sinh viên chưa xác nhận.

## Nội dung viết vào báo cáo

“Sau khi thống nhất bộ dữ liệu giả lập, hệ thống được kiểm tra thông qua các route xử lý biểu mẫu của Flask và đối chiếu với PostgreSQL. Bốn nhóm dữ liệu được thêm thành công. Lịch hẹn của thú cưng Mít được đổi từ 09:00 sang 10:00 ngày 24/10/2026 theo múi giờ UTC+7. Một khách hàng thử được tạo và xóa để kiểm chứng thao tác xóa mà không ảnh hưởng dữ liệu chính. Kết thúc kiểm tra, mỗi bảng nghiệp vụ còn một bản ghi. Phần đăng nhập và truy vấn qua giao diện pgAdmin sẽ được kiểm chứng ở bước tiếp theo.”
