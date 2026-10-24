# Môi trường hệ thống

Hệ thống quản lý cửa hàng thú cưng được triển khai trên máy tính sử dụng Windows 11, kết hợp Ubuntu chạy trong Windows Subsystem for Linux 2 (WSL2). Docker Engine và Docker Compose được sử dụng trong Ubuntu để xây dựng, khởi chạy và quản lý các container. Mã nguồn, cấu hình và tài liệu của đề tài được lưu tập trung tại `C:\DTC245200404`, tương ứng `/mnt/c/DTC245200404` trong Ubuntu.

## Các thành phần phần mềm

Phiên bản được đọc trực tiếp từ môi trường máy thực hành và container; không suy ra phiên bản từ tag image `latest`.

| Thành phần | Phiên bản / cấu hình | Vai trò |
|---|---|---|
| Hệ điều hành máy host | Windows 11 Home Single Language, 10.0.26200 | Môi trường máy tính thực hành và trình duyệt |
| Hệ điều hành Linux | Ubuntu 26.04.1 LTS trên WSL2 | Chạy Docker Engine và thao tác terminal |
| Kernel WSL2 | 6.18.54.1-microsoft-standard-WSL2 | Nhân Linux của môi trường WSL2 |
| Docker Engine trong Ubuntu | 29.1.3 | Quản lý image, container, network và volume |
| Docker Compose | 2.40.3+ds1-0ubuntu1 | Khai báo và triển khai các dịch vụ |
| Python trong container ứng dụng | 3.12.15 | Ngôn ngữ xử lý nghiệp vụ |
| Flask | 3.1.3 | Framework website |
| Gunicorn | 23.0.0 | Chạy ứng dụng WSGI |
| Psycopg | 3.3.6 | Kết nối Python với PostgreSQL |
| PostgreSQL | 16.15 | Lưu dữ liệu nghiệp vụ |
| Nginx | 1.30.6 | Reverse proxy và security headers |
| pgAdmin | Dịch vụ container riêng | Quản trị PostgreSQL |
| Prometheus, Grafana và các exporter | Các dịch vụ container riêng | Giám sát container, web server và DB |
| Loki và Promtail | Các dịch vụ container riêng | Thu thập, lưu trữ và truy vấn log |

Docker phiên bản trên là daemon trong Ubuntu WSL2 đang phục vụ đề 28; không lấy phiên bản Docker Desktop trên Windows làm phiên bản triển khai.

## Cổng truy cập của môi trường thực hành

| Thành phần | Địa chỉ trên máy thực hành |
|---|---|
| Website qua Nginx | http://localhost:8088 |
| pgAdmin | http://localhost:8089 |
| Prometheus | http://localhost:9091 |
| Grafana | http://localhost:3001 |
| Kiểm tra Loki sẵn sàng | http://localhost:3101/ready |

Các cổng công bố chỉ bind trên địa chỉ loopback 127.0.0.1. PostgreSQL, ứng dụng và các exporter không công bố cổng trực tiếp ra host. Hệ thống sử dụng HTTP với security headers; chưa triển khai SSL/TLS.

## Mạng và lưu trữ

Các container được kết nối qua bốn mạng theo chức năng: `web_net`, `db_net`, `admin_net` và `monitor_net`. Trong đó `db_net` đặt `internal: true` để cô lập mạng cơ sở dữ liệu. Dữ liệu cần duy trì được lưu trong Docker named volume cho PostgreSQL, pgAdmin, Prometheus, Grafana, Loki và vị trí đọc log của Promtail.

Không ghi dung lượng RAM, CPU hoặc ổ đĩa vào báo cáo từ cấu hình gợi ý của bài lab; mục này chưa kiểm kê phần cứng máy thực hành. Nếu cần bổ sung bảng phần cứng, phải đọc thông số thực tế trước.
