#!/usr/bin/env bash
# Chay tu thu muc goc du an. Chi tao tai khoan thong ke, khong sua du lieu nghiep vu.
set -euo pipefail
set -a
source .env
set +a
docker compose exec -T -e MONITOR_DB_USER -e MONITOR_DB_PASSWORD db sh -c 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" --set=monitor_user="$MONITOR_DB_USER" --set=monitor_password="$MONITOR_DB_PASSWORD"' <<'SQL'
SELECT format('CREATE ROLE %I LOGIN PASSWORD %L', :'monitor_user', :'monitor_password')
WHERE NOT EXISTS (SELECT FROM pg_roles WHERE rolname = :'monitor_user')
\gexec
GRANT pg_monitor TO :"monitor_user";
SELECT format('GRANT CONNECT ON DATABASE %I TO %I', current_database(), :'monitor_user')
\gexec
SQL
