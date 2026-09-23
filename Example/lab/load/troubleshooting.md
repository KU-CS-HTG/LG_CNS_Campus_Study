# PostgreSQL 실습 트러블슈팅 (7~8교시)

## 🔴 오류 1: DB 연결 실패

**증상**
```
psycopg.OperationalError: could not connect to server: Connection refused
```

**원인과 해결** (Windows cmd 기준)
```cmd
:: 컨테이너 실행 확인 (1교시에서 띄운 db-pg)
docker ps --filter name=db-pg

:: 컨테이너 자체가 없으면 1교시와 같은 방식으로 재생성
docker run -d --name db-pg -e POSTGRES_PASSWORD=postgres -p 5432:5432 -v db-pg-data:/var/lib/postgresql/data pgvector/pgvector:pg17

:: 컨테이너는 있는데 꺼져 있으면
docker start db-pg

:: course_db가 아직 없으면 생성 (재실행해도 안전)
docker exec db-pg psql -U postgres -c "SELECT 1 FROM pg_database WHERE datname='course_db'" | findstr 1 >nul || docker exec db-pg psql -U postgres -c "CREATE DATABASE course_db"

:: 재시도
python lab/load/verify.py --cp 1
```

REM ── macOS/Linux ──
REM docker ps --filter name=db-pg
REM docker run -d --name db-pg -e POSTGRES_PASSWORD=postgres -p 5432:5432 -v db-pg-data:/var/lib/postgresql/data pgvector/pgvector:pg17
REM docker start db-pg
REM docker exec db-pg psql -U postgres -c "SELECT 1 FROM pg_database WHERE datname='course_db'" | grep -q 1 || docker exec db-pg psql -U postgres -c "CREATE DATABASE course_db"
REM python lab/load/verify.py --cp 1

---

## 🔴 오류 2: 테이블이 이미 존재함

**증상**
```
ERROR: relation "hourly_error_stats" already exists
```

**해결법 A**: 기존 테이블 삭제 후 재생성
```sql
DROP TABLE IF EXISTS hourly_error_stats CASCADE;
DROP TABLE IF EXISTS latency_stats CASCADE;
DROP TABLE IF EXISTS spike_windows CASCADE;
```
그 후 `schema.sql` 다시 실행.

**해결법 B**: `CREATE TABLE IF NOT EXISTS` 사용 (부분 적용)
```sql
CREATE TABLE IF NOT EXISTS hourly_error_stats (...);
```

---

## 🔴 오류 3: UNIQUE 위반

**증상**
```
ERROR: duplicate key value violates unique constraint "hourly_error_stats_log_date_hour_key"
```

**원인**: `load.py`를 두 번 이상 실행했거나 `ON CONFLICT` 구문이 빠진 경우.

**해결**: `load.py`의 INSERT 구문에 `ON CONFLICT (log_date, hour) DO NOTHING` 추가 확인.
```sql
INSERT INTO hourly_error_stats (log_date, hour, error_count, total_count)
VALUES (%s, %s, %s, %s)
ON CONFLICT (log_date, hour) DO NOTHING;   ← 이 줄이 있어야 합니다
```

---

## 🔴 오류 4: CHECK 제약 위반

**증상**
```
ERROR: new row for relation "hourly_error_stats" violates check constraint
"hourly_error_stats_hour_check"
```

**원인**: `hour` 값이 0~23 범위를 벗어남. JSON에서 hour를 `int`로 변환하지 않은 경우.

**해결**:
```python
# ❌ 잘못됨
cur.execute("INSERT INTO ... VALUES (%s, %s, ...)", (log_date, hour_str, ...))

# ✅ 올바름
cur.execute("INSERT INTO ... VALUES (%s, %s, ...)", (log_date, int(hour_str), ...))
```

---

## 🔴 오류 5: psycopg 가 설치되지 않음

**증상**
```
ModuleNotFoundError: No module named 'psycopg'
```

**해결**: 오늘은 `psycopg` **v3**를 씁니다 (1교시와 동일 — 과거의 `psycopg2`와는 다른 패키지입니다). (Windows는 보통 아래 첫 줄이면 충분합니다)
```cmd
pip install "psycopg[binary]==3.3.4" python-dotenv

REM ── macOS/Linux (시스템 파이썬이 externally-managed면 --break-system-packages 필요) ──
REM pip install "psycopg[binary]==3.3.4" python-dotenv --break-system-packages
```

---

## 🟡 경고 1: verify.py --cp 3 실패 (에러율 기대값 불일치)

**증상**
```
❌ 최대 에러율: 3시 = 8.5% (기대 ≥ 10%)
```

**원인**: 본인의 이전 로그 분석 실습 결과와 샘플 데이터가 다를 수 있음. 본인 데이터를 쓰는 경우 정상.

**해결**: `verify.py` 상단의 기대값을 본인 데이터에 맞게 조정하거나, `result_sample.json` 사용.
```python
# verify.py 내 check_cp3 함수의 기대값 조정
ok = rate >= 10.0   # ← 본인 데이터의 최대 에러율에 맞게 수정
```

---

## 🟡 경고 2: CP4에서 p95 값이 None

**증상**
```
⚠️ 3시 p95 = None ms
```

**원인**: `latency_stats`에 데이터가 없거나 `result.json`에 `latency` 키가 없음.

**해결**: `result_sample.json`에는 `latency` 섹션이 있는지 확인. (아래 명령은 Windows·macOS·Linux 모두 동일합니다 — 순수 파이썬 명령이라 OS 차이가 없습니다)
```
python -c "import json; d=json.load(open('lab/load/data/result_sample.json')); print('latency' in d)"
# True 가 나와야 함
```

---

## 🟡 경고 3: 스키마가 있는데 verify.py가 CP1 실패

**원인**: 다른 데이터베이스에 생성된 경우.

**확인**:
```sql
\dt                        -- 현재 연결된 DB의 테이블 목록
SELECT current_database(); -- 현재 연결된 DB
```

`course_db`가 아닌 `postgres` DB에 연결된 경우 `-d course_db` 옵션 추가.

---

## 도움 요청 전 체크리스트

1. `docker ps --filter name=db-pg` → 컨테이너 실행 중?
2. `docker exec db-pg psql -U postgres -d course_db -c "\dt"` → 테이블 목록 확인?
3. `python lab/load/verify.py --cp 1` → 어떤 오류 메시지가 나오는가?
4. 오류 메시지를 복사해서 강사 또는 옆 팀원에게 보여주세요.
