"""Website De 28: bon nhom chuc nang da duoc sinh vien duyet."""
import hmac
import logging
import os
import secrets
from datetime import datetime
from decimal import Decimal, InvalidOperation
from zoneinfo import ZoneInfo

import psycopg
from psycopg import sql
from psycopg.rows import dict_row
from flask import Flask, abort, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.config.update(SECRET_KEY=os.environ['SECRET_KEY'], MAX_CONTENT_LENGTH=64 * 1024,
                  SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax')
logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
TZ = ZoneInfo('Asia/Bangkok')
STATUSES = {'scheduled': 'Đã đặt', 'completed': 'Hoàn thành', 'cancelled': 'Đã hủy'}
ENTITIES = {
    'khach-hang': dict(table='customers', title='Khách hàng', singular='khách hàng',
        description='Quản lý họ tên và số điện thoại của khách hàng.',
        fields=[('full_name', 'Họ tên', 'text', 120), ('phone', 'Điện thoại', 'text', 30)],
        headers=['Họ tên', 'Điện thoại'], columns=['full_name', 'phone']),
    'thu-cung': dict(table='pets', title='Thú cưng', singular='thú cưng',
        description='Mỗi thú cưng được liên kết với một khách hàng.',
        fields=[('name', 'Tên thú cưng', 'text', 100), ('species', 'Loài', 'text', 80), ('customer_id', 'Chủ sở hữu', 'customer', None)],
        headers=['Tên thú cưng', 'Loài', 'Chủ sở hữu'], columns=['name', 'species', 'owner_name']),
    'dich-vu': dict(table='services', title='Dịch vụ spa', singular='dịch vụ spa',
        description='Quản lý tên dịch vụ, giá và thời lượng thực hiện.',
        fields=[('name', 'Tên dịch vụ', 'text', 120), ('price', 'Giá (VNĐ)', 'money', None), ('duration_minutes', 'Thời lượng (phút)', 'integer', None)],
        headers=['Tên dịch vụ', 'Giá (VNĐ)', 'Thời lượng (phút)'], columns=['name', 'price', 'duration_minutes']),
    'lich-hen': dict(table='appointments', title='Lịch hẹn', singular='lịch hẹn',
        description='Theo dõi thú cưng, dịch vụ, ngày giờ và trạng thái lịch hẹn.',
        fields=[('pet_id', 'Thú cưng', 'pet', None), ('service_id', 'Dịch vụ', 'service', None), ('starts_at', 'Ngày giờ (UTC+7)', 'datetime', None), ('status', 'Trạng thái', 'status', None)],
        headers=['Thú cưng', 'Chủ sở hữu', 'Dịch vụ', 'Ngày giờ (UTC+7)', 'Trạng thái'],
        columns=['pet_name', 'owner_name', 'service_name', 'starts_at', 'status']),
}


def connect():
    return psycopg.connect(host=os.environ['DB_HOST'], dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'], password=os.environ['DB_PASSWORD'],
        row_factory=dict_row, connect_timeout=5)


def csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_urlsafe(32)
    return session['csrf_token']


app.jinja_env.globals.update(csrf_token=csrf_token, entities=ENTITIES)


@app.before_request
def protect_post():
    if request.method == 'POST':
        expected = session.get('csrf_token', '')
        actual = request.form.get('csrf_token', '')
        if not expected or not hmac.compare_digest(expected, actual):
            abort(400, description='Phiên làm việc không hợp lệ. Hãy tải lại trang rồi thử lại.')


@app.after_request
def headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'same-origin'
    response.headers['Content-Security-Policy'] = "default-src 'self'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'"
    return response


@app.template_filter('display')
def display(value):
    if isinstance(value, datetime):
        return value.astimezone(TZ).strftime('%d/%m/%Y %H:%M')
    if isinstance(value, Decimal):
        return f'{value:,.2f}'
    return STATUSES.get(value, value) if isinstance(value, str) else value


def get_entity(slug):
    if slug not in ENTITIES:
        abort(404)
    return ENTITIES[slug]


def options(conn):
    return {
        'customer': [(r['id'], r['full_name']) for r in conn.execute('SELECT id, full_name FROM customers ORDER BY id')],
        'pet': [(r['id'], r['name'] + ' — ' + r['full_name']) for r in conn.execute('SELECT p.id, p.name, c.full_name FROM pets p JOIN customers c ON c.id=p.customer_id ORDER BY p.id')],
        'service': [(r['id'], r['name']) for r in conn.execute('SELECT id, name FROM services ORDER BY id')],
        'status': list(STATUSES.items()),
    }


def parse_values(entity, form, choices):
    values = {}
    errors = []
    for name, label, kind, limit in entity['fields']:
        raw = form.get(name, '').strip()
        try:
            if not raw:
                raise ValueError('Không được để trống.')
            if kind == 'text':
                if len(raw) > limit:
                    raise ValueError(f'Tối đa {limit} ký tự.')
                value = raw
            elif kind == 'money':
                value = Decimal(raw)
                if not value.is_finite() or value < 0 or value > Decimal('9999999999.99') or value != value.quantize(Decimal('.01')):
                    raise ValueError('Nhập giá không âm, tối đa 2 chữ số thập phân và nhỏ hơn 10 tỷ.')
            elif kind == 'integer':
                value = int(raw)
                if value < 1 or value > 2147483647:
                    raise ValueError('Nhập số nguyên dương phù hợp.')
            elif kind == 'datetime':
                value = datetime.fromisoformat(raw)
                if value.tzinfo is not None:
                    raise ValueError('Chọn ngày giờ địa phương UTC+7.')
                value = value.replace(tzinfo=TZ)
            else:
                allowed = {str(key) for key, _ in choices[kind]}
                if raw not in allowed:
                    raise ValueError('Lựa chọn không tồn tại, hãy tải lại danh sách.')
                value = raw if kind == 'status' else int(raw)
            values[name] = value
        except (ValueError, InvalidOperation, OverflowError):
            errors.append(f'{label}: giá trị không hợp lệ hoặc còn trống.')
    return values, errors


def list_rows(conn, slug, entity):
    if slug == 'thu-cung':
        return conn.execute('SELECT p.*, c.full_name AS owner_name FROM pets p JOIN customers c ON c.id=p.customer_id ORDER BY p.id DESC').fetchall()
    if slug == 'lich-hen':
        return conn.execute('SELECT a.*, p.name AS pet_name, c.full_name AS owner_name, s.name AS service_name FROM appointments a JOIN pets p ON p.id=a.pet_id JOIN customers c ON c.id=p.customer_id JOIN services s ON s.id=a.service_id ORDER BY a.starts_at DESC, a.id DESC').fetchall()
    return conn.execute(sql.SQL('SELECT * FROM {} ORDER BY id DESC').format(sql.Identifier(entity['table']))).fetchall()


@app.get('/')
def home():
    with connect() as conn:
        counts = {slug: conn.execute(sql.SQL('SELECT count(*) AS n FROM {}').format(sql.Identifier(e['table']))).fetchone()['n'] for slug, e in ENTITIES.items()}
    return render_template('home.html', counts=counts, active='home', title='Tổng quan')


@app.get('/health')
def health():
    with connect() as conn:
        conn.execute('SELECT 1')
    return {'status': 'ok', 'database': 'connected'}


@app.get('/<slug>')
def listing(slug):
    entity = get_entity(slug)
    with connect() as conn:
        rows = list_rows(conn, slug, entity)
    return render_template('list.html', entity=entity, rows=rows, slug=slug, active=slug, title=entity['title'])


@app.route('/<slug>/them', methods=['GET', 'POST'])
@app.route('/<slug>/<int:record_id>/sua', methods=['GET', 'POST'])
def edit(slug, record_id=None):
    entity = get_entity(slug)
    errors = []
    saved = False
    with connect() as conn:
        choices = options(conn)
        row = {}
        if record_id is not None:
            row = conn.execute(sql.SQL('SELECT * FROM {} WHERE id=%s').format(sql.Identifier(entity['table'])), (record_id,)).fetchone()
            if row is None:
                abort(404)
            row = dict(row)
            if slug == 'lich-hen':
                row['starts_at'] = row['starts_at'].astimezone(TZ).strftime('%Y-%m-%dT%H:%M')
        if request.method == 'POST':
            values, errors = parse_values(entity, request.form, choices)
            row = request.form.to_dict()
            if not errors:
                try:
                    keys = list(values)
                    if record_id is None:
                        query = sql.SQL('INSERT INTO {} ({}) VALUES ({})').format(sql.Identifier(entity['table']), sql.SQL(', ').join(map(sql.Identifier, keys)), sql.SQL(', ').join(sql.Placeholder() for _ in keys))
                        conn.execute(query, list(values.values()))
                    else:
                        query = sql.SQL('UPDATE {} SET {} WHERE id=%s').format(sql.Identifier(entity['table']), sql.SQL(', ').join(sql.SQL('{}=%s').format(sql.Identifier(k)) for k in keys))
                        conn.execute(query, [*values.values(), record_id])
                    saved = True
                except psycopg.IntegrityError:
                    conn.rollback()
                    errors.append('Dữ liệu liên quan đã thay đổi hoặc không hợp lệ. Hãy kiểm tra lại.')
    if saved:
        app.logger.info('DATA_CHANGE entity=%s action=%s', slug, 'create' if record_id is None else 'update')
        flash('Đã lưu ' + entity['singular'] + '.', 'success')
        return redirect(url_for('listing', slug=slug))
    return render_template('form.html', entity=entity, slug=slug, active=slug, row=row, choices=choices, errors=errors,
                           title=('Thêm ' if record_id is None else 'Sửa ') + entity['singular'], editing=record_id is not None), 422 if errors else 200


@app.post('/<slug>/<int:record_id>/xoa')
def delete(slug, record_id):
    entity = get_entity(slug)
    try:
        with connect() as conn:
            result = conn.execute(sql.SQL('DELETE FROM {} WHERE id=%s').format(sql.Identifier(entity['table'])), (record_id,))
            if result.rowcount == 0:
                abort(404)
        app.logger.info('DATA_CHANGE entity=%s action=delete', slug)
        flash('Đã xóa ' + entity['singular'] + '.', 'success')
    except psycopg.errors.ForeignKeyViolation:
        flash('Chưa thể xóa: bản ghi đang được liên kết với thú cưng hoặc lịch hẹn. Hãy kiểm tra dữ liệu liên quan trước.', 'error')
    return redirect(url_for('listing', slug=slug))


@app.errorhandler(psycopg.OperationalError)
def unavailable(error):
    app.logger.error('DATABASE_UNAVAILABLE type=%s', type(error).__name__)
    return render_template('error.html', title='Chưa kết nối được cơ sở dữ liệu', message='Vui lòng kiểm tra dịch vụ PostgreSQL và thử lại.'), 503


@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(413)
def request_error(error):
    return render_template('error.html', title='Không thể thực hiện yêu cầu', message=error.description), error.code
