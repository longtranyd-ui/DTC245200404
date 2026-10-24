#!/usr/bin/env python3
"""Tao hai tai khoan ky thuat cuc bo, khong ket noi DB, khong in mat khau."""
import hashlib
import json
from pathlib import Path
import secrets

root = Path(__file__).resolve().parents[1]
envfile = root / '.env'
text = envfile.read_text(encoding='utf-8')
lines = text.splitlines()
env = dict(line.split('=', 1) for line in lines if '=' in line and not line.startswith('#'))
hash_keys = ['WEB_ADMIN_PASSWORD_HASH', 'WEB_STAFF_PASSWORD_HASH']
configured = [bool(env.get(k, '').strip("'\"")) for k in hash_keys]
if all(configured):
    print('Tai khoan web da cau hinh; giu nguyen hash va mat khau hien co.')
    raise SystemExit(0)
if any(configured):
    raise SystemExit('Cau hinh web chua dong bo. Khong tu ghi de; hay kiem tra .env.')
credentials_file = root / '.web-credentials'
if credentials_file.exists():
    raise SystemExit('.web-credentials da ton tai. Khong ghi de mat khau.')
users = [env.get('WEB_ADMIN_USER') or 'admin', env.get('WEB_STAFF_USER') or 'nhanvien']
if users[0] == users[1] or any(not u.isascii() or not u.replace('_', '').isalnum() for u in users):
    raise SystemExit('Ten tai khoan phai rieng biet va gom chu/so/gach duoi ASCII.')
updates = {'WEB_ADMIN_USER': users[0], 'WEB_STAFF_USER': users[1]}
credentials = {}
for name, key, role in zip(users, hash_keys, ['admin', 'staff']):
    password = secrets.token_urlsafe(24)
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 600000).hex()
    updates[key] = "'pbkdf2:sha256:600000$" + salt + '$' + digest + "'"
    credentials[role] = {'username': name, 'password': password}
with credentials_file.open('x', encoding='utf-8') as output:
    json.dump(credentials, output, indent=2)
    output.write('\n')
present = set()
for i, line in enumerate(lines):
    key = line.split('=', 1)[0]
    if key in updates:
        lines[i] = key + '=' + updates[key]
        present.add(key)
lines.extend(k + '=' + v for k, v in updates.items() if k not in present)
envfile.write_bytes(('\n'.join(lines) + '\n').encode('utf-8'))
print('Da tao 2 tai khoan. Hash o .env; thong tin dang nhap o .web-credentials cuc bo.')
print('Khong commit hoac chup hai file nay. Mat khau khong duoc in ra terminal.')
