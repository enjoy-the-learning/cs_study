# Spark 면접 질문

### 1. Spark의 Lazy Execution과 DAG는 어떻게 연결되며, 어떤 이점이 있나요?

- Transformation은 Lazy하게 처리되어 DAG에 쌓인다.

- Action이 호출될 때 DAG가 실행되며, Catalyst Optimizer가 이를 최적화한다.

- 이 구조 덕분에 필요 없는 연산은 생략되고, stage merge 등이 가능하다.


### 2. Wide Transformation이 발생하는 시점은 언제이며, 이로 인한 성능 병목은 어떻게 해소할 수 있나요?

- groupByKey, join, distinct 등은 Wide Transformation을 유발한다.

- 이때 shuffle, sort, data serialization이 발생하여 디스크/네트워크 I/O 병목 발생

- 해결책: reduceByKey, map-side combine, salting, partition 조정, broadcast join 전략 등


### 3. Spark SQL의 Catalyst Optimizer는 어떤 방식으로 쿼리를 최적화하나요?

- Catalyst는 Logical Plan → Optimized Logical Plan → Physical Plan으로 최적화

- Rule-based + Cost-based 전략을 혼합

- 예: filter pushdown, constant folding, predicate simplification 등 적용됨


### 4. Shuffle Spill은 언제 발생하고, 이를 줄이기 위한 설정 또는 코딩 전략에는 어떤 것들이 있나요?

- Aggregation, Join, Sort 시 메모리가 부족하면 디스크로 spill 발생

- 해결: executor.memory, memoryOverhead 조정, Kryo Serializer, shuffle.compress, Task 수 조정 등

- 코드 차원에선 groupByKey → reduceByKey, salting 등 적용


### 5. Spark에서 Dynamic Resource Allocation이 성능을 저하시키는 시나리오는 어떤 것이 있을까요?

- Executor 재할당 지연 (특히 K8s에서 Pod 생성 지연)

- Shuffle-heavy 작업에서 Executor가 죽으면 Shuffle 파일 유실 → 네트워크 재전송 증가

- Streaming이나 Skew Task 처리 시 오히려 불안정
