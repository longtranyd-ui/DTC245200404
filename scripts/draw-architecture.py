"""Ve so do tu cau hinh de 28 da doi chieu; khong chup man hinh."""
from pathlib import Path
from math import atan2, cos, sin, pi
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'so-do'
OUT.mkdir(parents=True, exist_ok=True)
W, H = 2400, 1720
im = Image.new('RGB', (W, H), '#ffffff')
d = ImageDraw.Draw(im)
fontdir = Path('C:/Windows/Fonts')
regular = fontdir / 'arial.ttf'
bold = fontdir / 'arialbd.ttf'
if not regular.exists():
    raise SystemExit('Can font Arial trong Windows de render dung tieng Viet.')


def font(size, strong=False):
    return ImageFont.truetype(str(bold if strong else regular), size)


def text(x, y, content, size=28, fill='#34465b', strong=False, anchor='la'):
    d.text((x, y), content, font=font(size, strong), fill=fill, anchor=anchor)


def box(rect, title, lines, color='#f0f7ff', border='#b6cfe8'):
    x1, y1, x2, y2 = rect
    d.rounded_rectangle(rect, radius=18, fill=color, outline=border, width=3)
    text((x1+x2)//2, y1+28, title, 34, '#173850', True, 'ma')
    y = y1+83
    for line in lines:
        text((x1+x2)//2, y, line, 26, anchor='ma')
        y += 37


def arrow(points, label=None, pos=None, color='#397295'):
    d.line(points, fill=color, width=5, joint='curve')
    x, y = points[-1]
    prev = points[-2]
    a = atan2(y-prev[1], x-prev[0])
    d.polygon([(x, y), (x-18*cos(a-pi/6), y-18*sin(a-pi/6)),
               (x-18*cos(a+pi/6), y-18*sin(a+pi/6))], fill=color)
    if label:
        x, y = pos
        bb=d.textbbox((x,y),label,font=font(24),anchor='ma')
        d.rectangle((bb[0]-10,bb[1]-4,bb[2]+10,bb[3]+4),fill='#ffffff')
        text(x,y,label,24,fill=color,anchor='ma')


text(90, 48, 'SƠ ĐỒ KIẾN TRÚC TỔNG THỂ', 52, '#173850', True)
text(90, 115, 'Đề 28 • Hệ thống Quản lý Cửa hàng Thú cưng • DTC245200404', 30)
d.rounded_rectangle((60,190,2340,1450),radius=24,fill='#fafcfe',outline='#c7d4e0',width=3)
text(100,213,'MÁY THỰC HÀNH: WINDOWS + UBUNTU WSL2 / DOCKER COMPOSE',28,strong=True)
box((120,275,2240,375),'Trình duyệt trên máy thực hành',[],color='#edf3f8')
text(1180,335,'Website :8088     •     pgAdmin :8089     •     Prometheus :9091     •     Grafana :3001',26,anchor='ma')

box((120,445,530,645),'Nginx', ['Reverse proxy :8080','Security headers • HTTP'])
box((690,445,1100,645),'Flask / Gunicorn', ['Ứng dụng :8000','Đăng nhập • Quản trị / Nhân viên'])
box((1260,445,1670,645),'PostgreSQL', ['petshop :5432','4 bảng dữ liệu nghiệp vụ'], '#eef8f0','#b6d5bc')
box((1830,445,2240,645),'pgAdmin', ['Quản trị PostgreSQL','Cổng nội bộ :5050'],'#eef8f0','#b6d5bc')
arrow([(325,375),(325,445)],'HTTP :8088',(325,396))
arrow([(530,545),(690,545)],'HTTP',(610,505))
arrow([(1100,545),(1260,545)],'SQL',(1180,505))
arrow([(1830,545),(1670,545)],'SQL',(1750,505))
text(1180,674,'Chức năng: Khách hàng • Thú cưng • Dịch vụ spa • Lịch hẹn',28,anchor='ma')

d.rounded_rectangle((100,755,1720,1055),radius=18,fill='#f1f6fc',outline='#c6d8ed',width=2)
text(130,775,'GIÁM SÁT — METRICS',28,strong=True)
box((130,830,740,1035),'Bộ thu thập thống kê', ['cAdvisor → CPU / RAM container','Nginx exporter → stub_status :8081','PostgreSQL exporter → role pg_monitor'])
box((1040,830,1660,1015),'Prometheus :9090', ['Chủ động kéo metrics mỗi 15 giây','Cổng truy cập host :9091'])
arrow([(740,925),(1040,925)],'Metrics',(890,883))

box((1840,890,2240,1210),'Grafana :3000', ['Host :3001','Dashboard: metrics','Explore: log','PromQL / LogQL'], '#f4effc','#d2c1ed')
arrow([(1660,925),(1770,925),(1770,970),(1840,970)],'PromQL',(1765,875))

d.rounded_rectangle((100,1115,1720,1400),radius=18,fill='#fff8ed',outline='#e8d5b4',width=2)
text(130,1135,'LOG TẬP TRUNG',28,strong=True)
box((130,1195,530,1355),'Log container', ['stdout / stderr','Chỉ project đề 28'],'#fffaf1','#e5d3b6')
box((690,1195,1090,1355),'Promtail', ['Đọc qua Docker socket','Gắn nhãn / lọc project'],'#fffaf1','#e5d3b6')
box((1250,1195,1650,1355),'Loki :3100', ['Lưu log tập trung','Host :3101'],'#fffaf1','#e5d3b6')
arrow([(530,1275),(690,1275)],'Log',(610,1230),color='#aa722f')
arrow([(1090,1275),(1250,1275)],'Push',(1170,1230),color='#aa722f')
arrow([(1650,1275),(1770,1275),(1770,1140),(1840,1140)],'LogQL',(1780,1310),color='#aa722f')
text(2040,1250,'Grafana truy vấn hai datasource',23,anchor='ma')
text(2040,1285,'Prometheus và Loki',23,anchor='ma')

text(100,1480,'PHÂN TÁCH MẠNG DOCKER',27,strong=True)
text(100,1530,'web_net: Nginx, app, Nginx exporter   |   db_net (internal): DB, app, pgAdmin, PostgreSQL exporter',25)
text(100,1570,'admin_net: pgAdmin   |   monitor_net: Prometheus, Grafana, cAdvisor, exporters, Loki, Promtail',25)
text(100,1620,'Lưu trữ: 6 named volumes cho PostgreSQL, pgAdmin, Prometheus, Grafana, Loki và vị trí đọc Promtail.',25)
text(100,1660,'Mũi tên biểu diễn luồng xử lý / dữ liệu. Các cổng host chỉ bind 127.0.0.1. Chưa triển khai HTTPS.',24)
im.save(OUT / 'kien-truc-tong-the.png', dpi=(300,300))
print(OUT / 'kien-truc-tong-the.png')
