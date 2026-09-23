-- ============================================================
-- 7교시 실습 · CP1 : 스키마 설계
-- 실행: docker exec -i db-pg psql -U postgres -d course_db < lab/load/skeleton/schema.sql
-- 빈칸(_____)을 채워서 완성하세요
-- ============================================================

-- ① hourly_error_stats : 시간대별 에러 집계
CREATE TABLE hourly_error_stats (
    id          _____       PRIMARY KEY,          -- 자동 증가 PK
    log_date    DATE        NOT NULL,
    hour        _____       NOT NULL              -- 0~23 사이 정수
                    CHECK (hour BETWEEN _____ AND _____),
    error_count INTEGER     NOT NULL DEFAULT 0,
    total_count INTEGER     NOT NULL DEFAULT 0,
    UNIQUE (log_date, _____)                      -- 날짜+시간 조합 중복 불가
);

-- ② latency_stats : 시간대별 응답시간 백분위
CREATE TABLE latency_stats (
    id       SERIAL        PRIMARY KEY,
    log_date DATE          NOT NULL,
    hour     SMALLINT      NOT NULL
                 CHECK (hour BETWEEN 0 AND 23),
    p50      _____,                               -- NULL 허용 (ms 단위)
    p95      NUMERIC(10,2),
    p99      NUMERIC(10,2),
    UNIQUE (log_date, hour)
);

-- ③ spike_windows : 에러 급증 구간
CREATE TABLE _____ (                              -- 테이블 이름을 채우세요
    id          SERIAL       PRIMARY KEY,
    log_date    DATE         NOT NULL,
    start_hour  SMALLINT     NOT NULL,
    end_hour    SMALLINT     NOT NULL,
    peak_count  INTEGER      NOT NULL,
    spike_ratio NUMERIC(5,4)
);

-- ============================================================
-- CP1 검증 쿼리 : 세 테이블이 모두 생성됐는지 확인
-- ============================================================
SELECT table_name
FROM   information_schema.tables
WHERE  table_schema = 'public'
  AND  table_name IN ('hourly_error_stats', 'latency_stats', 'spike_windows')
ORDER BY table_name;
-- 예상 결과: 3행 (hourly_error_stats, latency_stats, spike_windows)
