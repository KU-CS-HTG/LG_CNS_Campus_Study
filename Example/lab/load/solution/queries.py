"""8교시 실습 · CP3·CP4 : 기본 조회 쿼리 — 완성본"""

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
LOG_DATE = "2016-11-09"

print("=" * 50)
print("CP3: 시간대별 에러율 상위 5개")
print("=" * 50)
cur.execute("""
    SELECT
        hour,
        error_count,
        total_count,
        ROUND(error_count::NUMERIC / NULLIF(total_count, 0) * 100, 2) AS error_rate_pct
    FROM   hourly_error_stats
    WHERE  log_date = %s
    ORDER BY error_rate_pct DESC
    LIMIT 5
""", (LOG_DATE,))
for row in cur.fetchall():
    hour, error_count, total_count, error_rate_pct = row
    print(f"  {hour:>2}시 | 에러율 {error_rate_pct:>6}%"
          f" | 에러 {error_count:>7,}건 / 전체 {total_count:>7,}건")

print()
print("=" * 50)
print("CP4: 에러 급증 구간 + 응답시간")
print("=" * 50)
cur.execute("""
    SELECT
        s.start_hour,
        s.end_hour,
        s.peak_count,
        ROUND(s.spike_ratio * 100, 2) AS spike_rate_pct,
        l.hour,
        l.p50,
        l.p95,
        l.p99
    FROM   spike_windows s
    JOIN   latency_stats l
        ON s.log_date = l.log_date
       AND l.hour BETWEEN s.start_hour AND s.end_hour
    WHERE  s.log_date = %s
    ORDER BY s.start_hour, l.hour
""", (LOG_DATE,))
for row in cur.fetchall():
    start_hour, end_hour, peak_count, spike_rate_pct, hour, p50, p95, p99 = row
    print(f"  {start_hour}~{end_hour}시 급증"
          f" (에러율 {spike_rate_pct}%)"
          f" | {hour}시 p50={p50}ms p95={p95}ms p99={p99}ms")

cur.close()
conn.close()
