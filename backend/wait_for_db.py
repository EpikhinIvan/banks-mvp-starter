import os, time, sys
import psycopg2

host = os.environ.get("DB_HOST","db")
port = int(os.environ.get("DB_PORT","5432"))
name = os.environ.get("DB_NAME","banks")
user = os.environ.get("DB_USER","banks")
password = os.environ.get("DB_PASSWORD","banks")

for i in range(60):
    try:
        conn = psycopg2.connect(host=host, port=port, dbname=name, user=user, password=password)
        conn.close()
        print("Database is ready")
        sys.exit(0)
    except Exception as e:
        print(f"Waiting for database... ({i+1}/60)")
        time.sleep(1)
print("Database not ready in time", file=sys.stderr)
sys.exit(1)
