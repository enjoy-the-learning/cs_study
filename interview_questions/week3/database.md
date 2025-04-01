# 3주차 데이터 베이스 질문 내용

##### 1. 인덱스가 성능을 오히려 떨어뜨릴 수 있는 경우는 언제인가요?

- 선택도 낮은 컬럼일 때 (예: 성별, 상태값)

- Index-only scan이 불가능할 때 (인덱스에 없는 컬럼 SELECT)

- 인덱스 단편화로 탐색 비용 증가

- 인덱스가 너무 많으면 DML 성능 저하 (쓰기 시 갱신 오버헤드)



##### 2. EXPLAIN PLAN은 어떻게 해석하나요? 실제 쿼리 실행 순서와 실행 방식은?

- 트리 구조 아래에서 위로 읽는다

- 실행 노드: Seq Scan, Index Scan, Nested Loop, Hash Join 등

- 실제 쿼리 순서 = Bottom-up

- cost, rows, filter, index cond, execution time 등을 체크

- EXPLAIN (ANALYZE)로 실제 실행 시간 + 버퍼 읽기까지 확인


##### 3. RDB와 DWH의 차이는? OLTP vs OLAP 관점에서 어떻게 설계가 달라지나요?

- OLTP (RDB)
    - 목적: 서비스 처리
    - 구조: 정규화
    - 사용: INSERT/UPDATE, 트랜잭션
    - 예시: PostgreSQL, MySQL
    - OLTP는 정확하고 빠른 트랜잭션에 최적화

- OLAP (DWH)
    - 목적: 데이터 분석
    - 구조: 비정규화
    - 사용: SELECT + GROUP BY, 집계
    - 예시: BigQuery, Redshift
    - OLAP은 대량 분석에 최적화


##### 4. 스키마 변경 시 무중단 마이그레이션을 어떻게 설계할 수 있나요?

- 컬럼 추가는 nullable로 먼저 적용

- 백엔드 코드에서 새 컬럼을 읽고 쓰도록 수정

- 백필은 배치로 천천히 처리

- 이후에 NOT NULL 제약, 기존 컬럼 삭제 등 단계별 적용

- Zero-downtime 유지 위해 점진적 마이그레이션 필수 → lock 방지, backward compatibility, 트래픽 고려가 핵심


##### 5. 쿼리가 느릴 때 성능 분석은 어디서부터 시작하나요?

- EXPLAIN (ANALYZE)로 실행 계획 확인

- Seq Scan → 인덱스 미사용 여부 확인

- Index Scan이더라도 느리면 선택도, Filter 조건 확인

- Join 방식 확인 (Nested Loop vs Hash Join)

- 실제 execution time, rows, buffers 등을 통해 병목 지점 파악 → 쿼리 튜닝은 데이터 양 + 실행 방식 + 인덱스 관점에서 함께 봐야 함
