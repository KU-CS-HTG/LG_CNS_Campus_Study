# PostgreSQL 실습 체크포인트 가이드 (7~8교시)

## 체크포인트 개요

| CP | 내용 | 확인 방법 | 예상 소요 |
|---|---|---|---|
| CP1 | 세 테이블 생성 완료 | `verify.py --cp 1` | 5분 |
| CP2 | 이전 로그 분석 실습 결과 적재 | `verify.py --cp 2` | 10분 |
| CP3 | 에러율 상위 쿼리 완성 | `verify.py --cp 3` | 8분 |
| CP4 | JOIN 쿼리 완성 | `verify.py --cp 4` | 10분 |

## 실행 방법

```bash
# PostgreSQL 컨테이너 확인 (1교시에서 띄운 db-pg)
docker ps --filter name=db-pg

# 1. 스키마 생성 (schema.sql 빈칸 채운 후)
docker exec -i db-pg psql -U postgres -d course_db < lab/load/skeleton/schema.sql

# CP1 확인
python lab/load/verify.py --cp 1

# 2. 데이터 적재 (load.py 빈칸 채운 후)
python lab/load/skeleton/load.py

# CP2 확인
python lab/load/verify.py --cp 2

# 3. 조회 쿼리 (queries.py 빈칸 채운 후)
python lab/load/skeleton/queries.py

# CP3, CP4 확인
python lab/load/verify.py --cp 3
python lab/load/verify.py --cp 4

# 전체 한번에
python lab/load/verify.py
```

## 빈칸 힌트 요약

### schema.sql
- `_____` (PK 타입) → `SERIAL`
- `_____` (시간 타입) → `SMALLINT`
- `CHECK (hour BETWEEN _____ AND _____)` → `0 AND 23`
- `UNIQUE (log_date, _____)` → `hour`
- 세 번째 테이블 이름 → `spike_windows`

### load.py
- DB 연결 정보: `host="localhost"`, `port=5432`, `dbname="course_db"`, `user="postgres"`, `password="postgres"`
- `result["_____"]` → `"log_date"`
- `ON CONFLICT ... DO _____` → `NOTHING`
- `lats.get("_____")` → `"p50"`
- `spike["_____"]` → `"start_hour"`
- `conn._____()` → `commit`

### queries.py
- `NULLIF(total_count, _____)` → `0`
- `ORDER BY error_rate_pct _____` → `DESC`
- `LIMIT _____` → `5`
- `_____ latency_stats l` → `JOIN` 또는 `INNER JOIN`
- `s.end_hour AND s._____` → `end_hour`

## 막혔을 때

→ `lab/load/troubleshooting.md` 참조
→ 그래도 막히면 `lab/load/solution/` 폴더의 완성 파일 참조
