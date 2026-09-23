-- ============================================================
-- 6교시 실습 준비 · log_events 테이블 생성 + 100만 행 적재
-- 실행: docker exec -i db-pg psql -U postgres -d course_db < lab/load/data/init_log_events.sql
-- 소요 시간: 약 1~2분. 1교시에서 띄운 db-pg 컨테이너 안의 psql을 그대로 씁니다.
-- ============================================================

DROP TABLE IF EXISTS log_events;

CREATE TABLE log_events (
    id          BIGSERIAL   PRIMARY KEY,
    log_date    DATE        NOT NULL,
    created_at  TIMESTAMP   NOT NULL,
    hour        SMALLINT    NOT NULL CHECK (hour BETWEEN 0 AND 23),
    level       VARCHAR(10) NOT NULL,
    error_count INTEGER     NOT NULL DEFAULT 0,
    server_id   INTEGER     NOT NULL,
    latency_ms  NUMERIC(10,2)
);

-- 100만 행 생성 (03시 집중 에러 급증을 시뮬레이션 — 가설 1·2·3 검증용)
INSERT INTO log_events (log_date, created_at, hour, level, error_count, server_id, latency_ms)
SELECT
    '2016-11-09'::DATE,
    '2016-11-09'::TIMESTAMP + (random() * INTERVAL '24 hours'),
    EXTRACT(HOUR FROM '2016-11-09'::TIMESTAMP + (random() * INTERVAL '24 hours'))::SMALLINT,
    CASE
        WHEN gs <= 2571 THEN 'ERROR'          -- 03시 급증 시뮬레이션 (약 41,000 ~ 62,000)
        WHEN random() < 0.015 THEN 'ERROR'
        ELSE 'INFO'
    END,
    CASE WHEN random() < 0.015 THEN (random() * 100)::INTEGER ELSE 0 END,
    (random() * 10)::INTEGER + 1,
    CASE
        WHEN random() < 0.015 THEN (random() * 900 + 100)::NUMERIC(10,2)
        ELSE (random() * 50 + 5)::NUMERIC(10,2)
    END
FROM generate_series(1, 1000000) gs;

CREATE INDEX idx_log_events_hour        ON log_events (hour);
CREATE INDEX idx_log_events_created_at  ON log_events (created_at);
CREATE INDEX idx_log_events_error_count ON log_events (error_count);

ANALYZE log_events;

-- 확인: SELECT COUNT(*) FROM log_events;  → 1,000,000행이 나오면 성공
