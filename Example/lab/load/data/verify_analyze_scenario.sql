-- ============================================================
-- 6교시 실습 · ANALYZE 드리프트 시나리오 실측
-- 실행: docker exec -i db-pg psql -U postgres -d course_db < lab/load/data/verify_analyze_scenario.sql
-- 전제: lab/load/data/init_log_events.sql 을 먼저 실행해 log_events가 있어야 합니다
-- ============================================================

\echo '=== ANALYZE 전 — 대량 INSERT 직후 실행 계획 (통계가 낡은 상태) ==='

INSERT INTO log_events (log_date, created_at, hour, level, error_count, server_id, latency_ms)
SELECT
    '2016-11-10'::DATE,
    '2016-11-10'::TIMESTAMP + (random() * INTERVAL '24 hours'),
    (random() * 23)::SMALLINT,
    CASE WHEN random() < 0.015 THEN 'ERROR' ELSE 'INFO' END,
    CASE WHEN random() < 0.015 THEN (random() * 100)::INTEGER ELSE 0 END,
    (random() * 10)::INTEGER + 1,
    (random() * 50 + 5)::NUMERIC(10,2)
FROM generate_series(1, 500000);

EXPLAIN ANALYZE
SELECT * FROM log_events WHERE hour = 3;

\echo ''
\echo '→ 예측 rows 와 실제 rows 차이를 확인하세요 (예측이 크게 낮다면 통계가 오래된 것입니다)'
\echo ''
\echo '=== ANALYZE 후 — 같은 쿼리 재실행 ==='

ANALYZE log_events;

EXPLAIN ANALYZE
SELECT * FROM log_events WHERE hour = 3;

\echo ''
\echo '→ 예측 rows가 실제 rows에 가까워졌는지 확인하세요'
