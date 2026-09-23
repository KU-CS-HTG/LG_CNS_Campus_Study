"""7교시 실습 · CP2 : 데이터 적재 — 완성본"""

import json
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

conn = psycopg.connect(
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=int(os.getenv("POSTGRES_PORT", "5432")),
    dbname=os.getenv("POSTGRES_DB", "course_db"),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "postgres"),
)
cur = conn.cursor()

result_file = "result.json" if os.path.exists("result.json") else "lab/load/data/result_sample.json"
with open(result_file, encoding="utf-8") as f:
    result = json.load(f)

log_date = result["log_date"]
print(f"적재 대상 날짜: {log_date}")

for hour_str, stats in result["hourly_errors"].items():
    cur.execute("""
        INSERT INTO hourly_error_stats (log_date, hour, error_count, total_count)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (log_date, hour) DO NOTHING
    """, (log_date, int(hour_str), stats["error_count"], stats["total_count"]))

for hour_str, lats in result.get("latency", {}).items():
    cur.execute("""
        INSERT INTO latency_stats (log_date, hour, p50, p95, p99)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (log_date, hour) DO NOTHING
    """, (log_date, int(hour_str),
          lats.get("p50"), lats.get("p95"), lats.get("p99")))

for spike in result.get("spike_windows", []):
    cur.execute("""
        INSERT INTO spike_windows (log_date, start_hour, end_hour, peak_count, spike_ratio)
        VALUES (%s, %s, %s, %s, %s)
    """, (log_date,
          spike["start_hour"], spike["end_hour"],
          spike["peak_count"], spike.get("spike_ratio")))

conn.commit()
cur.close()
conn.close()
print("적재 완료! lab/load/verify.py --cp 2 로 확인하세요")
