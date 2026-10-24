#!/usr/bin/env python3
"""Kiem chung chi doc; khong in mat khau, khong ghi du lieu nghiep vu."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--section', choices=['all', 'app', 'network', 'db', 'http', 'secrets'], default='all')
section = parser.parse_args().section
failures = []


def run(*args):
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def check(label, passed):
    print(('[PASS] ' if passed else '[FAIL] ') + label)
    if not passed:
        failures.append(label)


def inspect(service):
    cid = run('docker', 'compose', 'ps', '-q', service)
    if not cid:
        raise RuntimeError('Service not running: ' + service)
    return json.loads(run('docker', 'inspect', cid))[0]


env = dict(line.split('=', 1) for line in (ROOT / '.env').read_text().splitlines()
           if '=' in line and not line.startswith('#'))

if section in ('all', 'app'):
    app = inspect('app')
    host = app['HostConfig']
    uid = run('docker', 'compose', 'exec', '-T', 'app', 'id', '-u')
    print('APP UID:', uid)
    check('App runs as UID 10001, not root', uid == '10001')
    check('App root filesystem is read-only', host['ReadonlyRootfs'])
    check('App drops ALL Linux capabilities', 'ALL' in host.get('CapDrop', []))
    check('App prevents privilege escalation', 'no-new-privileges:true' in host.get('SecurityOpt', []))
    tmp = host.get('Tmpfs', {}).get('/tmp', '')
    check('App /tmp has noexec, nosuid and size limit', all(x in tmp for x in ['noexec', 'nosuid', 'size=16m']))
    for service in ['prometheus', 'grafana', 'nginx-exporter', 'postgres-exporter', 'loki', 'promtail']:
        h = inspect(service)['HostConfig']
        check(service + ' drops ALL capabilities and prevents privilege escalation',
              'ALL' in h.get('CapDrop', []) and 'no-new-privileges:true' in h.get('SecurityOpt', []))

if section in ('all', 'network'):
    db = inspect('db')
    app = inspect('app')
    nginx = inspect('nginx')
    dbnet = 'dtc245200404-de28_db_net'
    net = json.loads(run('docker', 'network', 'inspect', dbnet))[0]
    check('Database network is internal', net['Internal'])
    check('Database has no host port binding', not db['HostConfig'].get('PortBindings'))
    check('App has no host port binding', not app['HostConfig'].get('PortBindings'))
    check('Nginx is not connected to DB network', dbnet not in nginx['NetworkSettings']['Networks'])
    for service in ['nginx', 'pgadmin', 'prometheus', 'grafana', 'loki']:
        bindings = inspect(service)['HostConfig'].get('PortBindings', {})
        check(service + ' publishes only on 127.0.0.1', bool(bindings) and
              all(b['HostIp'] == '127.0.0.1' for group in bindings.values() for b in group))

if section in ('all', 'db'):
    for key in ['APP_DB_USER', 'MONITOR_DB_USER', 'POSTGRES_USER', 'POSTGRES_DB']:
        if not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*', env[key]):
            raise ValueError('Invalid identifier: ' + key)
    app_user = env['APP_DB_USER']
    monitor = env['MONITOR_DB_USER']
    query = f"""SELECT json_build_object(
      'app_unprivileged', (SELECT NOT rolsuper AND NOT rolcreatedb AND NOT rolcreaterole FROM pg_roles WHERE rolname='{app_user}'),
      'app_no_schema_create', NOT has_schema_privilege('{app_user}', 'public', 'CREATE'),
      'app_crud', (SELECT bool_and(has_table_privilege('{app_user}', tablename, 'SELECT') AND has_table_privilege('{app_user}', tablename, 'INSERT') AND has_table_privilege('{app_user}', tablename, 'UPDATE') AND has_table_privilege('{app_user}', tablename, 'DELETE')) FROM pg_tables WHERE schemaname='public'),
      'monitor_stats', pg_has_role('{monitor}', 'pg_monitor', 'MEMBER'),
      'monitor_unprivileged', (SELECT NOT rolsuper AND NOT rolcreatedb AND NOT rolcreaterole FROM pg_roles WHERE rolname='{monitor}'),
      'monitor_no_business_access', (SELECT bool_and(NOT has_table_privilege('{monitor}', tablename, 'SELECT,INSERT,UPDATE,DELETE')) FROM pg_tables WHERE schemaname='public'),
      'customers', (SELECT count(*) FROM customers),
      'pets', (SELECT count(*) FROM pets),
      'services', (SELECT count(*) FROM services),
      'appointments', (SELECT count(*) FROM appointments));"""
    result = json.loads(run('docker', 'compose', 'exec', '-T', 'db', 'psql', '-X', '-U', env['POSTGRES_USER'], '-d', env['POSTGRES_DB'], '-At', '-c', query))
    print('APP DB ROLE:', app_user, '| MONITOR ROLE:', monitor)
    for key in ['app_unprivileged', 'app_no_schema_create', 'app_crud', 'monitor_stats', 'monitor_unprivileged', 'monitor_no_business_access']:
        check(key, result[key] is True)
    print('READ-ONLY COUNTS:', {k: result[k] for k in ['customers', 'pets', 'services', 'appointments']})

if section in ('all', 'http'):
    required = {'X-Content-Type-Options': 'nosniff', 'X-Frame-Options': 'DENY', 'Referrer-Policy': 'same-origin'}
    for path, expected in [('/health', 200), ('/.env', 403), ('/.git/config', 403), ('/khong-ton-tai', 404)]:
        try:
            response = urllib.request.urlopen('http://127.0.0.1:8088' + path, timeout=10)
        except urllib.error.HTTPError as error:
            response = error
        print('HTTP', path, response.code)
        check(path + ' expected status', response.code == expected)
        check(path + ' basic security headers', all(response.headers.get(k) == v for k, v in required.items()) and "default-src 'self'" in response.headers.get('Content-Security-Policy', ''))
        check(path + ' hides Nginx version', response.headers.get('Server') == 'nginx')
        response.close()

if section in ('all', 'secrets'):
    keys = ['POSTGRES_PASSWORD', 'APP_DB_PASSWORD', 'PGADMIN_DEFAULT_PASSWORD', 'MONITOR_DB_PASSWORD', 'GRAFANA_ADMIN_PASSWORD', 'SECRET_KEY']
    values = [env.get(k, '') for k in keys]
    check('Each password/key has at least 16 characters', all(len(v) >= 16 for v in values))
    check('Passwords/keys are distinct', len(set(values)) == len(values))
    check('.env is ignored by Git', bool(run('git', 'check-ignore', '.env')))
    check('.env is not tracked by Git', not run('git', 'ls-files', '--', '.env'))
    print('Secret values are intentionally not printed. Length checks do not prove complete password security.')

print('RESULT:', 'PASS' if not failures else 'FAIL')
raise SystemExit(1 if failures else 0)
