#!/usr/bin/env python3
"""
PostgreSQL 실습 검증 스크립트 (7~8교시 · CP1~CP4)
사용법:
  python lab/load/verify.py --cp 1    # CP1만 검증
  python lab/load/verify.py --cp 2    # CP1~CP2 검증
  python lab/load/verify.py           # 전체 (CP1~CP4) 검증
"""

import os
import sys
import argparse
import psycopg
from dotenv import load_dotenv

load_dotenv()   # .env 파일이 있으면 POSTGRES_* 환경변수를 불러옵니다

# ──────────────────────────────────────────────
# DB 연결 설정 (.env 로 덮어쓸 수 있음, 없으면 기본값 사용)
# ──────────────────────────────────────────────
DB_CONFIG = dict(
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=int(os.getenv("POSTGRES_PORT", "5432")),
    dbname=os.getenv("POSTGRES_DB", "course_db"),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "postgres"),
)
LOG_DATE = "2016-11-09"

PASS = "✅"
FAIL = "❌"


def connect():
    try:
        return psycopg.connect(**DB_CONFIG)
    except psycopg.OperationalError as e:
        print(f"{FAIL} DB 연결 실패: {e}")
        print("   PostgreSQL 컨테이너(db-pg)가 실행 중인지, 연결 정보가 맞는지 확인하세요.")
        sys.exit(1)


# ──────────────────────────────────────────────
# CP1: 세 테이블이 모두 존재하는가
# ──────────────────────────────────────────────
def check_cp1(cur) -> bool:
    print("\n[CP1] 테이블 생성 확인")
    required = {"hourly_error_stats", "latency_stats", "spike_windows"}
    cur.execute("""
        SELECT table_name
        FROM   information_schema.tables
        WHERE  table_schema = 'public'
          AND  table_name = ANY(%s)
    """, (list(required),))
    found = {row[0] for row in cur.fetchall()}
    missing = required - found

    for tbl in sorted(required):
        icon = PASS if tbl in found else FAIL
        print(f"  {icon} {tbl}")

    if missing:
        print(f"  → 누락 테이블: {', '.join(sorted(missing))}")
        print("    schema.sql 을 다시 실행하세요.")
        return False
    print(f"  → CP1 통과 {PASS}")
    return True


# ──────────────────────────────────────────────
# CP2: 적재 행 수 확인
# ──────────────────────────────────────────────
def check_cp2(cur) -> bool:
    print("\n[CP2] 데이터 적재 확인")
    checks = [
        ("hourly_error_stats", 24, "SELECT COUNT(*) FROM hourly_error_stats WHERE log_date = %s"),
        ("latency_stats",      24, "SELECT COUNT(*) FROM latency_stats      WHERE log_date = %s"),
        ("spike_windows",       1, "SELECT COUNT(*) FROM spike_windows      WHERE log_date = %s"),
    ]
    all_ok = True
    for tbl, expected_min, sql in checks:
        try:
            cur.execute(sql, (LOG_DATE,))
            cnt = cur.fetchone()[0]
            ok = cnt >= expected_min
            icon = PASS if ok else FAIL
            print(f"  {icon} {tbl}: {cnt}행 (기대 ≥ {expected_min})")
            if not ok:
                all_ok = False
        except psycopg.Error as e:
            print(f"  {FAIL} {tbl} 조회 오류: {e}")
            all_ok = False

    if all_ok:
        print(f"  → CP2 통과 {PASS}")
    else:
        print("    load.py 를 다시 실행하세요.")
    return all_ok


# ──────────────────────────────────────────────
# CP3: 최대 에러율이 10% 이상인가 (03시 급증 반영)
# ──────────────────────────────────────────────
def check_cp3(cur) -> bool:
    print("\n[CP3] 시간대별 에러율 조회 확인")
    cur.execute("""
        SELECT
            hour,
            ROUND(error_count::NUMERIC / NULLIF(total_count, 0) * 100, 2) AS rate
        FROM   hourly_error_stats
        WHERE  log_date = %s
        ORDER BY rate DESC
        LIMIT 1
    """, (LOG_DATE,))
    row = cur.fetchone()
    if row is None:
        print(f"  {FAIL} 데이터 없음 — CP2를 먼저 완료하세요")
        return False

    hour, rate = row
    ok = rate >= 10.0
    icon = PASS if ok else FAIL
    print(f"  {icon} 최대 에러율: {hour}시 = {rate}% (기대 ≥ 10%)")
    if ok:
        print(f"  → CP3 통과 {PASS}")
    else:
        print("    queries.py 의 ORDER BY, LIMIT 를 확인하세요.")
    return ok


# ──────────────────────────────────────────────
# CP4: spike_windows JOIN latency_stats 가 작동하는가
# ──────────────────────────────────────────────
def check_cp4(cur) -> bool:
    print("\n[CP4] JOIN 쿼리 확인 (급증 구간 + 응답시간)")
    cur.execute("""
        SELECT
            s.start_hour,
            l.hour,
            l.p95
        FROM   spike_windows s
        JOIN   latency_stats l
            ON s.log_date = l.log_date
           AND l.hour BETWEEN s.start_hour AND s.end_hour
        WHERE  s.log_date = %s
          AND  s.start_hour = 3        -- 03시 급증 구간
        ORDER BY l.hour
    """, (LOG_DATE,))
    rows = cur.fetchall()

    if not rows:
        print(f"  {FAIL} 결과 없음 — JOIN 조건이나 적재 데이터를 확인하세요")
        return False

    ok = True
    for (start_hour, hour, p95) in rows:
        high_latency = p95 is not None and p95 > 100
        icon = PASS if high_latency else "⚠️"
        print(f"  {icon} {hour}시 p95 = {p95}ms")
        if not high_latency:
            ok = False

    if ok:
        print(f"  → CP4 통과 {PASS}")
    else:
        print("    03시 p95가 100ms 이상이어야 합니다. latency 데이터를 확인하세요.")
    return ok


# ──────────────────────────────────────────────
# 메인
# ──────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="PostgreSQL 실습 검증 (CP1~CP4)")
    parser.add_argument("--cp", type=int, choices=[1, 2, 3, 4],
                        help="검증할 체크포인트 번호 (기본: 전체)")
    args = parser.parse_args()

    max_cp = args.cp if args.cp else 4

    conn = connect()
    cur = conn.cursor()

    results = []
    checkers = [check_cp1, check_cp2, check_cp3, check_cp4]

    for i, fn in enumerate(checkers[:max_cp], start=1):
        ok = fn(cur)
        results.append((i, ok))
        if not ok:
            break  # 순서대로 — 앞 CP가 실패하면 다음은 의미 없음

    cur.close()
    conn.close()

    print("\n" + "=" * 40)
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    print(f"결과: {passed}/{total} 통과")
    if passed == total == max_cp:
        print(f"{PASS} 모든 체크포인트 통과!")
    else:
        first_fail = next((i for i, ok in results if not ok), None)
        if first_fail:
            print(f"{FAIL} CP{first_fail}에서 중단 — 위 안내를 따라 수정하세요")
    print("=" * 40)


if __name__ == "__main__":
    main()
