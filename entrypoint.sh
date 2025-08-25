#!/usr/bin/env bash
set -e

if [ -n "$DB_HOST" ]; then
  echo "Waiting for database at $DB_HOST:$DB_PORT..."
  until python - <<'PY'
import os, socket, time
host=os.getenv("DB_HOST","db"); port=int(os.getenv("DB_PORT","5432"))
s=socket.socket(); s.settimeout(1)
for _ in range(60):
    try:
        s.connect((host,port)); s.close(); break
    except Exception:
        time.sleep(1)
else:
    raise SystemExit("DB not reachable")
PY
  do
    sleep 1
  done
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
