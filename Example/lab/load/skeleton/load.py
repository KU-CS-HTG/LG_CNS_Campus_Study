"""
7교시 실습 · CP2 : 데이터 적재
빈칸(_____) 을 채워서 완성하세요
실행: python lab/load/skeleton/load.py
"""

import json
import psycopg
from dotenv import load_dotenv

load_dotenv()   # .env 파일이 있으면 POSTGRES_* 환경변수를 불러옵니다

# ──────────────────────────────────────────────
# 1. DB 연결
# ──────────────────────────────────────────────
conn = psycopg.connect(
    host="_____",        # localhost
    port=_____,          # 5432
    dbname="_____",      # course_db
    user="_____",        # postgres
    password="_____"     # postgres
)
cur = conn.cursor()

# ──────────────────────────────────────────────
# 2. 결과 파일 로드 (없으면 샘플 사용)
# ──────────────────────────────────────────────
import os
result_file = "result.json" if os.path.exists("result.json") else "lab/load/data/result_sample.json"
with open(result_file, encoding="utf-8") as f:
    result = json.load(f)

log_date = result["_____"]   # "log_date" 키를 채우세요
print(f"적재 대상 날짜: {log_date}")

# ──────────────────────────────────────────────
# 3. hourly_error_stats 적재
# ──────────────────────────────────────────────
inserted_hourly = 0
for hour_str, stats in result["hourly_errors"].items():
    cur.execute("""
        INSERT INTO hourly_error_stats (log_date, hour, error_count, total_count)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (log_date, hour) DO _____   -- 중복이면 무시
    """, (log_date, int(hour_str), stats["error_count"], stats["total_count"]))
    inserted_hourly += 1

print(f"hourly_error_stats: {inserted_hourly}행 시도")

# ──────────────────────────────────────────────
# 4. latency_stats 적재
# ──────────────────────────────────────────────
inserted_latency = 0
for hour_str, lats in result.get("latency", {}).items():
    cur.execute("""
        INSERT INTO latency_stats (log_date, hour, p50, p95, p99)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (log_date, hour) DO NOTHING
    """, (log_date, int(hour_str),
          lats.get("_____"),   # p50
          lats.get("p95"),
          lats.get("p99")))
    inserted_latency += 1

print(f"latency_stats: {inserted_latency}행 시도")

# ──────────────────────────────────────────────
# 5. spike_windows 적재
# ──────────────────────────────────────────────
inserted_spike = 0
for spike in result.get("spike_windows", []):
    cur.execute("""
        INSERT INTO spike_windows (log_date, start_hour, end_hour, peak_count, spike_ratio)
        VALUES (%s, %s, %s, %s, %s)
    """, (log_date,
          spike["_____"],   # start_hour
          spike["end_hour"],
          spike["peak_count"],
          spike.get("spike_ratio")))
    inserted_spike += 1

print(f"spike_windows: {inserted_spike}행 시도")

# ──────────────────────────────────────────────
# 6. 커밋 및 연결 종료
# ──────────────────────────────────────────────
conn._____()   # commit 또는 rollback
cur.close()
conn.close()
print("완료! lab/load/verify.py --cp 2 로 확인하세요")
