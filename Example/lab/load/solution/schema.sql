-- ============================================================
-- 7교시 실습 · CP1 : 스키마 설계 — 완성본
-- ============================================================

-- ① hourly_error_stats : 시간대별 에러 집계
CREATE TABLE hourly_error_stats (
    id          SERIAL      PRIMARY KEY,
    log_date    DATE        NOT NULL,
    hour        SMALLINT    NOT NULL
                    CHECK (hour BETWEEN 0 AND 23),
    error_count INTEGER     NOT NULL DEFAULT 0,
    total_count INTEGER     NOT NULL DEFAULT 0,
    UNIQUE (log_date, hour)
);

-- ② latency_stats : 시간대별 응답시간 백분위
CREATE TABLE latency_stats (
    id       SERIAL        PRIMARY KEY,
    log_date DATE          NOT NULL,
    hour     SMALLINT      NOT NULL
                 CHECK (hour BETWEEN 0 AND 23),
    p50      NUMERIC(10,2),
    p95      NUMERIC(10,2),
    p99      NUMERIC(10,2),
    UNIQUE (log_date, hour)
);

-- ③ spike_windows : 에러 급증 구간
CREATE TABLE spike_windows (
    id          SERIAL       PRIMARY KEY,
    log_date    DATE         NOT NULL,
    start_hour  SMALLINT     NOT NULL,
    end_hour    SMALLINT     NOT NULL,
    peak_count  INTEGER      NOT NULL,
    spike_ratio NUMERIC(5,4)
);

-- CP1 검증
SELECT table_name
FROM   information_schema.tables
WHERE  table_schema = 'public'
  AND  table_name IN ('hourly_error_stats', 'latency_stats', 'spike_windows')
ORDER BY table_name;
