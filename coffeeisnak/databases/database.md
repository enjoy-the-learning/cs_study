# 데이터 베이스 CS 질문 공부


### 1. DB 기본 개념

##### 1 - 1. RDB와 NoSQL 차이는? 언제 어떤 DB를 쓰는 게 적절한가? CAP 정리까지 가능?

1. RDB (Relational Database): 정형화된 스키마 구조를 가짐 (테이블, 열, 타입 등 명확히 정의됨)
    - 데이터는 관계(Relation) 로 표현 (PK, FK 통한 관계설계)
    - SQL(Structured Query Language) 로 질의
    - ACID 트랜잭션 보장
    - RDBMS 대표 예시: MySQL, PostgreSQL, Oracle, SQL Server

2. NoSQL (Not only SQL): 비정형/반정형 데이터를 유연하게 저장 (스키마 덜 엄격하거나 없음)

- 다양한 형태 존재:
    - Key-Value: Redis, DynamoDB
    - Document: MongoDB, Couchbase
    - Wide Column: Cassandra, HBase
    - Graph: Neo4j, JanusGraph

- 일반적으로 수평 확장(Scale-out) 에 유리
- BASE 모델을 따름 (Eventually consistent 등)

3. RDB vs NoSQL: 언제 어떤 걸 쓰는 게 적절한가?

- 데이터 구조가 명확하고 관계성이 복잡한 경우: RDB 적합, No SQL 은 복잡한 Join 어렵거나 불가
- 트랜잭션이 중요한 금융/ERP/정산 시스템: RDB 강력한 ACID 보장, No SQL은 Eventually consistent
- 성능보다 데이터 정합성 우선: RDB 적합, NoSQL 별로
- 대규모 트래픽 처리 (SNS, IoT 등): RDB는 단일 노드 병목 발생, No SQL은 수평 확장 최적화됨.
- 빠른 쓰기 + 단순한 조회: No SQL, 예: Redis 캐시
- 유연한 스키마 + 빠른 개발: RDB는 매번 테이블 수정, No SQL은 Document 기반 구조 자유로움

4. CAP 이론과 NoSQL 이해

- 분산 시스템에서 세 가지 속성 중 두 가지만 만족할 수 있음
    - C (Consistency): 모든 노드에 동일한 데이터 보장
    - A (Availability): 클라이언트의 요청에 항상 응답
    - P (Partition Tolerance): 네트워크 분할 상황에서도 시스템이 계속 동작

- NoSQL은 보통 AP or CP 조합을 선택
    - MongoDB: CP => 네트워크 분할 시 일관성 우선, 일부 노드 잠시 중단 가능
    - Cassandra: AP => 가용성 우선, Consistency는 튜닝 가능
    - RDB (단일 노드): CA => 네트워크 분할 고려 X (CAP 논의 외 대상)


##### 1 - 2. - 정규화란? 왜 필요한가? 1NF, 2NF, 3NF 설명 가능? 비정규화는 언제 할까?

1. 정규화란? 왜 필요한가?

- 정의: 정규화(Normalization)는 중복을 제거하고, 데이터의 무결성을 유지하며, 관계형 데이터베이스의 설계를 체계적으로 개선하는 과정

- 정규화의 목적
    - 데이터 중복 제거: 같은 데이터가 여러 테이블/행에 존재하지 않도록 함
    - 업데이트 이상 방지: 중복 때문에 일부만 수정되면 모순 발생 → 정규화로 방지
    - 삽입/삭제 이상 방지: 특정 정보가 없으면 insert/delete가 안 되는 문제 방지
    - 데이터 무결성 유지: 설계 단계에서 잘못된 상태가 생기지 않도록 보장

2. 1NF ~ 3NF까지 설명

2 - 1. 1NF (First Normal Form): 컬럼 값은 원자값(Atomic Value) 이어야 함
    - 위반 예시
        - 학번, 이름, 수강과목
        - 101 , 홍길동, DB, AI
        - 수강과목이 복수값 => 1NF 위반

- 정규화
    - 학번, 이름, 수강과목
    - 101, 홍길동, DB
    - 101, 홍길동, AI


2 - 2. 2NF (Second Normal Form): 1NF 만족 + 부분 함수 종속 제거 (기본키의 일부분에만 의존하는 컬럼이 없어야 함)

- 위반 예시
    - 학번, 과목코드, 교수명
    - 101, DB101, 김교수
    - (학번, 과목코드) 복합키인데 => 교수명은 과목코드에만 종속됨 → 2NF 위반

- 정규화
    - 수강 테이블: 학번 + 과목코드
    - 과목 테이블: 과목코드 + 교수명

2 - 3. 3NF (Third Normal Form): 2NF 만족 + 이행적 종속 제거 (기본키 → A → B → B는 기본키에 직접 종속돼야함.)

- 위반 예시
    - 학번, 학과코드, 학과명
    - 101, CS, 컴퓨터공학
    - 학번 → 학과코드 → 학과명 → 학과명은 학번에 이행적 종속 → 3NF 위반

- 정규화
    - 학생 테이블: 학번, 학과코드
    - 학과 테이블: 학과코드, 학과명

3. 비정규화는 언제 할까?

- 성능 향상 or 시스템 제약으로 인해 정규화를 일부 포기하는 경우

- 비정규화 적용 시점
    - JOIN이 너무 많아서 쿼리 성능 저하: 자주 쓰는 컬럼을 함께 묶어 테이블 재설계
    - 데이터 읽기 위주 시스템: 정합성보다 조회 속도 우선 (ex: 로그분석, 대시보드)
    - NoSQL 설계: 정규화보다 중복 허용 → read/write 패턴 중심 설계
    - CDN or Reporting Table 설계: 특정 조회 패턴 최적화용 테이블 별도 구성
    - 예: 사용자 이름 + 부서명 JOIN 자주 발생 → 별도 조회용 테이블 만들어 중복 저장


##### 1 - 3. - PK와 FK의 차이는? FK 제약 조건은 언제 유용하고, 성능에 미치는 영향은?

1. PK vs FK: 개념과 차이

- Primary Key (PK)
    - 정의: 테이블에서 각 레코드를 고유하게 식별하는 열(또는 열 집합)
    - 특징: 중복 X, NULL X, 자동 인덱스 생성됨
    - 역할: 고유 ID 역할
    - 예시: 학생 테이블의 학번

- Foreign Key (FK)
    - 정의: 다른 테이블의 PK를 참조하는 제약 조건
    - 특징: NULL 가능, 중복 가능, 참조 대상(PK)이 반드시 존재해야 함
    - 역할: 테이블 간 관계 표현
    - 예시: 수강 테이블의 학번 → 학생 테이블의 PK 참조

2. 예시

- 학생 테이블

```sql
CREATE TABLE student (
    student_id INT PRIMARY KEY,
    name VARCHAR(100)
);
```

- 수강 테이블

```sql
CREATE TABLE course_enrollment (
    student_id INT,
    course_id INT,
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);
```

- student_id는 학생 테이블에서는 PK

- course_enrollment에서는 FK (학생 테이블의 student_id 참조)


##### 1 - 4. 인덱스란? 왜 쓰나? B-Tree vs Hash Index, Composite Index 활용 전략은?

1. 인덱스(Index)란? 왜 쓰나?

- 인덱스 정의: 인덱스는 데이터베이스에서 특정 컬럼의 값을 빠르게 찾기 위해 사용하는 데이터 구조
    - 즉, 책의 목차나 색인과 같은 역할, 테이블 전체를 스캔하지 않고도 빠르게 원하는 행에 접근 가능.

- 인덱스의 장점
    - 조회 속도 향상: WHERE 조건, JOIN 키, ORDER BY 등에 큰 효과
    - 데이터 접근 최소화: 불필요한 row scan을 방지

- 인덱스의 단점
    - 쓰기 성능 저하: INSERT/UPDATE/DELETE 시 인덱스도 같이 갱신
    - 디스크 공간 사용: 인덱스도 별도 저장구조로 공간 차지
    - 과한 인덱스는 독: 너무 많으면 오히려 성능 역효과, 쿼리 플랜 꼬일 수도 있음


2. B-Tree vs Hash Index

- B-Tree Index
    - 기본 구조: 정렬된 균형 트리
    - 지원 연산: =, <, >, BETWEEN, LIKE 등 범위 조건 가능
    - 정렬된 결과: 자동 정렬 가능 (ORDER BY 효과 있음)
    - 대표 사용처: MySQL(InnoDB), PostgreSQL 기본
    - 활용도: 매우 높음
    - 대부분의 RDB는 기본 인덱스를 B-Tree 기반으로 생성함 => 범위 조회 + 정렬 최적화에 유리

- Hash Index
    - 기본 구조: 해시 테이블 (Key → Value 매핑)
    - 지원 연산: = (정확히 일치하는 값만)
    - 정렬된 결과: 정렬 불가
    - 대표 사용처: Redis 내부 등 일부 특화된 상황
    - 활용도: 제한적 (PostgreSQL에선 거의 사용 안 함)


3. Composite Index (복합 인덱스) 전략

- 정의: 여러 컬럼을 묶어서 하나의 인덱스로 만드는 것
    - 예: `CREATE INDEX idx ON orders(user_id, created_at);`

- 활용 전략
    - Left-most Prefix Rule: user_id 단독 검색은 인덱스 사용 가능, created_at 단독은 X
    - 선택도 높은 컬럼 먼저: WHERE user_id = ? AND created_at > ? → user_id부터 설정
    - 정렬 최적화: ORDER BY user_id, created_at 순서일 때 인덱스 자동 활용
    - 조건 순서 맞추기: 인덱스 순서와 WHERE 조건 컬럼 순서가 달라도, 내부적으로는 가능 (하지만 정렬은 안 됨)

- 팁 정리
    - 자주 조인되는 키: 복합 인덱스로 JOIN 성능 최적화 가능
    - 비정규화 테이블: 여러 검색 조건 대응 위해 다중 컬럼 인덱스 필수
    - 과도한 인덱스 등록: 쿼리 플래너가 인덱스 선택 헷갈릴 수 있음 → EXPLAIN 필수 확인



##### 1 - 5. 트랜잭션이란? ACID 설명 → Isolation Level이 왜 중요한가?


1. 트랙잭션과 ACID

- 트랜잭션(Transaction) 정의: 데이터베이스에서 하나의 작업 단위를 구성하는 일련의 연산 묶음
    - 전부 성공하거나, 전부 실패해야 함 (all-or-nothing)

- 대표 예

```text
A → B로 100원 송금:  
1. A 계좌 잔액 –100  
2. B 계좌 잔액 +100  
→ 둘 다 성공해야 트랜잭션 완료
```

- ACID
    - A (Atomicity): 원자성 => 전부 성공 or 전부 실패. 중간 실패 없음
    - C (Consistency): 일관성 => 트랜잭션 전후에 DB 상태가 규칙 위반되지 않음
    - I (Isolation): 격리성 => 동시에 수행되는 트랜잭션이 서로 간섭하지 않음
    - D (Durability): 지속성 => Commit된 데이터는 영구 반영됨 (장애 발생에도 유지)

- 대부분의 RDBMS는 ACID 보장을 핵심으로 설계됨, 특히 OLTP 시스템에서 매우 중요

2. Isolation Level이 왜 중요한가?

- Isolation은 동시성 제어의 핵심
    - 여러 트랜잭션이 동시에 접근해도, 논리적으로 순차 실행된 것처럼 보여야 함
    - 그렇지 않으면 "일관성 위반" + "이상현상(Anomaly)" 발생

- 격리 수준에 따른 이상 현상
    - Dirty Read: A 트랜잭션이 아직 Commit 안 한 값을 B가 읽어버림
    - Non-repeatable Read: 같은 조건으로 두 번 조회했는데, 값이 바뀜
    - Phantom Read: 범위 조건으로 두 번 조회했더니, 행이 늘어남

- ANSI SQL 정의: Isolation Level 4단계
    - READ UNCOMMITTED: 가장 낮은 수준, dirty read 허용, 속도 높음, 정합성 낮음
    - READ COMMITTED: commit된 데이터만 읽음 (dirty read 방지), 대부분의 RDB 기본 설정
    - REPEATABLE READ: 같은 Row는 반복 조회 시 동일, phantom read는 발생 가능
    - SERIALIZABLE: 가장 강한 격리, 모든 트랜잭션을 순차적으로 실행한 것처럼 보이게 함, 정합성 높음, 성능 낮음

- PostgreSQL의 REPEATABLE READ는 사실상 SERIALIZABLE에 가깝게 작동함.
    - MVCC 기반으로 snapshot isolation 제공함.

- 상황별 고려사항
    - 성능 우선, dirty read 허용 가능 => READ COMMITTED
    - 분석 시스템에서 안정적 결과가 필요 => REPEATABLE READ or SERIALIZABLE
    - IoT, 로그 수집 등 대량 입력 중심 => 낮은 격리 수준, 병렬성 우선 고려
    - 정합성 가장 중요 (ex. 금융, 주문) => SERIALIZABLE 설정 + 로직상 보정도 필요


3. MVCC란?

- 정의: 동시성(Concurrency)을 안전하게 처리하기 위한 방법 중 하나로, '잠그지 않고, 과거 버전을 읽는' 방식의 트랜잭션 처리 기법입니다.
    - '잠금 없이 읽을 수 있다' = 조회 성능도 좋고, 충돌도 적다는 장점.

- MVCC 필요한 이유
    - 문제 상황: 트랜잭션 충돌 => 여러 트랜잭션이 동시에 데이터를 읽고/수정하려 할 때

```text
T1: UPDATE users SET name='헌성2' WHERE id=1;
T2: SELECT name FROM users WHERE id=1;
```

- 위 두 쿼리가 동시에 실행된다면
    - 잠금(Lock) 을 걸면 → T2가 기다려야 함 → 성능 저하, 병목 발생
    - Lock 안 걸면 → Dirty Read, Non-repeatable Read 발생 가능
    - 그래서 등장한 해결책: MVCC

- MVCC의 핵심 아이디어
    - 모든 데이터에 "버전(version)"을 붙여서 관리하고, 트랜잭션은 자신의 시점(snapshot)에 맞는 버전을 읽기만 한다.
    - 누군가가 데이터를 바꾸고 있어도 => 나는 내가 처음 봤던 시점의 데이터만 계속 읽는다 => 즉, '과거 버전 보기' 전략

- MVCC 내부 구조
    - 각 Row에 포함되는 정보
        - xmin: 이 Row를 생성한 트랜잭션 ID
        - xmax: 이 Row를 삭제한 트랜잭션 ID (또는 NULL = 아직 유효함)
        - PostgreSQL, MySQL(InnoDB), Oracle 등 대부분의 RDB가 유사한 구조

- MVCC 기반 SELECT 흐름
    - 트랜잭션 T100에서 `SELECT * FROM users WHERE id=1` 실행 시
    - Row의 xmin ≤ 100 (내 시점보다 먼저 만들어진 데이터)
    - xmax는 없거나, xmax > 100 (내 시점보다 나중에 삭제된 것)
    - 이 조건을 만족하는 유효한 버전만 읽는다

- UPDATE 흐름 
    - 직접 수정 안 함 => 기존 Row는 삭제 표시(xmax 설정) => 새로운 Row를 복사해서 새로운 버전으로 만듦

```sql
UPDATE users SET name='헌성2' WHERE id=1;

/* Row 1: name='헌성', xmin=10, xmax=100 (삭제됨)
/* Row 2: name='헌성2', xmin=100, xmax=NULL (새로운 값) 
```

- MVCC가 보장하는 격리 수준
    - Read Committed: 매 쿼리마다 최신 커밋된 값만 봄
    - Repeatable Read: 트랜잭션 전체 동안, 처음 본 시점의 Snapshot 유지
    - Serializable: 트랜잭션 간 완전 독립 보장 (실제로는 Snapshot + Validation 활용)
    - 이 모든 걸 Lock 없이 처리 → 병렬 처리 성능 굿!

- MVCC의 단점
    - 불필요한 Row 버전 증가: 매번 복사 → 공간 차지
    - 삭제된 Row도 남아있음: GC 필요함 (ex: PostgreSQL의 VACUUM)
    - 버전 충돌 가능성: 같은 Row에 대해 여러 버전이 생기면, 충돌 판단 필요 (could not serialize access 오류 등)

- 예시: PostgreSQL MVCC 흐름 요약
    - SELECT: 현재 트랜잭션 ID 기준으로 xmin/xmax 체크
    - INSERT: 새로운 xmin 부여
    - DELETE: xmax 값 부여 (물리적 삭제는 아님)
    - UPDATE: delete + insert (새 버전 생성)
    - VACUUM: 더 이상 참조되지 않는 old row를 실제로 삭제








### 2. SQL 활용 능력

##### 2 - 1. GROUP BY - WHERE 와 HAVING의 차이? Aggregate 함수 쿼리 최적화 포인트는?

1. WHERE, GROUP BY vs HAVING 차이점

- GROUP BY
    - 위치: SELECT 다음에 나옴
    - 용도: 데이터를 집계 기준으로 묶을 때 사용
    - 실행 시기: 집계 전에 실행
    - WHERE 절: WHERE는 집계 이전에 필터링

- HAVING
    - 위치: GROUP BY 다음에 나옴
    - 용도: 집계된 결과를 필터링할 때 사용
    - 실행 시기: 집계 후에 실행됨
    - WHERE와 차이: HAVING은 집계 이후에 필터링

- 예제

```sql
-- 직원 테이블에서 부서별 평균 연봉이 5000 이상인 부서만 보기

SELECT department, AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) >= 5000;
```

- GROUP BY → 부서별로 묶기
- AVG(salary) → 부서별 평균 계산
- HAVING → 집계 후, 조건에 맞는 부서만 출력
- 이때 WHERE AVG(salary) >= 5000 은 에러임. (집계 전이니까 AVG() 못 씀)

2. Aggregate 함수 쿼리 최적화 포인트

- 기본 개념: Aggregate 함수 = 집계 함수
    - COUNT(), SUM(), AVG(), MIN(), MAX() 자주 사용됨
    - GROUP BY와 함께 자주 쓰이며, 쿼리 성능에 직접 영향

- 최적화 전략 5가지
    - WHERE로 먼저 필터링: 집계 전에 줄일 수 있는 Row는 최대한 줄이기
    - 필요한 컬럼만 SELECT: SELECT * 하지 않기. 필요한 컬럼만
    - 인덱스 활용: GROUP BY 대상 컬럼에 인덱스 있을 경우 정렬 부담 감소
    - HAVING 대신 WHERE 사용 가능하면 WHERE 사용: HAVING은 집계 후 처리 → 비용 높음.
    - ROLLUP/CUBE도 과도하게 쓰면 성능 저하: OLAP계열 쿼리에서 주의 필요

- 예시

```sql
-- 성능 느린 쿼리
SELECT department, AVG(salary)
FROM employees
HAVING AVG(salary) > 5000;

-- 성능 개선된 쿼리
SELECT department, AVG(salary)
FROM employees
WHERE salary > 3000      -- 먼저 줄이기!
GROUP BY department
HAVING AVG(salary) > 5000;
```

- SQL의 내부 실행 순서 기준으로 보는 차이
    - FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
    - WHERE은 집계 전에
    - HAVING은 집계 후에



##### 2 - 2. 서브쿼리 vs JOIN? 서브쿼리로 느린 쿼리, JOIN으로 바꿔본 경험 있는가?

1. 서브쿼리 vs JOIN: 개념 차이

- 서브쿼리(Subquery)
    - 정의: SELECT 안에 포함된 또 다른 SELECT
    - 실행 순서: 내부 쿼리 먼저 실행 → 외부에서 사용
    - 성능: 느려질 수 있음 (특히 상관 서브쿼리)
    - 가독성: 간단한 상황에서는 직관적


- JOIN
    - 테이블을 기준 조건으로 병합
    - 실행 순서: 논리적 조인을 기준으로 DB 엔진이 최적 실행 계획 생성
    - 성능: 대부분의 경우 더 빠르고 최적화 가능
    - 가독성: 복잡한 조건일 땐 더 유연하게 조작 가능



- 느릴 수 있는 서브쿼리 예시

```sql
SELECT name
FROM employees
WHERE department_id IN (
  SELECT id FROM departments WHERE location = 'Seoul'
);
```

- 더 빠른 JOIN 서브쿼리 예시

```sql
SELECT e.name
FROM employees e
JOIN departments d ON e.department_id = d.id
WHERE d.location = 'Seoul';
```

- JOIN 쿼리는 실행 계획에서 인덱스를 활용한 Hash Join / Merge Join 등으로 최적화 가능 => 반면 서브쿼리는 결과를 먼저 만들어놓고 필터 → 메모리/속도 손해 가능성 있음


2. 상관 서브쿼리(Correlated Subquery)의 문제점

- 상관 서브쿼리 = 서브쿼리 안에서 바깥 쿼리의 값을 참조하는 구조

```sql
SELECT name
FROM employees e
WHERE salary > (
  SELECT AVG(salary) FROM employees WHERE department_id = e.department_id
);
```

- 이 쿼리는 employees의 각 Row마다 서브쿼리를 매번 실행함 → N개의 Row면 N번의 쿼리 실행 = 심각한 성능 저하

- JOIN + GROUP BY로 바꾸면?
    - 한 번만 집계하고 JOIN가능, 훨씬 빠르고 확장성도 높음

```sql
WITH avg_salary AS (
  SELECT department_id, AVG(salary) AS dept_avg
  FROM employees
  GROUP BY department_id
)

SELECT e.name
FROM employees e
JOIN avg_salary a ON e.department_id = a.department_id
WHERE e.salary > a.dept_avg;
```

- JOIN으로 바꿔본 경험, 이런 식으로 말하면 좋아요

```
이전 프로젝트에서 상관 서브쿼리를 사용한 성능 저하가 있어서,
CTE(Common Table Expression) + JOIN 방식으로 리팩토링했습니다.
불필요한 반복 실행을 피하면서 실행 계획도 Hash Join으로 잡혀 성능이 5배 이상 개선됐습니다.
```

- 언제 서브쿼리가 더 나을 수 있나?
    - 단순 존재 여부 확인 (EXISTS): 불필요한 JOIN 방지, 빠름
    - 중첩된 집계 필터링: JOIN보다 간결하게 표현 가능
    - CTE로 반복 활용 어려운 구조: 쿼리 복잡도 낮추기 위해 일시적으로 유용
    - 서브쿼리가 '느려서 안 쓰는 게 아니라, 잘 쓰면 유용하고, 잘못 쓰면 치명적'인 구조라는 걸 이해하는 게 핵심



##### 2 - 3. EXISTS vs IN 차이점은? Anti Join 구조로 최적화하는 사례 설명 가능?

1. EXISTS vs IN의 기본 차이

- IN
    - 개념: 서브쿼리 결과 안에 값이 있는지 확인
    - 실행 방식: 서브쿼리 결과를 전부 계산한 후, 메인 쿼리 비교
    - 성능: 서브쿼리 결과가 작을 땐 효율적
    - NULL 처리: NULL이 섞여 있으면 예측 못함 (주의)

- EXISTS
    - 개념: 서브쿼리에 결과가 존재하는지 확인
    - 실행 방식: 조건 만족하는 Row를 발견하면 즉시 TRUE 리턴
    - 성능: 서브쿼리 결과가 클수록 EXISTS가 유리
    - NULL 처리: EXISTS는 NULL 무관


2. 예시 비교

- IN 예시 => departments의 id 리스트를 먼저 구함 → 전체 IN (...) 비교

```sql
SELECT name
FROM employees
WHERE department_id IN (
    SELECT id FROM departments WHERE location = 'Seoul'
);
```


- EXISTS 예시 => departments에 조건을 만족하는 Row가 있으면 즉시 TRUE 리턴 → 빠르게 단락 가능

```sql
SELECT e.name
FROM employees e
WHERE EXISTS (
    SELECT 1 FROM departments d
    WHERE d.location = 'Seoul'
      AND d.id = e.department_id
);
```

3. 차이 포인트 정리
    - 서브쿼리 결과가 작을 때: IN이 빠름 (명확한 리스트 비교)
    - 서브쿼리 결과가 크고, 조인 조건이 있을 때: EXISTS가 훨씬 빠름
    - NULL 주의: IN (...) 안에 NULL 있으면 예외 가능성 높음.
    - 상관 서브쿼리: EXISTS가 더 자연스럽고 빠름


4. Anti Join 구조

- 정의: 특정 조건을 만족하지 않는 레코드를 찾는 쿼리 구조
    - 예: '서울이 아닌 부서에 소속된 직원만 조회'


- 가장 단순한 형태 (서브쿼리)

```sql
SELECT *
FROM employees
WHERE department_id NOT IN (
    SELECT id FROM departments WHERE location = 'Seoul'
);
```

- 문제점
    - NOT IN은 NULL 포함되면 전부 FALSE 처리
    - 실행 계획 상, 서브쿼리 전체 평가가 필요 → 성능 저하

- 개선된 형태: Anti Join (LEFT JOIN + NULL FILTER)
    - 서울 부서에 해당하지 않는 직원만 남김
    - LEFT JOIN 후 매칭 안 되는 데이터 필터 → Anti Join
    - 인덱스 활용 가능 → 대규모 데이터에서도 빠름

```sql
SELECT e.*
FROM employees e
LEFT JOIN departments d
  ON e.department_id = d.id AND d.location = 'Seoul'
WHERE d.id IS NULL;
```




##### 2 - 4. DDL, DML, DCL의 차이? GRANT/REVOKE 쓰는 상황은 언제 있나?

1. DDL (Data Definition Language): 데이터 구조(스키마)를 정의하고 변경하는 명령어

- 대표 예시
    - CREATE: 테이블, 인덱스, 뷰, DB 등 생성
    - ALTER: 테이블 구조 변경 (컬럼 추가, 타입 변경 등)
    - DROP: 테이블/DB/인덱스 삭제
    - TRUNCATE: 전체 데이터 삭제 (로그 기록 거의 없음, 빠름)

- 특징
    - 자동 커밋 발생 (ROLLBACK 안 됨)
    - 트랜잭션과 별개로 즉시 적용


2. DML (Data Manipulation Language): 실제 데이터를 조작하는 명령어

- 대표 명령어
    - SELECT: 데이터 조회
    - INSERT: 데이터 삽입
    - UPDATE: 데이터 수정
    - DELETE: 데이터 삭제

- 특징
    - 트랜잭션 관리 대상 (COMMIT, ROLLBACK 가능)
    - 데이터 값의 읽기/쓰기/수정/삭제와 관련됨


3. DCL (Data Control Language): 사용자 권한 및 접근 제어를 다루는 명령어

- 대표 명령어
    - GRANT: 특정 사용자에게 권한 부여
    - REVOKE: 특정 사용자로부터 권한 회수

- 특징
    - 시스템 보안, 운영, DB 접근 권한과 직결
    - DDL/DML을 누구에게 허용할지를 설정


4. GRANT / REVOKE 실제 사용 상황
    - 개발자에게 SELECT 권한만 부여: `GRANT SELECT ON employees TO dev_user;`
    - ETL 계정에게 특정 테이블에 INSERT/UPDATE만 허용: `GRANT INSERT, UPDATE ON sales TO etl_user;`
    - 실수로 부여한 권한 회수: `REVOKE DELETE ON sales FROM intern_user;`
    - 뷰(View)를 접근용으로 만들고, 원본 테이블은 막기: `원본에 REVOKE, 뷰에만 GRANT`

- PostgreSQL/MySQL에서도 비슷하게 동작: AWS RDS, Cloud SQL에서는 IAM 연동 or 접속 계정별 권한 설정과 연결됨

- DB 권한 설계 팁
    - 최소 권한 부여 원칙: 개발자/운영자 등 역할에 맞게 권한 제한
    - 업무 단위로 사용자 그룹화: 역할(Role) 기반 권한 부여 추천 (GRANT SELECT ON ... TO analyst_role)
    - 감사(Audit)와 보안 고려: 삭제 권한은 매우 제한적으로 부여해야 함



##### 2 - 5. 윈도우 함수 써봤나요? RANK(), LAG(), SUM OVER() 등 활용 예시?


1. 윈도우 함수란?

- 전체 결과 집합에서 특정 행을 기준으로 "창(window)"을 만들어, 그 범위 내에서 집계 또는 계산을 수행하는 함수

- 일반적인 GROUP BY와 다르게 집계 후에도 Row를 유지하기 때문에 원본 + 계산 결과를 함께 출력 가능


2. 대표 윈도우 함수 예시 + 활용

- RANK() / DENSE_RANK() / ROW_NUMBER()
    - RANK(): 같은 값은 같은 순위, 다음 순위는 건너뜀 (1, 1, 3, 4...)
    - DENSE_RANK(): 같은 값은 같은 순위, 번호 건너뛰지 않음 (1, 1, 2, 3...)
    - ROW_NUMBER(): 단순히 행 번호 매김 (중복 없음)

- 예시: 부서 내 급여 순위 => 부서별로 급여가 높은 순서대로 순위 부여

```sql
SELECT employee_id, department_id, salary,
       RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dept_rank
FROM employees;
```


- LAG() / LEAD(): 이전/다음 행과 비교할 때 사용
    - LAG(col, n): 이전 n번째 행의 값
    - LEAD(col, n): 다음 n번째 행의 값

- 예시: 일별 매출 증가율 계산 => 전일 대비 증감량 계산

```sql
SELECT sales_date, amount,
       LAG(amount, 1) OVER (ORDER BY sales_date) AS prev_amount,
       (amount - LAG(amount, 1) OVER (ORDER BY sales_date)) AS diff
FROM daily_sales;
```

- SUM() OVER() / AVG() OVER()
    - 누적합, 이동평균 등 다양한 Running Total 계산 가능

- 예시: 월별 누적 매출

```sql
SELECT sales_date, amount,
       SUM(amount) OVER (ORDER BY sales_date) AS running_total
FROM daily_sales;
```

- 활용 예시
    - 실시간 랭킹: RANK() + PARTITION BY
    - 전날 대비 변화량: LAG()
    - 다음 상태 예측: LEAD()
    - 누적 가입자 수: SUM() OVER()
    - 분기별 매출 증감: AVG() + PARTITION BY quarter


3. GROUP BY vs 윈도우 함수

- GROUP BY
    - Row 유지: 안됨. 집계 결과만 남김
    - 동시 사용: 불가능
    - 가독성/표현력: 제한적

- 윈도우 함수
    - Row 유지: 집계 + 원본 Row 모두 유지
    - 동시 사용: 같은 쿼리 안에서 복수 집계 가능
    - 가독성/표현력: 유연하고 강력함 (비교/누적/순위 등)








### 3. 성능/튜닝/운영 관점


##### 3 - 1. 인덱스가 왜 느려질 수 있나? Index Selectivity, Index-only scan 개념까지 가능?


1. 선택도(Selectivity)가 낮을 때

- 선택도 (Selectivity): 인덱스를 통해 전체 데이터 중 얼마나 적은 수의 row만 선택 가능한지를 나타내는 수치.

- 공식: 선택도 = (조회 결과 row 수) / (전체 row 수) => 값이 작을수록 인덱스 효율 높음

- 예시
    - 성별 = '남': 전체 인구의 50% 이상 → 선택도 낮음, 인덱스 비효율적
    - 주민등록번호 = '991212-1234567': 1명 → 선택도 높음, 인덱스 효과적


2. 인덱스만으로 결과를 반환할 수 없을 때 (Index-only Scan 불가)

- Index-only Scan: 인덱스에 필요한 컬럼이 모두 포함되어 있어서, 테이블까지 접근하지 않고도 쿼리 결과를 낼 수 있음

- 인덱스에 없는 컬럼까지 필요하다면 → 테이블 row 접근 필요 => 느려짐
    - 즉, 추가 I/O 비용 발생

- 예시
    - age 컬럼에 인덱스는 있다 가정
    - 근데 name은 인덱스에 없음 → 테이블 row 접근 필요 → Index-only Scan 불가

```sql
SELECT name FROM users WHERE age = 20;
```

3. 인덱스 단편화(Index Fragmentation)

- 잦은 INSERT / DELETE / UPDATE로 인해 인덱스 내부 구조가 비효율적으로 변형

- B-tree 구조가 비틀어지면 → 탐색 성능 저하

- 디스크 I/O 증가 → 느려짐


4. 인덱스가 너무 많을 때

- INSERT/UPDATE/DELETE 시마다 모든 관련 인덱스 갱신해야 해서 오히려 느려짐




##### 3 - 2. Explain Plan 볼 줄 아나요? PostgreSQL 기준 실제 읽는 순서 이해하고 있나?

1. Explain Plan 보는 법

- EXPLAIN (ANALYZE, BUFFERS) → 쿼리가 실제로 어떻게 실행되었는지 보여줌

- 단순 EXPLAIN은 예상 계획, ANALYZE 붙이면 실행 결과 기반

- 기본적인 실행 계획 구조

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT name FROM users WHERE age = 20;
```

- 예시 출력:

```sql
Seq Scan on users  (cost=0.00..35.50 rows=5 width=32)
  Filter: (age = 20)
  Rows Removed by Filter: 1000
  Buffers: shared hit=10
  Execution Time: 1.234 ms
```

- 주요 항목 해석
    - Node Type: 실행 방식 (Seq Scan, Index Scan, Nested Loop 등)
    - cost: (시작 비용..예상 총 비용)
    - rows: 예측되는 결과 row 수
    - width: row 평균 크기 (byte)
    - Filter: WHERE 조건
    - Buffers: 얼마나 많은 페이지를 읽었는지
    - Execution Time: 실제 소요 시간
    - Rows Removed by Filter: 필터링에서 제거된 row 수 (Seq Scan일 때 자주 나옴)

2. PostgreSQL에서 실제 읽는 순서

- 읽는 순서는 항상 아래에서 위로
    - 실행 계획은 트리 구조, 그리고 bottom-up 방식으로 읽어야 함

- 예시

```sql
SELECT u.name, o.amount
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.amount > 100;
```

- 실행 계획 예시

```java
Nested Loop  (cost=...)
  -> Seq Scan on orders o  (Filter: amount > 100)
  -> Index Scan on users u (Index Cond: u.id = o.user_id)
```

- 읽는 순서
    - orders 테이블에서 amount > 100 조건 만족하는 row 찾기 (Seq Scan)
    - 각 row마다 user_id를 기준으로 users 인덱스에서 사용자 정보 찾기 (Index Scan)
    - 최종적으로 Nested Loop로 조합하여 반환


3. 실행 계획 유형 예시
    - Seq Scan: 테이블 전체 탐색
    - Index Scan: 인덱스를 통해 특정 row 탐색 (→ 효율적)
    - Bitmap Index Scan: 여러 인덱스를 OR 조건 등으로 사용
    - Nested Loop: 작은 테이블 루프 돌며 큰 테이블에서 찾기 (보통 Index Scan과 같이)
    - Hash Join: 해시 테이블 만들어서 Join (메모리 사용)
    - Merge Join: 정렬된 두 테이블을 병합 (정렬 전제 조건)

4. 요약

- EXPLAIN (ANALYZE)는 실제 실행 계획 + 소요 시간을 보여줌

- 실행 계획은 트리 구조, 아래에서 위로 해석

- 주요 노드: Seq Scan, Index Scan, Nested Loop, Hash Join 등

- 조건이 필터인지 인덱스 조건인지 구분 (Filter vs Index Cond)






##### 3 - 3. 조인이 느릴 땐 어떤 전략? Hash Join / Merge Join / Nested Loop 차이 설명

- 조인이 느려질 때는 다음 네 가지 방향에서 원인 분석 & 전략을 세울 수 있음.


1. Join 방식 변경 (Join Algorithm 선택)

- PostgreSQL은 상황에 따라 Hash Join, Merge Join, Nested Loop 중 선택
- 직접 힌트를 줄 수는 없지만, 통계 정보와 인덱스 설계로 영향 줄 수 있음


2. 인덱스 확인 및 추가

- Join 조건의 컬럼에 인덱스가 없는 경우, Nested Loop의 성능이 치명적으로 떨어짐
- user_id, order_id처럼 Join Key에는 항상 인덱스를 고려하자

3. 필터 조건을 조인 전에 적용 (Filter Pushdown)

- 조인 전에 WHERE 필터를 최대한 적용해서 row 수를 줄이면 성능 대폭 향상
- 예: `WHERE amount > 100` => orders에서 먼저 필터링하고 조인

4. 통계 정보 갱신

- PostgreSQL은 통계 기반으로 Join 전략을 선택함
- 오래된 통계로 인해 잘못된 실행 계획이 나올 수 있음 → ANALYZE 명령으로 갱신

5. Join 방식 비교
    - Nested Loop
        - 아무 조건 없이 사용 가능
        - 한 row마다 다른 테이블 스캔
        - 한 쪽이 아주 작고, 다른 쪽에 인덱스 있을 때 빠름.
    - Hash Join
        - 등호 조건 필요 (=)
        - 작은 테이블로 해시 테이블 만들고, 큰 테이블에서 해시 조회
        - 한 쪽이 메모리에 들어갈 만큼 작고, 정렬 안 되어 있을 때 빠름.
    - Merge Join
        - 양쪽이 정렬되어 있어야 함
        - 정렬된 상태에서 병합
        - 두 테이블 모두 정렬되어 있거나 인덱스로 정렬 가능할 때 빠름


6. 예시로 join 방법 비교

```sql
SELECT * FROM users u
JOIN orders o ON u.id = o.user_id;
```

1. Nested Loop
    - users가 10 row, orders가 100,000 row일 때
    - orders.user_id에 인덱스 있다면 빠름
    - 없다면... 10 x 100,000 => 성능 폭망


2. Hash Join
    - orders가 크고 users가 작을 때
    - users를 메모리에 해시로 만들고, orders와 매칭
    - 인덱스 필요 없음, 하지만 메모리 사용량 주의

3. Merge Join
    - users.id와 orders.user_id가 정렬되어 있다면 최고 성능
    - 정렬하려면 추가 비용 들어감 → 인덱스 있으면 Good







##### 3 - 4. 파티셔닝이란? 수평/수직 파티셔닝, 테이블 샤딩 개념과 차이점은?

1. 파티셔닝이란?

- 큰 테이블을 쪼개서 성능과 관리 효율을 높이는 방법
- 쿼리 속도 개선
- 데이터 보관 및 삭제 용이
- 병렬 처리 가능

- 포인트: 파티셔닝은 "하나의 테이블을 논리적으로 나눈 것"이지만, 물리적으로는 다수의 파티션으로 구성돼 있음. → 사용자는 여전히 하나의 테이블처럼 접근 가능!
    - 즉, 개발자/사용자 입장에서 보면 여전히 그냥 하나의 테이블처럼 쿼리함
    - 그런데 내부적으로는 PostgreSQL이나 MySQL 등은 이 orders 테이블을 실제로는 이렇게 여러 개의 물리적 테이블로 나눠서 관리
        - 파일 시스템 기준으로 보면 얘네는 각각의 테이블(=파일)
        - DBMS가 알아서 조합해서 보여줄 뿐.

2. 수평 / 수직 파티셔닝

- 수평 파티셔닝 (Horizontal Partitioning): Row 단위로 나눔
    - 날짜 기준, 지역 기준, 고객 ID 기준 등

```txt
users_2023     ← 2023년 데이터
users_2024     ← 2024년 데이터
users_2025     ← 2025년 데이터
```

- 쿼리에서 WHERE year = 2024면 → 해당 파티션만 스캔

- 쿼리 성능에 가장 큰 영향을 줌


- 수직 파티셔닝 (Vertical Partitioning): Column 단위로 나눔
    - 자주 쓰는 컬럼과 안 쓰는 컬럼 분리

```plaintext
users_main (id, name, email)      ← 자주 쓰는 컬럼
users_info (id, address, birthday, hobbies)  ← 덜 쓰는 컬럼
```

- 캐시 효율 증가

- 전체 row 크기 줄어서 디스크 I/O 효율↑

- 단점: join 자주 발생하면 오히려 느려짐


3. 테이블 샤딩 (Sharding)

- 파티셔닝과 비슷해 보이지만, 완전히 다름!

- 샤딩: 물리적으로 다른 서버(노드)에 나눠서 저장

- 각각의 샤드를 독립된 DB 인스턴스로 운용


```plaintext
user_id 1 ~ 1,000,000  → DB1
user_id 1,000,001 ~ 2,000,000 → DB2
```

- 차이점 요약
    - 파티셔닝
        - 분할 기준: 논리적으로 같은 DB
        - 목적: 성능 최적화, 관리 효율
        - 접근: 단일 DB 인스턴스
        - 트랜잭션: 일반 트랜잭션 OK
    - 샤딩
        - 분할 기준: 다른 DB 서버 간 분산
        - 목적: 확장성 확보 (스케일 아웃)
        - 접근: 여러 DB 인스턴스
        - 트랜잭션: 분산 트랜잭션 처리 필요


- 파티셔닝은 한 테이블을 보기 좋게 쪼개는 거
- 샤딩은 트래픽/데이터 양 많아져서 DB를 아예 분산시키는 것

- 예시

```sql
CREATE TABLE orders (
  id SERIAL,
  user_id INT,
  order_date DATE,
  ...
) PARTITION BY RANGE (order_date);

-- 각 연도별로 파티션 만들기
CREATE TABLE orders_2023 PARTITION OF orders FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');
CREATE TABLE orders_2024 PARTITION OF orders FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```






##### 3 - 5. Query가 느리다, 어디서부터 볼 건가요? 테이블 스캔 여부, 인덱스 hit 여부, execution plan 해석 순서

- 1단계: Execution Plan (EXPLAIN (ANALYZE)) 부터 봐야 함
    - 이유: 느린 원인은 눈으로 보기 전까진 모름 → 예상이 아니라, 진짜로 어떤 순서로 실행됐는지 확인해야 함.

- 분석 순서 흐름: 3가지 핵심 포인트

1. Table Scan (Seq Scan) 나오는지 먼저 확인
    - Seq Scan은 전체 테이블을 읽는 것 → 매우 느릴 수 있음
    - 왜 발생했는지 이유를 파악해야 함
        - 조건의 선택도 낮음
        - 인덱스 없음
        - 통계가 부정확해서 인덱스를 안 쓰는 경우도 있음
    -  Seq Scan 발견 시 → “인덱스를 써야 하는 상황인데 왜 안 썼지?” 분석 시작

2. Index Scan / Index Only Scan 여부 확인
    - 쿼리에서 조건절 (WHERE, JOIN ON)이 인덱스를 잘 타고 있는지 확인
    - Index Scan: 인덱스 타고 테이블 접근
    - Index Only Scan: 인덱스만으로 결과 가능 → 더 빠름
    - Index Scan인데 느리다면? → "인덱스 선택도 낮은가?" 확인

3. Join 방식과 순서 확인
    - Nested Loop인지, Hash Join인지, Merge Join인지
    - 아래에서 위로 읽으며 어떤 테이블부터 읽고, Join을 어떤 방식으로 했는지 확인
    - 비효율적인 Nested Loop가 수십만 row 돌고 있는지 꼭 체크

- 순서 요약
    1. 전체 테이블 스캔 (Seq Scan) 있는지? => 테이블 크면 위험
    2. 인덱스 쓰고 있는지? => Index Scan/Only Scan 인지 확인
    3. Join 방식은 적절한가? => Nested Loop / Hash Join / Merge Join 적절한가
    4. 실제 행 수/예상 행 수 차이 큰가? => 통계가 잘못되어 planner가 삽질 중일 수 있음.
    5. Buffers 정보 / Execution Time => 실제 쿼리 시간이 어디서 오래 걸렸는지 확인

- 예시
    - 인덱스 없음 → 전체 테이블 스캔
    - age 선택도 낮음 → 인덱스 만들어도 효과 없음
    - 튜닝보다 쿼리 구조 개선 or 파티셔닝 고려

```sql
SELECT name FROM users WHERE age = 30;

EXPLAIN (ANALYZE)

SELECT name FROM users WHERE age = 30;
```

```sql
Seq Scan on users  (cost=0.00..35.50 rows=100 width=32)
  Filter: (age = 30)
  Rows Removed by Filter: 9900
  Execution Time: 20.000 ms
```


- 느릴 때 자주 쓰는 점검 리스트
    - WHERE 절에 인덱스 잘 잡힘?
    - LIMIT 없이 대량 row 처리하고 있는가?
    - GROUP BY / ORDER BY 정렬 비용 큰가?
    - JOIN 전에 불필요하게 큰 row set 있는가?
    - 함수 사용해서 인덱스 못 쓰는 조건이 있는가? (WHERE date(created_at) = '2024-01-01' 이런 거)









### 4. 데이터 엔지니어 관점의 DB 실무 질문

##### 4 - 1. CDC란? Debezium으로 Kafka 연계해본 적 있나요?

1. CDC 란?

- CDC (Change Data Capture)는 "DB의 데이터 변경 사항(Insert, Update, Delete)을 실시간으로 감지해서 다른 시스템으로 전달하는 기술"
    - OLTP DB에서 변경된 데이터를 ELT/Streaming 시스템으로 보낼 때 유용
    - 성능 저하 없이 실시간 데이터 파이프라인 구성 가능

- 예시 상황: 사용자 웹사이트 활동 → PostgreSQL DB 반영됨 → CDC로 Kafka에 전송 → Flink/Spark에서 실시간 처리 → BigQuery, Elasticsearch 등에 적재

- 대표적인 CDC 방식 3가지
    - Trigger 기반
        - DB에 트리거 걸어서 로그 테이블에 기록
        - 구현 단순
        - DB 부하 큼, 실시간성 떨어짐
    - Timestamp 기반
        - 변경 시각 기준으로 주기적 Polling
        - 구현 쉬움
        - 완전 실시간은 아님
    - Binlog 기반
        - DB의 Binary Log를 분석해서 변경 감지
        - 실시간 가능, 성능 우수
        - 로그 형식에 종속적, 세팅 복잡

- 보통 Binlog 기반 CDC + Debezium 조합을 많이 쓴다고 함 (지피티는 왜 실무를 해본적도 없는데 실무라는 표현을 좋아할까)

- Debezium이란?
    - Debezium은 Binlog 기반 CDC를 Kafka로 전달해주는 오픈소스 플랫폼이야.
    - Kafka Connect 기반으로 동작하고, MySQL, PostgreSQL, MongoDB 등 다양한 DB 지원함.

- Debezium 흐름도

```css
[PostgreSQL]  →  [Debezium (Kafka Connect)]  →  [Kafka Topic]  →  [Consumer (Flink, Spark, ELK 등)]
```

- 연동할 때 필요한 구성 요소
    - PostgreSQL: 변경 감지 대상 DB
    - Kafka: 이벤트를 전달할 스트리밍 플랫폼
    - Zookeeper: Kafka coordination용
    - Kafka Connect: Debezium이 붙는 플랫폼
    - Debezium Connector: PostgreSQL용 connector 설정 필요

- Debezium PostgreSQL 연동할 때 중요한 설정들

- PostgreSQL 설정

```conf
wal_level = logical
max_replication_slots = 4
max_wal_senders = 4
```

- Kafka Connect + Debezium 설정

```json
{
  "name": "pg-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "dbz",
    "database.dbname": "mydb",
    "database.server.name": "pgserver1",
    "plugin.name": "pgoutput",
    // ...
  }
}
```

- Kafka Topic 구조
    - 테이블 단위로 Kafka Topic 생성됨
    - 예: pgserver1.public.users






##### 4 - 2. OLTP vs OLAP 차이? RDS와 DWH를 구분하고 있는가?


1. OLTP vs OLAP 차이

- OLTP (Online Transaction Processing)
    - 목적: 실시간 트랜잭션 처리 (읽기/쓰기)
    - 사용처: 웹서비스, 앱, 결제 시스템
    - 데이터 구조: 정규화 (Normalized) → 중복 최소화
    - 작업 예시: 회원가입, 주문, 로그인
    - 트랜잭션: 다수의 짧은 트랜잭션
    - 성능 포인트: 빠른 INSERT/UPDATE, 동시성 제어
    - 데이터 양: 비교적 적음 (핫 데이터)

- OLAP (Online Analytical Processing)
    - 목적: 데이터 분석 (읽기 중심)
    - 사용처: 데이터 웨어하우스, BI 대시보드
    - 데이터 구조: 비정규화 (Denormalized) → 조회 성능 ↑
    - 작업 예시: 매출 요약, 사용자 분석, 집계
    - 트랜잭션: 소수의 복잡한 쿼리
    - 성능 포인트: 빠른 SELECT, 대량 집계 최적화
    - 데이터 양: 수십수백 GBTB (히스토리 포함)

- 한줄 요약
    - OLTP는 앱/서비스용 "실시간 처리 DB"
    - OLAP은 분석/BI용 "읽기 위주 대용량 조회용 DB"


2. RDS vs DWH (Redshift, BigQuery 등)

- RDS (Relational Database Service)
    - OLTP용 데이터베이스 — 애플리케이션 백엔드에서 사용
    - 예시: MySQL, PostgreSQL, Aurora 등
    - 특징
        - 실시간 트랜잭션 처리
        - INSERT/UPDATE/Delete 위주
        - 정규화된 구조
        - 데이터 무결성과 동시성 제어 중시
        - 일반적으로 쿼리 응답이 빠르지만, 대량 집계에는 적합하지 않음

- DWH (Data Warehouse)
    - OLAP용 — 분석/집계/리포팅 전용 시스템
    - 예시: Amazon Redshift, Google BigQuery, Snowflake
    - 특징
        - 대량의 데이터를 읽기 중심으로 최적화
        - SELECT + GROUP BY, JOIN, 집계 연산 성능에 특화
        - 대용량 데이터를 병렬로 쪼개서 처리 (MPP 구조)
        - 비정규화 구조가 많음 (성능 위해 중복 허용)

- OLTP vs OLAP 예시
    - 고객이 주문을 생성한다 => OLTP (예: PostgreSQL in RDS)
    - 마케팅팀이 월별 상품별 매출 분석한다 => OLAP (예: BigQuery, Redshift)
    - 로그인 기록 저장 => OLTP
    - 사용자 클릭 로그 기반으로 행동 분석 => OLAP

- OLTP (RDS)
    - 사용 목적: 서비스 운영
    - 대표 제품: RDS, Aurora, MySQL, Postgres
    - 구조: 정규화
    - 주요 연산: INSERT, UPDATE
    - 트랜잭션: 짧고 많음
    - 스토리지: 비교적 작음
    - 병렬 처리: 보통 없음

- OLAP (DWH)
    - 사용 목적: 데이터 분석
    - 대표 제품: Redshift, BigQuery, Snowflake
    - 구조: 비정규화
    - 주요 연산: SELECT, GROUP BY
    - 트랜잭션: 길고 복잡
    - 스토리지: 대용량
    - 병렬 처리: MPP 구조 (대규모 병렬 처리)

- MPP = Massively Parallel Processing (대규모 병렬 처리) → 하나의 쿼리를 여러 노드(서버)가 나눠서 동시에 처리하는 구조
    - 일반적인 OLTP DB(RDS, MySQL 등)는 단일 노드에서 모든 쿼리를 처리
    - 반면에 MPP 구조를 사용하는 DWH (BigQuery, Redshift 등)는 → 쿼리를 쪼개서 여러 노드에 나눠 처리하고, → 마지막에 결과를 합쳐서 리턴

- MPP의 장점 vs 단점
    - 병렬 처리: 대용량 쿼리를 빠르게 수행 가능, 그러나 노드 간 네트워크 병목 가능
    - 확장성: 노드 수 늘리면 성능 스케일 아웃, 비용 상승
    - 성능: 데이터 집계, 분석에 특화, 작은 쿼리엔 오히려 느릴 수도




##### 4 - 3. PostgreSQL vs BigQuery 차이? Column-store vs Row-store의 구조적 차이?


1. PostgreSQL vs BigQuery 차이

- PostgreSQL
    - 목적: OLTP (서비스용)
    - 저장 방식: Row-oriented (Row-store)
    - 실행 구조: 단일 인스턴스, 트랜잭션 강함
    - 쿼리 처리: 빠른 단건 SELECT / INSERT
    - 스토리지: 일반 디스크 기반
    - 확장성: 수직 확장 (Vertical Scaling)
    - 비용: 인스턴스 기준 요금


- BigQuery
    - 목적: OLAP (분석용)
    - 저장 방식: Column-oriented (Column-store)
    - 실행 구조: MPP 기반, 분석에 최적화
    - 쿼리 처리: 느린 INSERT, 빠른 대용량 SELECT
    - 스토리지: GCP 내부 분산 저장 (Colossus)
    - 확장성: 수평 확장 (Horizontal / Serverless)
    - 비용: 쿼리/스토리지 기준 요금 (사용한 만큼)

- 요약
    - PostgreSQL은 실시간 서비스용 트랜잭션 처리에 특화된 Row-store OLTP DB
    - BigQuery는 대용량 분석용으로 특화된 Column-store OLAP DWH


2. Row-store vs Column-store 구조 차이

- Row-store (행 저장 구조) — PostgreSQL
    - 데이터를 한 행(row) 단위로 디스크에 연속 저장
    - 전체 행을 빨리 읽기 좋음 → INSERT/UPDATE 성능 좋음
        - SELECT *에 유리
    - 하지만 특정 컬럼만 수천만 건 읽을 땐 불리함 (불필요한 I/O)

```plaintext
[1, Alice, 25]
[2, Bob,   30]
[3, Carol, 22]
```



- Column-store (열 저장 구조) — BigQuery
    - 데이터를 컬럼별로 분리해서 저장
    - 특정 컬럼만 읽는 집계 쿼리에 매우 유리
        - SELECT AVG(age) → age 컬럼만 읽으면 됨
    - 압축 효율 높음, 병렬 처리에 유리
    - 하지만 단건 INSERT/UPDATE는 느림 (분산된 구조 재조합 필요)

```plaintext
IDs:     [1, 2, 3]
Names:   [Alice, Bob, Carol]
Ages:    [25, 30, 22]
```

- 예시 비교: 수천만 명 중 평균 나이 구하기
    - PostgreSQL (Row-store) → 전체 row I/O 발생 → 느림
    - BigQuery (Column-store) → age 컬럼만 읽음 → 빠름


- 판단 기준
    - 로그인/결제 등 실시간 처리: Row-store 적합
    - 하루 수천만건 데이터 분석: Columnar store 적합
    - 실시간 데이터 집계: Column store 적합
    - 대시보드 백엔드: Row store도 가능 (작은 규모), Column store가 추천됨 (대규모 기준)
    - 비용 고정: row store = 인스턴스 기준, column store = 사용량 기준 (예측 어려움)



##### 4 - 4. 테이블 스키마 변경 시 고려할 점은? 백필 작업, 마이그레이션 전략 (Zero-downtime 방식?)

- 테이블 스키마 변경 시 고려할 점
    - 예: 컬럼 추가/삭제, 타입 변경, 테이블 리네이밍 등
    - 바로 바꿨다가 장애 나는 일 진짜 많음
    - 서비스 무중단(zero-downtime) 유지하려면 아래 순서 꼭 챙겨야

- 주요 고려사항

1. 백필(Backfill) 문제: 새 컬럼을 추가했을 때 기존 데이터는 NULL 상태임
    - Default 값 넣거나 계산해서 채워야 함
    - 특히 UPDATE로 대량 row 수정 시 → I/O 폭탄, 서비스 지연 가능!

```sql
ALTER TABLE users ADD COLUMN age INT;
-- 기존 row는 NULL, 백필 필요!
```

2. 읽기/쓰기 영향: 컬럼 삭제/타입 변경은 기존 SELECT/INSERT 쿼리에 영향 줌
    - ORM, 백엔드 코드에서 그 컬럼을 참조하고 있으면 서비스 터짐

3. DB Lock 발생 가능성
    - 대용량 테이블에서 스키마 변경은 테이블 전체에 락 걸릴 수 있음
    - 서비스 쓰기/읽기 중단될 수도 있음


- 마이그레이션 전략: Zero-Downtime 방식 (점진적 적용)

- 단계별 예시 (컬럼 추가/변경 시)

1. 컬럼 추가 (Nullable)

```sql
ALTER TABLE users ADD COLUMN status TEXT; -- NULL 허용
```

2. 백엔드 코드 수정

- 새 컬럼을 읽거나 쓰도록 코드 수정 (기존 코드도 병행 운영)

3. 백필 작업 (배치 처리)

```sql
UPDATE users SET status = 'active' WHERE status IS NULL;
-- 쪼개서 처리 (LIMIT + OFFSET or WHERE 조건 등)
```

4. NOT NULL 제약 조건 추가

```sql
ALTER TABLE users ALTER COLUMN status SET NOT NULL;
```

5. 완전 이전 완료 후, 예전 로직 제거

- 나쁜 예시
    - 대량 데이터에서 전체 row update 발생
    - 쓰기 잠깐 중단될 수도 있음 → 이건 꼭 피하자!

```sql
ALTER TABLE users ADD COLUMN status TEXT NOT NULL DEFAULT 'active';
```

- 컬럼 삭제/타입 변경 시 전략

- 컬럼 삭제
    - 먼저 백엔드 코드에서 해당 컬럼 안 쓰도록 변경
    - 로그 확인하고 진짜 사용 안 되는지 검증
    - 마지막에 컬럼 DROP

- 타입 변경
    - 새 컬럼 생성 → 값 복사 (CAST)
    - 코드 교체 후, 기존 컬럼 DROP
    - Blue-Green 방식 처럼 두 버전 운영

- 자주 쓰는 표현
    - Backward compatible하게: 새 코드가 구버전 스키마에서도 잘 돌아가게
    - Online schema change 고려해야 함: 서비스 중단 없이 적용하는 마이그레이션








##### 4 - 5. DB 백업 전략 아는가? Full vs Incremental, PITR(Point-in-time recovery)?


1. DB 백업 전략

- DB 백업은 데이터 유실/장애 상황을 대비해서 복구 가능한 상태를 만드는 게 목적
    - 백업 전략은 복구 속도, 보존 기간, 용량 등을 균형 있게 설계야 함.

- 주요 백업 방식 두 가지
    1. Full Backup (전체 백업)
        - DB 전체 데이터를 통째로 백업
        - 장점: 복원 속도 빠름, 간단
        - 단점: 시간 오래 걸림, 용량 큼
        - 주기: 일반적으로 주 1회 등
        - 예시: `pg_dumpall > full_backup.sql`
    2. Incremental Backup (증분 백업)
        - 마지막 백업 이후 변경된 데이터만 백업
        - 장점: 빠르고 용량 작음
        - 단점: 복원 시 이전 백업과 순차 적용 필요
        - 주기: Full + Incremental 혼합 전략 사용 (예: 주 1회 Full + 매일 Incremental)


2. PITR (Point-in-time Recovery)

- 특정 시점으로 DB를 복구하는 기술

- 예를 들어, 오전 10시에 실수로 users 테이블을 지웠다면 → 오전 9시 59분 상태로 복구하는 게 PITR

- 동작 방식, PostgreSQL 기준:
    - Full Backup + WAL (Write-Ahead Logs) 보관
    - 복구 시 Full Backup을 복원하고,
    - WAL 로그를 적용해서 특정 시점까지 Replay
    - `[ FULL BACKUP ] + [ WAL Logs ]`  →  특정 시점 복구 가능 → 로그가 시간 순서로 기록돼 있어서 가능

- PostgreSQL에서 PITR 준비 예시

```bash
# PostgreSQL 설정
wal_level = replica
archive_mode = on
archive_command = 'cp %p /backup/%f'

# 복구 시
restore_command = 'cp /backup/%f %p'
recovery_target_time = '2025-03-31 09:59:00'
```

- 복구 시점(recovery_target_time)을 지정해서 복원함 → 마치 Git checkout처럼 시점 이동하는 느낌


- 백업 전략 예시
    - 장애 발생 시, 최대 24시간 + 몇 분 로그만 손실 가능성 있음.

```
매주 일요일 03:00 → Full Backup
매일 00:00 → Incremental Backup
WAL 로그는 실시간 보관 (PITR 지원)
보존 기간: 최근 30일
```


3. WAL (Write-Ahead-Log)

- WAL = Write-Ahead Logging → "먼저 로그에 쓰고 나중에 디스크에 반영한다"는 전략

- DB는 성능을 위해 메모리(RAM)에서 작업을 처리함. => 이러다 서버가 갑자기 장애 시 데이터 날아갈 수 있음.
    - 그래서 PostgreSQL은 데이터를 변경하기 전에, 반드시 로그(WAL)에 먼저 기록함.

```plaintext
1. 변경 내용 로그(WAL)에 기록
2. 로그 기록이 완료되면 → 실제 디스크 변경 (커밋)
```

- 이 순서가 바로 "Write Ahead Logging"

- WAL 파일이 저장하는 내용
    - 어떤 테이블의 어떤 row가 어떤 값으로 바뀌었는지
    - 어떤 INSERT, UPDATE, DELETE가 실행됐는지
    - 전체 redo 로그 (변경 이력) => 즉, DB의 모든 변경 이력

- WAL의 쓰임새 3가지

1. Crash Recovery
    - 서버가 갑자기 꺼졌을 때 → WAL 보고 다시 복원
    - 디스크에 반영 못 했던 작업을 WAL로 재현 가능!

2. PITR (Point-in-time Recovery)
    - 특정 시점까지 WAL만 replay 해서 복구 가능

3. Streaming Replication
    - Master DB가 WAL을 Slave에게 스트리밍 전송 → 거의 실시간 복제 가능

- 예시 흐름

```plaintext
1. 사용자 INSERT 요청
2. PostgreSQL → WAL 로그 먼저 작성
3. 그 다음 디스크에 실제 반영
4. 문제가 생겨도 WAL 보고 복구 가능
```













### 5. 비정형/NoSQL 연계 질문 (심화)

##### 5 - 1. NoSQL 중 써본 것? MongoDB, Redis, Cassandra 등 비교 가능?

1. NoSQL이란?

- RDBMS처럼 스키마 강제 없이, 유연한 구조 + 수평 확장에 강한 데이터베이스
    - 구조: Key-Value / Document / Column / Graph
    - 장점: 유연한 데이터 구조, 고속 처리, 분산 환경에 최적화
    - 단점: 복잡한 조인/트랜잭션은 어려움 (CAP trade-off)

- 대표 NoSQL 종류 비교
    - MongoDB
        - Document 형 DB
        - JSON-like 문서 저장, 쿼리 풍부함.
        - 유저 정보, 게시글, 로그 등 반정형 데이터에 적합
    - Redis
        - Key-Value (in-memory)
        - 초고속, 메모리 기반, TTL, pub/sub
        - 캐시, 세션 저장소, 실시간 순위 등에 적합
    - Cassandra
        - Wide-Column DB
        - 분산성 최고, 쓰기 중심, 무중단 확장
        - IoT, 로그 수집, 수평 확장이 필요한 대규모 쓰기 시스템
    - HBase
        - Wide-Column
        - Hadoop 기반, 실시간 읽기 가능
        - 정형+비정형 혼합 빅데이터
    - Neo4j
        - Graph DB
        - 노드-엣지 구조, 관계 질의 특화
        - 소셜 네트워크, 추천 시스템

2. No SQL DB 상세

- MongoDB
    - 문서(Document) 단위 저장 = JSON(BSON) 형태
    - 컬렉션 = 테이블, 문서 = row
    - 스키마 유연함 → 같은 컬렉션 안에서도 구조 다를 수 있음
    - 쿼리 풍부하고 Index도 잘 지원
    - 하지만 대규모 집계는 RDB보다 느릴 수 있음
    - 사용 예시: 사용자 정보, 게시글, 이벤트 로그 등 반정형 데이터

```json
{
  "name": "헌성",
  "tags": ["data", "cs"],
  "age": 27
}
```

- Redis
    - 인메모리 기반 Key-Value 저장소 (속도 최강)
    - TTL, pub/sub, sorted set 등 다양한 자료구조
    - 읽기/쓰기 밀리초 단위 → 캐시로 최고
    - 지속성 설정 (AOF, RDB)으로 데이터 보존 가능
    - 사용 예시: 로그인 세션, 캐시, 랭킹 시스템, 실시간 알림

- Cassandra
    - 대규모 분산 시스템에 특화
    - Column-family 구조 (RDB 테이블과 비슷해 보이지만 다름)
    - 데이터 복제, 자동 샤딩, 수평 확장에 아주 강함
    - 쓰기 성능 매우 뛰어남 (Append-only 구조)
    - 단점: 쿼리 제약 많음 (WHERE는 기본적으로 Partition Key 기반)
    - 사용 예시: IoT 센서 로그, 금융 거래 기록, 대규모 이벤트 로그 등

- 상황 예시
    - 유저 정보 저장 (구조 유연): MongoDB
    - 로그인 세션 + 캐시: Redis
    - 초당 수만 건 이벤트 수집: Cassandra
    - 대규모 소셜 그래프 탐색: Neo4j
    - 빅데이터 Hadoop 연동: HBase


- DB 별 핵심 키워드
    - MongoDB: 문서형, 유연한 구조
    - Redis: 메모리 기반, 실시간 캐시
    - Cassandra: 분산성 끝판왕, 쓰기 특화



##### 5 - 2. Redis는 언제 쓰는가? Cache vs Pub/Sub 구조 경험했는가?

- Redis는 언제 쓰는가?
    - Redis는 초고속 인메모리 데이터 저장소야.
    - 주로 아래 3가지 용도로 많이 씀

1. 캐시 (Cache)

- DB 조회 결과를 Redis에 저장 → 다음 요청부터 빠르게 응답

- TTL(Time-To-Live) 설정 가능 → 자동 만료

- 서비스 부하 감소 + 응답 속도 향상

```plaintext
1. 클라이언트가 요청
2. Redis 캐시에 key 존재? → 바로 응답 (HIT)
3. 없으면 → DB 조회 후 캐시에 저장 (MISS)
```

2. 세션 저장소

- 로그인한 사용자 세션 정보를 Redis에 저장

- Fast + TTL로 자동 만료 처리 가능


3. Pub/Sub (Publish/Subscribe)

- 실시간 메시지 브로커로 사용 가능

- 하나의 서비스가 메시지를 발행(Publish) 하면 => 다른 서비스들이 구독(Subscribe) 하여 실시간 반응
    - 예: 실시간 채팅, 알림 시스템, 게임 이벤트 브로드캐스트 등

- Cache vs Pub/Sub 차이와 구조
    - 목적: 빠른 데이터 응답, 부하 분산 / 실시간 메시지 전달
    - 구조: Key-Value / Channel 기반 메시징
    - 사용 예: 로그인 정보, 상품 정보 캐싱 / 채팅, 알림, 실시간 업데이트
    - TTL 가능: O / X
    - 지속성: 보통 휘발성 / 휘발성 (메시지는 소비되면 사라짐)

- Cache 예시 구조

```plaintext
[Client] → [Backend Server] → [Redis Cache] → [DB]
```

- Pub/Sub 예시 구조
    - Publisher가 chat:room1 채널에 메시지 발행
    - 구독 중인 모든 Subscriber가 동시에 받음
    - MQ (Kafka 등)처럼 메시지를 저장하거나 재전송하진 않음

```plaintext
[Publisher] → Redis Channel → [Subscriber 1] → [Subscriber 2]
```




##### 5 - 3. MongoDB에서 JOIN 안 되는데 어떻게 모델링? Embedded vs Reference 설계 원칙은?


- 전제: MongoDB는 RDB랑 다르게 JOIN이 기본적으로 불편함
    - `$lookup` 연산으로 JOIN 흉내는 가능하지만 성능도 별로고, 분산 시스템에선 쓰기 힘듦
    - 그래서 MongoDB는 JOIN 없이도 잘 굴러가도록 모델링을 해야 함.

- 해법 = Embedded vs Reference 설계
    - Embedded: 하나의 문서 안에 다른 데이터를 "중첩 저장" => 책 한 권에 부록까지 다 넣는 느낌
    - Reference: 관련 문서를 ObjectID 등으로 연결만 해두고, 나중에 따로 조회 => 링크만 붙여놓고, 필요한 순간에 찾아가는 방식

1. Embedded Document (내장 문서) 설계: 관계된 데이터를 하나의 문서로 묶어버리는 방식

```json
{
  "_id": "user123",
  "name": "헌성",
  "posts": [
    {"title": "첫 글", "date": "2024-01-01"},
    {"title": "두 번째 글", "date": "2024-01-02"}
  ]
}
```

- 사용하기 좋을 조건
    - 관계가 1:N이며, N이 적다 => 사용자 - 게시글 몇 개 정도
    - 자식 데이터가 자주 같이 조회된다 => 사용자 정보 보면서 게시글도 항상 같이 보여줘야 함
    - 자식 데이터가 거의 안 바뀜 => 수정/삭제가 드물다


2. Reference (참조) 설계

- 문서끼리 연결만 해두고, 실제 데이터는 따로 저장

```json
// users
{ "_id": "user123", "name": "헌성" }

// posts
{ "_id": "post456", "user_id": "user123", "title": "첫 글" }
```

- 실제 JOIN은 안 되니까 → 앱단에서 두 번 조회하거나, `$lookup` 연산을 써야 함 (하지만 대용량일수록 느림)

- 사용하기 좋을 조건
    - 관계가 N:M 또는 자식이 많음 => 하나의 유저가 수천 개의 게시글 작성
    - 자식 데이터가 자주 바뀜 => 댓글, 좋아요, 주문 상태 등
    - 자식 데이터를 독립적으로 조회할 일도 많음 => 댓글 목록, 주문 내역 등


- 설계 원칙 요약

- Embedded
    - 성능: 빠름 (한 번에 읽음)
    - 조회 시 편의성: 좋음 (바로 보여줌)
    - 데이터 중복: 가능성 있음
    - 자식 개수 많을 때: No (16MB 문서 크기 한계)
    - 독립성: 약함 (부모랑 같이 다녀야 함)


- Reference
    - 성능: 느릴 수 있음 (두 번 조회)
    - 조회 시 편의성: 따로 조회 필요
    - 데이터 중복: 최소화
    - 자식 개수 많을 때: Yes
    - 독립성: 강함 (각자 관리 가능)




##### 5 - 4. Cassandra의 데이터 모델링 방식은? Write-heavy 서비스에서의 denormalization 설계 이해

1. Cassandra의 데이터 모델링 방식
    - 핵심 개념: 쿼리를 기준으로 테이블을 설계한다
    - 정규화 X → 조인 X → ✅ denormalization 중심

2. Cassandra 모델링 철학
    - 조인 없음 (JOIN, Subquery 지원 거의 없음)
    - 동적 조건 필터링 없음 (WHERE 조건은 항상 파티션 키 기반)

- 쿼리 패턴에 맞춰 미리 정해진 조회를 위한 테이블을 만든다

- 데이터 중복을 허용 (정규화 X)

3. 예시: 일반적인 사용자 - 주문 관계

- RDB 모델
```sql
users (id, name)
orders (id, user_id, item, date)
```

- Cassandra에서는 이렇게 못 함 → 대신 조회 패턴을 기준으로 별도 테이블 설계
    - 이렇게 하면 WHERE user_id = ? 로 빠르게 조회 가능
    - user_id 기준으로 파티셔닝 되어 있음!

```plaintext
orders_by_user (
  user_id     TEXT,         ← Partition Key
  order_id    UUID,         ← Clustering Key
  item        TEXT,
  order_date  TIMESTAMP,
  PRIMARY KEY (user_id, order_id)
)
```



- 왜 denormalization이 중요한가?
    - Cassandra는 쓰기 비용이 매우 낮고 빠르기 때문에, 데이터를 중복 저장하더라도 읽기 성능을 위한 구조를 미리 만들어두는 게 원칙

4. Write-heavy 환경에서는?

- 예시 상황: 유저의 활동 로그 수집 시스템 (하루에 수백만 건씩 들어옴)

- 설계 전략
    - 쓰기 성능 우선: WAL 기반 append-only 구조 → 병렬 쓰기 성능 좋음
    - 읽기 효율도 고려해서 여러 뷰용 테이블을 미리 만들어놓음
    - 중복 저장 OK, 대신 쿼리가 항상 빠르게 터져야 함

- 예시 구조
    - 같은 로그 데이터를 두 테이블에 나눠서 저장함 (중복 OK)
    - 대신 어떤 쿼리에도 빠르게 대응 가능

```sql
-- 전체 로그를 시간순으로 조회
logs_by_day (
  log_date  DATE,
  log_time  TIMESTAMP,
  user_id   TEXT,
  action    TEXT,
  PRIMARY KEY ((log_date), log_time)
)

-- 유저별 활동 로그
logs_by_user (
  user_id   TEXT,
  log_time  TIMESTAMP,
  action    TEXT,
  PRIMARY KEY ((user_id), log_time)
)
```



- 핵심 모델링 개념 정리
    - Partition Key: 데이터를 물리적으로 분산 저장하는 기준 필드
    - Clustering Key: Partition 내부에서 정렬 기준 필드
    - 데이터 중복 허용: JOIN 불가하므로, 필요한 만큼 뷰별 테이블 생성
    - 쿼리 패턴 기반 설계: 어떤 쿼리를 할 건지 → 그에 맞춰 테이블 생성

- 한 줄 요약
    - Cassandra는 '쓰기 빠르게 하고, 읽기는 미리 설계된 테이블에서 하자' 가 철학
    - 그래서 denormalization(비정규화) + 쿼리 중심 테이블 설계가 필수다!













