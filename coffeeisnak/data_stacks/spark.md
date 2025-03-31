
# 스파크 스터디 목차 & 질문 리스트

### 0. 스파크란?

- 아파치 스파크는 빅데이터 분석 프레임웍으로, 하둡의 단점을 보완하기 위해서 탄생하였다.
- 하둡을 대체하기 보다는 하둡 생태계를 보완하는 기술로 보면 되는데 실제로 기동할때 하둡의 기능들을 사용하는 방식으로 기능한다. (그렇게 등장했다.)

- 하둡: 맵리듀스 방식으로 디스크(HDFS)에 저장된 파일 데이터를 기반으로 배치 분석을 진행 
- 스파크: 디스크나 기타 다른 저장소(데이터 베이스등)에 저장된 데이터를 메모리로 올려서 분석하는 방식으로 배치 분석 뿐만 아니라, 스트리밍 데이터 양쪽 분석을 모두 지원한다.
 
- 스파크 기본 동작 원리 및 아키텍쳐
    - 스파크 클러스터의 구조는 크게 물리적 Master node 와 worker 노드로 구성 / Driver, Executor라는 논리적 노드로 구성됨.
    - Master Node: 전체 클러스터를 관리하고 분석 프로그램을 수행하는 역할을 한다. (사용자가 만든 분석 프로그램을 Driver Program 이라고 한다.) => 이 분석 프로그램을 스파크 클러스터에 실행하게 되면 하나의 JOB이 생성된다.
    - Worker Node: 생성된 JOB이 외부 저장소 (HDFS와 같은 파일 시스템이나 외부 데이터 베이스)로 부터 데이터를 로딩하는 경우, 이 데이터는 스파크 클러스터 Worker node로 로딩이 되는데, 로딩된 데이터는 여러 서버의 메모리에 분산되어 로딩이 된다. 
    - 스파크 메모리에 저장된 데이터 객체를 RDD라고 한다. => 로딩된 데이터는 애플리케이션 로직에 의해서 처리되는데, 하나의 JOB이 여러 worker node에 분산된 데이터를 이용해서 분산되어 실행되기 때문에, 하나의 JOB은 여러개의 Task로 분리되어 실행이 된다. 이렇게 나눠진 Task를 실행하는 것을 Executor 라고 한다. 

- 클러스터 매니저(Cluster Manager)
    - 스파크는 데이터를 분산 처리하기 위해서 하나의 클러스터 내에 여러대의 머신, 즉 워커(Worker)들로 구성
    - 하나의 JOB이 여러대의 워커에 분산되서 처리되기 위해 하나의 JOB을 여러개의 TASK로 나눈 후에, 적절하게 이 TASK들을 여러 서버에 분산해서 배치
    - 클러스터내의 워크 들도 관리를 해줘야 하는데, 이렇게 클러스터내의 워커 리소스를 관리하고 TASK를 배치 하는 역할을 하는 것이 클러스터 매니저
    - 클러스터 매니저는 일종의 스파크 런타임으로 기능, Standalone , Yarn, SIMR 등의 타입이 있다. 
    - Standalone은 하나의 머신 내에서 스파크를 운영하는 방식, 로컬 개발 환경등에 적합 
    - 하둡 2.X의 리소스 매니저인 YARN을 사용하여, YARN으로 하여금 클러스터내에 TASK를 배치하도록 하는 방법
    - 하둡 1.X 이하를 사용할 경우 하둡의 맵리듀스안에 맵 작업으로 스파크 TASK를 맵핑하는 Spark In MR (SIMR)방식이 있다. 
    - 하둡 에코 시스템 외에도 다른 클러스터 매니저를 사용할 수 있는데, 대표적으로 Apache Mesos나, Kubernetes등을 클러스터 매니저로 사용이 가능하다. 

- 스토리지
    - 스파크는 메모리 베이스로 데이터를 처리하지만 외부 스토리지는 포함하고 있지 않기 때문에 별도의 외부 스토리지를 사용해야 함 
    - 가장 대표적으로 사용되는것이 하둡의 HDFS 분산 파일 시스템이고, 클라우드의 경우 AWS S3나 Google Cloud의 Google Cloud Storage(GCS)등을 사용할 수 있음. 
    - 데이터 베이스로는 분산 노드에서 데이터를 동시에 읽으므로, 분산 처리를 잘 지원할 수 있는 NoSQL인 HBase등이 널리 사용됨. 
    - 그외에도 목적에 따라서 Solr, Kudu 등의 데이터 스토어를 사용한다. 

- 파일 포맷
    - 스파크에서는 여러 파일 포맷으로 데이터의 입, 출력을 지원함.
    - CSV,JSON : 우리가 일반적으로 사용하는 TEXT기반의 파일 포맷으로, 사람이 읽을 수 는 있지만 압축이 되지 않았기 때문에 용량이 크고 비효율적.
    - Parquet (Columnar) : 스파크와 함께 가장 널리함께 사용되는 파일 포맷으로 바이너리 포맷을 사용, 특히 데이터 뿐만 아니라 컬럼명, 데이터 타입, 기본적인 통계 데이타등의 메터 데이터를 포함함. CSV, JSON과는 다르게 기본적인 압축 알고리즘을 사용하고 특히 snappy와 같은 압축 방식을 사용했을때, 원본 데이터 대비 최대 75% 까지 압축이 가능
    - Parquet 포맷의 특징은 WORM (Write Once Read Many)라는 특성을 가지고 있는데, 쓰는 속도는 느리지만, 읽는 속도가 빠르다는 장점이 있다. 그리고 컬럼 베이스의 스토리지로 컬럼 단위로 저장을 하기 때문에, 전체테이블에서 특정 컬럼 만 쿼리하는데 있어서 빠른 성능을 낼 수 있다.
    - Avro (Row) : Avro는 Paquet 과 더불어 스파크와 함께 널리 사용되는 바이너리 데이터 포맷으로 Parquet이 컬럼 베이스라면, Avro는 로우 베이스로 데이터를 저장함. 
    - Avro는 바이너리로 데이터를 저장하고 스키마는 JSON 파일에 별도로 저장한다. 그래서 사용자가 바이너리 파일을 이해할 필요 없이 JSON 만으로도 전체적인 데이터 포맷에 대한 이해가 가능함. 만약 ROW에서 전체 컬럼을 리턴해야 하는 시나리오의 경우에는 Avro가 parquet보다 성능적으로 더 유리함.


### 1. Apache Spark 기본 개념 및 아키텍처

##### 스파크와 MR의 차이

- Spark는 왜 MapReduce보다 빠른가? 어떤 구조적 차이가 있나?
    - Hadoop MapReduce
        - 디스크 기반(Disk IO 중심)
        - 단계별 Job → Map → Reduce (직렬 처리)
            - Map: Mapping 한다, 1:1 대응 변환 
                - 각 원소가 독립적이기 때문에, 분산 시스템에서 쉽게 나눠서 처리 가능 → Spark에서는 Task 단위로 쪼개서 Executor에 할당
                - 함수형 프로그래밍에서 Map(f, [x1, x2, x3, ...])는 [f(x1), f(x2), f(x3), ...]를 반환함.
            - Reduce: 여러 개의 값을 하나로 합치는 집계(Aggregation) 연산, 데이터 집합을 누적하면서 하나의 값으로 축소
                - 부분 결과를 병렬로 구할 수 있지만, 최종 결과를 합치는 과정이 반드시 필요
                - 자연스럽게 병렬 연산이 어렵고 성능 병목의 가능성이 높아짐.
                - Spark에서는 Shuffle + Aggregation 과정이 동반됨 (느려지는 원인 중 하나!)
                - Reduce(f, init, [x1, x2, x3]) → f(f(f(init, x1), x2), x3) 처럼 동작
        - 매 단계마다 HDFS에 기록 후 처리
        - 중간 데이터를 디스크에 저장해서 장애 복구
        - 고지연 (수 분 이상)
            - MapReduce의 고지연: 단계마다 디스크(HDFS)를 필수로 사용
            - Map 단계 → 디스크에 저장 → Shuffle 단계 → 디스크 → Reduce 단계 → 디스크 ...
            - 디스크 IO + 네트워크 IO가 반복 → 각 단계마다 중간 결과를 저장하고 읽는 시간이 발생
            - 기본적으로 Batch 기반 설계라서 모든 데이터를 다 처리한 뒤 결과를 반환 → 중간에 결과를 빨리 줄 수 없음
            - 보통 수 분에서 수십 분 단위 지연 발생 → 실시간 분석은 거의 불가능 (고지연)
        - 매 연산이 끝나면 디스크(HDFS)에 결과를 저장하고 다음 연산으로 넘어감. 디스크 IO가 병목, 단계별로 반복적이고 느림.
    - Apache Spark
        - 메모리 기반(In-Memory 중심)
        - 메모리에 유지 (필요할 때만 디스크에 스필)
        - RDD Lineage로 손실 시 재계산
            - RDD 리니지(Lineage)란?
                - RDD는 불변(Immutable) 객체, 연산(Transformation)을 할 때마다 새로운 RDD가 생기게 됨.
                - 그 과정(이력)을 연결한 게 Lineage임. → "이 데이터를 어떻게 만들었는지"를 기록
            - 리니지가 필요한 이유
                - Spark는 중간 데이터를 디스크에 저장하지 않음 (MapReduce와 차이!)
                - 대신에 리니지를 기억하고 있어서 → 만약 Partition이 날아가거나 Executor가 죽어도 → 그 Partition만 다시 계산할 수 있는 장애 복구 기능 제공
            - 리니지의 한계
                - 리니지가 너무 길어지면 재연산이 비효율적
                - 그래서 Checkpoint를 해서 특정 시점에서 RDD를 디스크에 저장해두기도 함 → 리니지를 끊고, 거기서부터 재시작 가능하도록
        - 저지연 (초~분 단위)
            - Spark의 저지연
                - 기본적으로 In-Memory 연산
                - 메모리에 데이터를 올려놓고, 그 상태에서 변환과 계산을 함 → 디스크 접근을 최소화 (필요할 때만 스필, 자세한 건 밑에서 설명!)
                - DAG를 통해 스테이지 병렬 실행 최적화
                - Lazy Execution 덕분에 실제 Action이 호출될 때까지 연산을 미루고, → 그때 최적화해서 빠르게 실행
                - 일반적으로 초 단위에서 수십 초 내 응답 가능 → 스트리밍 처리나 빠른 ETL에 적합 (저지연)
        - 메모리 기반으로 데이터를 처리하고, 중간 결과를 메모리에 유지. 반복 연산과 중간 연산이 빠르며, DAG 최적화를 통해 Job을 병렬로 나눠 실행.
    - 결론
        - 메모리 중심 설계 + DAG 최적화 및 병렬 실행 + 최소한의 디스크 접근 => Spark가 최대 100배 빠른 처리 속도를 제공할 수 있다고 말함.

- MR보다 100배 빠르다, 진실?
    - 출처
        - Spark가 처음 나왔을 때, Berkeley AMPLab에서 발표한 논문 기준
        - Hadoop MapReduce 대비 10배 ~ 100배 빠르다고 주장 → 특히 머신러닝 알고리즘(반복 연산)에서 월등히 빠름
    - 실제 성능이 100배 빠른 경우
        - In-Memory 반복 처리가 중요한 알고리즘에서 → 머신러닝, 그래프 처리, 반복적 계산 → Hadoop은 매번 디스크 접근 → Spark는 메모리 기반이라 차이가 큼
        - Disk IO 병목이 큰 환경에서 Spark는 극적인 개선이 가능함
        - Spark SQL + Catalyst 최적화 + Columnar 포맷 사용 시 → Hadoop 대비 10배~50배 성능 개선은 여전히 체감 가능할 것.
    - 그런데 무조건 100배는 과장일 수 있음
        - 실제 데이터/클러스터/파라미터/쿼리 최적화에 따라 다름 → 잘못 쓰면 Spark도 느림.
        - 메모리 부족하거나, Shuffle 최적화 안 하면 Spark도 병목 발생할 구간이 많음.
        - Hadoop은 대규모 배치 작업에 여전히 안정적 → Spark는 메모리 최적화와 튜닝을 반드시 고려해야 진짜 빠름.


##### 스파크의 데이터 구조

- RDD와 DataFrame, Dataset의 핵심 차이점은? 왜 Dataset을 쓰는 환경이 제한적일까?
    - RDD
        - 자료구조: 분산 리스트
        - 타입: 안정성	있음 (컴파일 시점)
        - API: 함수형 API (map, reduce 등)
        - 성능 최적화: 없음
        - 언어 지원: Java, Scala, Python
        - 주 사용처: 저수준 데이터 처리, 커스텀 연산
    - DataFrame
        - 자료구조: 테이블 형태(컬럼 기반)
        - 타입 안정성: 없음 (런타임 오류 가능)
        - API: SQL + DataFrame API
        - 성능 최적화: Catalyst + Tungsten 최적화
        - 언어 지원: Java, Scala, Python, R
        - 주 사용처: 일반 분석, SQL 쿼리, ETL 작업
    - Dataset
        - 자료구조: 테이블 형태 + 타입 안정성
        - 타입 안정성: 있음 (컴파일 시점)
        - API: DataFrame + 타입지정 가능
        - 성능 최적화: Catalyst + Tungsten 최적화
        - 언어 지원: Java, Scala (Python은 없음)
        - 주 사용처: 정적 타입 언어의 복잡한 ETL
    - Dataset을 쓰는 환경이 제한적인 이유
        - Scala/Java에서만 지원 => Python은 동적 타입 언어라 Dataset 불가.
        - 데이터 직렬화 비용과 JVM 의존성 이슈로 빅데이터 환경에서 복잡성 증가.
        - 실제 현업에서는 DataFrame 중심 + Spark SQL이 주로 사용됨. (이라는 피셜..) => 최적화가 잘 되어 있고, 런타임 유연성이 높음.



##### 스파크의 Driver, Exectutor

- Driver와 Executor의 역할은? Driver 장애 시 어떻게 복구하고, Executor 장애 시 Spark는 어떻게 대응하는가?
    - 스파크는 기본적으로 (소프트웨어 적으로), Cluster Manager 아래에 Driver와 Executor들이 뜨게 됨. 
    - Driver: 스파크 애플리케이션의 메인 프로세스임. DAG 생성, Stage 분할, Task 스케줄링, Executor 할당. 클러스터와 직접 통신
        - Driver 장애: 전체 스파크 애플리케이션 중단. Spark 자체 복구 기능 없음 → 외부에서 재시작 필요 (예: YARN/K8s 재시작)
    - Executor: 실질적인 데이터 연산 수행. Task 처리, 메모리 관리, 결과 반환 각각 JVM 프로세스로 격리됨
        - Executor 장애: Spark가 Task를 다른 Executor에 재할당. Driver가 지속적으로 헬스 체크 및 재시작 담당


- DAG(Directed Acyclic Graph)는 어떤 과정에서 생성되고, 어떻게 최적화되는가?
    - DAG 생성 과정
        - Transformation 연산 호출: (예: map(), filter(), join() 등) → Lazy 실행
        - Action 호출 시 트리거: (예: collect(), count(), save())
        - DAG 생성 및 최적화 수행
            - Stage 분할 (Narrow / Wide Transformation 기준)
            - Task 병렬화 및 Scheduling
    - DAG 최적화 기법
        - Catalyst Optimizer: 쿼리 최적화 엔진 (DataFrame, Dataset, SQL), Predicate Pushdown, Constant Folding
        - Tungsten 엔진: 물리계층 최적화 + 메모리 관리 개선, Whole-stage Code Generation으로 JVM 네이티브 코드 생성
        - Pipeline 병합: Stage 간 중간 데이터 최소화, Narrow Transformation은 가능한 한 병합 실행
    - 주요 DAG 사용처
        - DAG는 Spark UI → Stage/Task 분석에 필수.
        - Wide Transformation = Shuffle 발생 가능성 → 병목이 어디서 발생하는지 DAG 분석으로 확인 가능.

- Spark: 디스크에 스필(Spill to Disk) 한다는 의미
    - 기본 개념: Spark는 메모리 중심 프레임워크 → 근데, 메모리가 부족하다면 남은 데이터를 디스크로 임시 저장하는 게 Spill to Disk
    - 스필 사용할 때
        - Task 실행 중 데이터가 Executor 메모리를 초과할 때
        - Shuffle 단계에서 버퍼가 가득 찼을 때
        - 조인이나 집계가 커서 한 번에 메모리에 못 올릴 때
    - 스필의 문제점
        - 디스크 IO는 메모리 IO보다 훨씬 느림 (수백 배 차이)
        - Spark의 성능 저하 원인이 되고, GC까지 유발할 수 있음
        - 결국, 스필이 많을수록 Spark는 느려진다 → Spark 튜닝 포인트 중 하나임.
    - Spill 발생 방지 방법
        - Executor 메모리를 넉넉하게 설정
        - spark.shuffle.spill.compress 압축 설정 고려
        - Partition 개수 늘리기 (spark.sql.shuffle.partitions)
        - Joins에서 Broadcast Join 사용으로 Shuffle을 줄이기
        - 데이터 포맷 최적화 (예: Parquet + Column Pruning)

##### Spark에서 연산(Operation)

- Spark는 기본적으로 데이터를 분산 처리하기 위한 프레임워크고, 데이터를 가공하고 결과를 내는 과정이 연산(Operation)

- Spark의 연산은 크게 두 가지:
    - Transformation (변환 연산)
    - Action (실행 연산)

- Transformation: 데이터를 가공(변환)하는 연산. 하지만 바로 실행되지는 않음.
    - 결과로 새로운 RDD/DataFrame을 반환할 뿐, 아직 계산은 안 함.
    - Lazy 하다 → 실행이 "미뤄진다".
    - 데이터를 가공하는 설계도만 만드는 느낌, 쿼리 계획을 세움.
    - 원본 RDD/DataFrame은 변하지 않고, 새로운 객체를 반환
    - Transformation을 여러 번 이어 붙일 수 있음 => 이를 체이닝이라고 함.

-  주요 Transformation 종류
    - map(): 각 요소를 변환 (1:1 매핑), Narrow
    - filter(): 조건을 만족하는 요소만 필터링, Narrow
    - flatMap(): 요소를 0개 이상으로 변환 (리스트 펼치기), Narrow
    - groupByKey(): Key 별로 그룹화 (Shuffle 발생), Wide
    - reduceByKey(): Key 별 집계 (Local + Shuffle 최적화), Wide
    - join(): 두 RDD를 조인 (Shuffle 발생), Wide

- Action: 최종 결과를 트리거하는 실행 연산
    - Transformation으로 쌓아둔 모든 연산을 실제로 실행시키는 연산임.
    - Action을 호출해야만 Spark가 실제로 연산을 수행한다.
    - 이때 DAG를 완성하고, 최적화 후 Executor에서 Task 실행.
    - 결과를 Driver로 가져오거나, 외부 저장소에 저장함.

- 주요 Action 종류
    - collect(): 모든 데이터를 Driver로 가져옴
    - count(): 전체 데이터 개수를 반환
    - first(): 첫 번째 값을 반환
    - take(n): 앞 n개의 값을 반환
    - reduce(): 집계 연산 수행 (f(x, y))
    - saveAsTextFile(): 데이터를 파일로 저장
    - foreach(): 각 요소에 함수 실행 (저장, 외부 시스템 연결 등)

- Narrow Transformation: 각 부모(Parent) 파티션이 하나의 자식(Child) 파티션에만 데이터를 제공하는 연산
    - 즉, 데이터를 한 파티션 안에서만 처리하는 경우를 말함. => Shuffle이 발생하지 않는다
    - 데이터 이동(네트워크 IO)이 없고, 빠르고 안정적이다.
    - 데이터 이동 없음 (한 Executor 내에서 처리), Shuffle 발생 없음, 같은 Stage 안에서 처리됨. 빠름 (네트워크 비용 X, 디스크 I/O X)
    - 대표적인 Narrow 연산
        - map(): 각 요소를 개별적으로 변환
        - filter(): 각 요소를 조건으로 필터링
        - flatMap(): 각 요소를 펼쳐서 변환
        - union(): 두 RDD를 합침 (단, 파티션 수 같아야 Narrow)

- Wide Transformation: 하나의 자식(Child) 파티션이 여러 부모(Parent) 파티션으로부터 데이터를 받는 연산
    - 즉, 데이터가 재분배되어야 함. => Shuffle이 발생 => 네트워크 통신 필요 + 디스크에 임시 저장 가능성 (Spill)
    - 데이터 이동 있음 (네트워크로 다른 노드로 이동 가능), Shuffle 반드시 발생, 다른 Stage로 분할됨 (Shuffle 경계에서 나뉘는 기준), 성능 상대적으로 느림 (네트워크, 디스크 IO 부담)
    - 대표적인 Wide 연산
        - groupByKey(): Key 기준으로 그룹화 → 전파티션 데이터 섞임
        - reduceByKey(): Key 기준으로 값 집계 (Local Aggregation 후 Shuffle)
        - join(): 두 RDD를 Join → Key 기준으로 데이터 이동 필요
        - distinct(): 중복 제거 위해 데이터 이동 필요
        - repartition(): 파티션 재배분 → 전 데이터 Shuffle

- Narrow vs Wide 핵심 비교
    - Shuffle: 발생 안 함 / 반드시 발생
    - Stage 분할: 같은 Stage에서 실행 / 다른 Stage로 분할
    - 병목 원인: 거의 없음 / 네트워크 I/O, 디스크 Spill 가능
    - 성능: 빠름 / 상대적으로 느림
    - 예시: map(), filter() / groupByKey(), join()

- Narrow, Wide의 구분 이유
    - Spark Stage가 어디서 나뉘는지 알 수 있다. → Wide가 나오면 새로운 Stage 시작 = DAG 분석 가능
    - Shuffle 발생 시 성능 저하를 예방할 수 있다. → Wide Transformation을 쓸 때, 데이터 스큐(Data Skew)를 의심하고 대비해야 함.
    - 최적화 기준을 세울 수 있다. → Wide Transformation을 Narrow로 대체할 수 있는지 고민해야 함 (ex. groupByKey() 대신 reduceByKey())

- Shuffle 발생 과정과 비용
    - Shuffle: 데이터를 파티션 간에 재분배하는 과정 → 네트워크 전송 + 디스크에 임시 파일 저장(Spill) + 다시 읽기
    - 비용이 많이 드는 이유: 네트워크 I/O 발생 → Executor 간 데이터 전송 (수 GB~TB 데이터가 오갈 수 있음)
    - 디스크 쓰기/읽기 발생 (Spill) → 메모리 부족 시 디스크에 임시 저장 후 다시 읽어야 함
    - GC 부하 증가 → 객체가 많아지면 Garbage Collection이 빈번하게 발생 → Executor가 느려지고 Task가 지연됨

- Narrow Transformation이 선호됨.
    - 파티션 간 데이터 이동이 없어서 안정적
    - Executor 간 통신이 없어서 병목이 거의 없음

- Wide Transformation을 쓸 때 고려사항
    - Shuffle 병목 최소화 → reduceByKey()는 groupByKey()보다 Local Aggregation이 있어 성능이 좋음.
    - Broadcast Join 고려 → 한 쪽 데이터가 작으면 Broadcast 해서 Shuffle을 피할 수 있음.
    - 데이터 스큐(Data Skew) 처리 → 특정 Key에 데이터가 몰리면 병렬처리가 무너진다 → Salting 기법을 적용해서 Key 분산


##### Spark의 Lazy Execution

- Lazy Execution: 실제 실행을 Action까지 미룬다

- 개념: Spark는 Transformation을 호출해도 바로 실행하지 않음. => 어떤 연산을 할 지에 대한 DAG라는 실행 계획만 세워둠 => Action이 호출되는 순간까지 연산은 미뤄진다.

- 왜 Lazy Execution이 좋은가?
    - 최적화할 수 있다 → 여러 Transformation을 묶어서 실행할 수 있음 → Catalyst Optimizer가 불필요한 연산 제거, Predicate Pushdown, 필터 병합 등
    - 효율적인 스케줄링 가능 → DAG Scheduler가 Stage로 나눠서 병렬 처리 최적화
    - 불필요한 계산 방지 → Action이 없으면 실제 계산이 필요 없어서 리소스 낭비 없음.

- Spark 연산은 결국 DAG를 만든다.
    - DAG: Directed Acyclic Graph (유향 비순환 그래프) → Transformation을 쌓아둔 작업 흐름(Execution Plan)을 그래프로 표현한 것.
    - Narrow Transformation → 같은 Stage에 있음
    - Wide Transformation → 새로운 Stage 분리 + Shuffle 발생

- 실제 실행 과정
    - Transformation 호출 (map, filter 등)
    - Lazy Execution 상태로 DAG 생성
    - Action 호출 시 DAG 최적화
    - Stage 분할 및 Task 생성 → Executor 분배
    - 실제 데이터 처리 후 결과 반환

- Spark에서 나오는 기본 용어 정리
    - RDD: Resilient Distributed Dataset → 기본 분산 데이터셋 (불변, 분산, 장애복구 지원)
    - Transformation: 변환 연산 (실제 실행 X, DAG에 기록)
    - Action: 결과 반환 및 저장 연산 (실제 실행 트리거)
    - Lazy Execution: Action 호출 전까지 실행 미루는 방식
    - DAG: 연산 순서 및 의존성을 나타내는 그래프 (실행 계획)
    - Stage: DAG를 기반으로 나눈 실행 단계 (Narrow/Wide 기준)
    - Task: Stage 안에서 병렬로 실행되는 최소 단위 작업
    - Shuffle: Wide Transformation 시 데이터 재분배 과정 (비용 큼)
    - Executor: Task 실행 담당하는 JVM 프로세스 (노드 당 여러 개 가능)
    - Driver: 애플리케이션의 메인 컨트롤러, 스케줄링/분배 담당

- Spark 프로그램 실행 과정 정리
    - 사용자 코드 작성: RDD/DataFrame 생성, Transformation(변환), Action(결과)
    - Lazy Execution (변환만 정의): map(), filter() → DAG 생성 준비
    - Action 호출: collect(), saveAsTextFile()
    - DAG Scheduler가 DAG 최적화 후 Stage 분리
        - Narrow Transformation은 같은 Stage
        - Wide Transformation은 Shuffle 후 다른 Stage
    - Task Scheduler가 Task를 Executor로 분배
    - 병렬 처리 시작
    - 결과 수집 및 반환
        - Driver에 결과 반환하거나 외부 저장소에 저장

- collect() 같은 Action은 자칫하면 OOM(Out of Memory) 발생 가능 => Action이 성능 병목 지점일 수도 있음.
    - DAG와 Stage 분리를 이해해야 병렬 처리와 최적화를 할 수 있음.

- Driver로 수집하는 Action 주의
    - collect(), take() 등은 모든 데이터를 Driver 메모리로 가져온다 → 데이터가 크면 Driver OOM(Out of Memory) 날 수 있음!
    - foreachPartition() + 저장소(S3, DB 등)에 직접 저장하는 패턴 추천.

- 성능 최적화와 Shuffle
    - Action 실행 시 Wide Transformation이 포함되면 Shuffle이 발생
    - 네트워크 I/O와 디스크 Spill 유발
    - reduceByKey() 같은 건 Local Aggregation 후 Shuffle을 줄이는 대표적인 예.

- 스파크 스트리밍에서의 Action
    - Structured Streaming에서도 Action이 필요 → writeStream.start()가 Action임.
    - 여전히 Action이 없으면 Stream이 시작되지 않음. → Trigger나 Watermark 같은 처리도 여기서 실제로 동작.



### 2. Spark RDD, DataFrame, Dataset 심화

##### 2 - 1. RDD가 메모리 기반이라면서 왜 느릴 수 있는가? (Serialization, Garbage Collection 관점에서)
    - RDD
        - Spark에서 가장 기본적인 분산 데이터 구조
        - Immutable (불변) & 분산 컬렉션 → 여러 노드의 메모리에 데이터를 나눠서 저장
        - 메모리 중심으로 동작하기 때문에 Hadoop보다 빠르다지만, 경우에 따라 느려질 수도 있음.
    - 느려지는 이유
        - Serialization 문제: Executor 간 통신할 때나 메모리 저장 시 직렬화 필요 → 비효율적인 직렬화 포맷일 경우 오버헤드 발생
        - Garbage Collection 문제: RDD는 Java/Scala 기반의 JVM 메모리를 사용 → 객체가 많아지면 GC가 잦아지고 지연이 커짐

- 직렬화(Serialization) 문제
    - RDD는 기본적으로 데이터를 JVM 객체(Object)로 다룸
    - 데이터를 Executor 간 전송하거나 디스크에 저장하려면 직렬화/역직렬화 과정이 필요
    - 기본 직렬화 방식이 Java Serialization → 느리고 메모리 낭비 심함
    - 해결책
        - Kryo Serialization 사용 → 더 빠르고, 더 적은 메모리 사용
        - 설정: `sparkConf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")`

- Garbage Collection(GC) 문제
    - JVM 메모리 안에서 객체를 많이 생성하면 GC(가비지 컬렉션)이 자주 발생
    - GC가 잦아지면 Executor가 멈추고, Task 실행이 느려진다 (STW: Stop The World 현상)
    - 해결책
        - 데이터 포맷 최적화 → DataFrame, Dataset 사용 (메모리 내에서 더 최적화된 형태로 데이터 저장)
        - Tungsten 실행 엔진 활용 → JVM 객체를 아예 쓰지 않고 바이트 배열로 저장해서 GC 자체를 줄임 (뒤에서 설명!)

##### 2 - 2. DataFrame과 Dataset의 Catalyst Optimizer는 어떤 최적화를 수행하는가? 구체적인 예시와 함께 설명하시오.

- Catalyst Optimizer는 Spark SQL / DataFrame / Dataset의 쿼리 최적화 엔진 → Spark가 RDD보다 훨씬 빠르고 똑똑하게 동작할 수 있게 만든 핵심 기술!

- Catalyst Optimizer가 하는 일: 기본적으로 4단계 최적화를 한다.

1. 분석(Analysis): 테이블/컬럼/함수 등 논리적 구조 파악 → 스키마, 타입 체크

2. 논리 최적화(Logical Optimization): 중복 필터 제거, 불필요한 연산 제거 등 논리 최적화

3. 물리 계획 생성(Physical Planning): 물리적 실행 계획을 여러 개 생성 후 비용 기반 최적화(Cost-based Optimizer, CBO) 수행

4. 코드 생성(Code Generation): 효율적인 바이트코드(Java 바이트코드) 생성 → Whole-stage Code Generation으로 빠른 실행


- Catalyst가 수행하는 구체적인 최적화 예시
    1. Predicate Pushdown (필터 푸쉬다운): WHERE 조건을 가능한 한 빨리 적용 → 읽는 데이터 양 줄임
    - 예시: `SELECT * FROM logs WHERE date = '2024-03-01'` → 파티션 프루닝, 파일 스캔 최소화 (Parquet 같은 컬럼 포맷일 때 효과 극대화)
    - 파티션 프루닝: 파티션을 적용하면, WHERE 절에서 필요한 파티션만 읽도록 할 수 있음. => 이를 파티션 프루닝(Partition Pruning)이라고 함.
    - DPP, Dynamic Partition Pruning, 동적 파티션 프루닝을 스파크 3.0 이후로 자동 적용되고 있음. 
        - 이는 쿼리 계획 단에서 join 등으로 파티셔닝 된 컬럼과 안 된 컬럼이 있을 때 파티셔닝 된 컬럼을 먼전 연산하여 파티션 프루닝의 최적화를 적용할 수 있도록 함. => 성능 개선

    2. Constant Folding (상수 접기): 연산 중 고정값을 미리 계산 → 예시: `SELECT salary * (1 + 0.05) → salary * 1.05`

    3. Projection Pruning (필요한 컬럼만 가져오기): SELECT에 필요한 컬럼만 읽음 → 예시: `SELECT name FROM user_table` → 다른 컬럼은 스캔 안 함 (Parquet/ORC에서 효과적)
    - ORC: Hive, Spark에서 많이 사용되는 컬럼형 데이터 저장 포맷, 하이브나 하둡 최적화된 설계
        - 컬럼형이며, 강력한 압축(Zlib, Snappy, LZO, ZSTD) 제공
        - 빠른 조회, indexing(Min/Max, Bloom Filter, Row Index 등) 지원, Splittable & 병렬 처리 가능 => 하이브, 스파크의 분산 처리 엔진과 호환 좋음
        - 작은 파일이 많거나, 실시간 처리에는 부적합.
        - 반면 대량의 데이터를 높은 압축률로 저장하고, 컬럼 단위 배치 작업 등에는 적합함.
    
    4. Reordering Join (조인 순서 변경): Join 비용을 계산하고 가장 효율적인 순서로 조인 수행 → CBO가 이를 담당 (통계 정보가 있을 때 더 정확함)
    - CBO는 Cost-Based Optimizer의 약자
    - DB가 SQL 실행 계획(Execution Plan)을 세울 때, 어떤 방식으로 데이터를 조회하고 조인할지를 결정하는 역할을 하는 게 옵티마이저(Optimizer), 크게 두 종류
        - RBO (Rule-Based Optimizer): 미리 정해진 규칙에 따라 실행 계획을 짜는 방식
        - CBO (Cost-Based Optimizer): 통계 정보를 바탕으로 비용(Cost)을 계산해서, 가장 효율적인 실행 계획을 선택하는 방식
        - 조인 순서 변경은 CBO가 담당하는데, 이유는 조인의 순서가 전체 쿼리 성능에 큰 영향을 주기 때문
        - 예시로 작은 테이블과 큰 테이블을 조인할 때 작은 테이블을 먼저 읽어서 필터링하면 이후 조인이 빨라짐. => CBO는 테이블의 크기, 인덱스 유무, 데이터 분포 등 통계 정보를 이용해서 어느 테이블을 먼저 읽을지, 어떤 방식(중첩 루프, 해시 조인 등)으로 조인할지, 어떤 순서로 조인을 수행할지를 결정
        - CBO(Cost-Based Optimizer)는 통계 정보를 이용해서 실행 비용을 계산하고, 가장 효율적인 조인 순서와 방식을 선택하는 옵티마이저로, 통계가 정확할수록 더 좋은 실행 계획이 나옴.

- Catalyst 최적화 + Tungsten 엔진 = Spark SQL 최적화
    - Tungsten 엔진: Catalyst가 쿼리를 최적화했다면, Tungsten은 실행 단계에서 속도를 극대화하는 역할

- Tungsten이 하는 최적화

1. 메모리 관리 개선: 기존 JVM 객체 대신 메모리 관리 직접 수행 → Off-Heap 메모리 사용 → GC 문제 거의 없음 → CPU 캐시 최적화까지 신경 씀

2. Whole-stage Code Generation (WSCG): Catalyst의 최종 실행 계획을 바탕으로 → Java 바이트코드 생성 → Spark가 네이티브 코드 수준으로 빠르게 실행
    - 중간 Iterator 생성 안 하고 → Loop Unrolling, 브랜치 제거 등 적용, 실질적인 실행 시간 대폭 절감
    - 예시: filter + map → 하나의 코드 블록으로 통합하여 빠르게 실행
    - Whole-stage Code Generation이 왜 빠른가?
        - 인터프리터 방식이 아닌 컴파일 방식으로 실행
        - 중간 오브젝트 안 만들고 바로 CPU에 명령 → JVM이 아닌 Native에 가까운 속도를 가능케 함 => Spark SQL + DataFrame은 기본으로 이걸 사용!


##### 2 - 3. 타입 안정성과 성능은 Dataset에서 어떻게 충돌하는가? Scala와 Python에서 차이는?

- Dataset의 특징
    - 타입 안정성: 컴파일 타임에 타입 검사 가능 (Scala/Java)
    - 성능 최적화: Catalyst + Tungsten을 활용한 최적화 가능
    - 사용 가능 언어: 주로 Scala/Java (Python은 지원 안 함)

- 충돌하는 이유: 타입 안정성을 얻기 위해선 → JVM 객체 기반으로 처리하는 경우가 많음 (특히 Scala에서)
    - JVM 객체를 많이 만들면 → GC 부하 증가, 객체 관리 비용 발생
    - Catalyst 최적화를 방해할 수도 있음 → 특정 타입 구조가 복잡할 경우 → 최적화가 덜 일어날 수 있음
    - Dataset은 타입 안정성 때문에 최적화보다 타입 우선이 될 수 있음

- Scala와 Python의 차이
    - Scala / Java
        - Dataset 지원: 지원 (타입 안정성 제공)
        - 최적화 엔진: Catalyst + Tungsten 최적화 모두 적용 가능
        - 타입 안정성: 컴파일 타임 타입 검사 가능
    - Python
        - Dataset 지원: 지원 안 함 (동적 타입 언어이므로)
        - 최적화 엔진: DataFrame만 지원 → Catalyst 최적화만 부분 적용
        - 타입 안정성: 런타임에서 타입 검사 (불안정)

- 그럼에도 대부분 DataFrame을 사용함
    - Catalyst + Tungsten 최적화만으로도 충분히 빠름
    - Python에서는 어차피 DataFrame만 쓰게 돼 있음
    - Dataset은 복잡한 타입 관리가 필요한 경우에만 선택 → 단순 집계/ETL은 DataFrame으로 처리하는 경우가 많다고 함..

- 예시 코드로 차이 확인하기

1. DataFrame (Python)

```python
df = spark.read.json("examples/src/main/resources/people.json")
df.filter(df["age"] > 21).select("name").show()
```

2. Dataset (Scala)

```scala
case class Person(name: String, age: Long)
val ds = spark.read.json("examples/src/main/resources/people.json").as[Person]
ds.filter(_.age > 21).map(_.name).show()
```



### 3. Spark Execution & 내부 최적화

##### 3 - 1. Stage와 Task는 어떻게 나뉘고, Task Scheduling은 어떻게 작동하는가? Task 병렬성은 어떻게 조절할 수 있나?

- 전체 진행 순서 요약
    - User Code (RDD, DataFrame, Dataset)
    - Transformation
    - DAG 생성 (Logical Plan)
    - Action 호출 → DAG Scheduler 동작
    - Stage 나누기 (Narrow vs Wide 기준)
    - Stage → 여러 Task로 쪼갬
    - Task를 Executor에 병렬로 분배하고 실행 (Task Scheduler)

- Stage란?
    - Stage = 작업을 실행 단위로 나눈 묶음 (Step)
    - DAG를 쪼개서 실행 단위로 나눈 것이 Stage
    - Stage는 Pipeline으로 실행할 수 있는 Task 집합이라고 생각하면 됨.

- Stage 나누는 기준
    - Narrow Transformation: 같은 Stage에 포함됨. → 데이터가 같은 파티션 안에서 처리 가능 → 데이터 이동(Shuffle) 없음
    - Wide Transformation: Stage가 나뉘는 기준 → 데이터가 다른 Executor나 Partition으로 이동해야 함 → Shuffle 발생 → 이때 새로운 Stage가 만들어짐

- Stage 기준 예시
    - `RDD → map() → filter() → reduceByKey() → collect()`
    - map() → filter()까지는 Narrow Transformation → Stage 1
    - reduceByKey()는 Wide Transformation + Shuffle → Stage 2
    - collect()는 Action → 결과 반환하는 Task가 Stage 3 (없을 수도 있음)

- Task란?
    - Task = Stage 안에서 병렬로 실행되는 최소 작업 단위
    - Stage가 쪼개진 후 각 Partition별로 처리하는 작업
    - Stage 안에서 Partition 개수 = Task 개수 → Stage가 100개 파티션을 갖고 있다면, 이 Stage의 Task는 100개

- Task의 역할
    - Partition 데이터를 가져와서 Transformation 연산 수행
    - Executor가 Task를 담당해서 실행 → 한 Executor에서 여러 Task를 병렬 실행 가능

- Task Scheduling: Task를 어디서 실행할지, 어떤 Executor가 담당할지 결정하는 과정
    - 동작 순서
    - DAG Scheduler가 Stage를 쪼갬
    - Task Scheduler가 Stage의 Task 목록 생성
    - 클러스터 매니저(YARN, K8s 등)가 리소스(Executor) 할당
    - Executor에 Task 분배 후 병렬 실행 → 기본적으로 데이터 로컬리티(Data Locality) 우선 → 데이터가 있는 노드 근처 Executor를 우선 배정 (네트워크 비용 절감)

- 데이터 로컬리티 수준
    - Locality Level, 설명
    - PROCESS_LOCAL: Task와 데이터가 같은 Executor 프로세스 안에 있음
    - NODE_LOCAL: 같은 노드에 있지만 다른 Executor에서 데이터 가져옴
    - RACK_LOCAL: 같은 랙 안에 있음 (네트워크 I/O 발생)
    - ANY: 어디든 상관없이 실행 (로컬리티 보장 안 함)
    - Locality가 높을수록 네트워크 비용 줄고 빠르다!

- Task 병렬성은 어떻게 조절할 수 있나?
    - 병렬성 = 동시에 몇 개의 Task가 실행되는가 → 데이터 분산, 클러스터 리소스 사용에 직접적인 영향을 줌.
    - 방법 1. Partition 수 조절하기
        - Partition = Task 수
        - 데이터 소스나 Transformation에서 결정됨
        - 기본적인 결정 기준
            - 단계별 기본 Partition 수
            - 파일 읽기 (HDFS 등): 블록 수에 따라 Partition 생성 (기본 128MB 블록 기준)
            - RDD 생성: sc.parallelize(data, numPartitions)에서 명시 가능
            - Shuffle 이후: spark.sql.shuffle.partitions 기본값 200 (조절 가능)

    - 방법 2. 병렬성 파라미터 조절하기
        - 기본 병렬성 설정 (RDD 기준) => `spark.default.parallelism`
            - 기본 Task 병렬성 수
            - 보통 클러스터 전체 CPU 코어 수와 연관됨 → Executor 코어 * Executor 개수
        - Shuffle 병렬성 설정 (DataFrame/SQL 기준) => `spark.sql.shuffle.partitions`
            - Shuffle 이후 생성할 Partition 수
            - 기본값 200 → 데이터 양이 많으면 이걸 더 늘려야 함
            - 파티션이 너무 적으면 병목 발생 / 너무 많으면 오버헤드 발생 → 보통 데이터 크기에 따라 2~4배 정도로 조절

    - 방법 3. Executor와 Core 수 조절
        - Executor 당 코어 수 → 각 Executor가 동시에 처리할 수 있는 Task 수 → `--executor-cores` 옵션으로 설정
        - Executor 수 → 전체 클러스터에 분배할 Executor 개수 → `--num-executors` 옵션으로 설정

    - 예시
    ```bash
    spark-submit \
    --executor-cores 4 \
    --num-executors 10
    ```
    - 총 4 * 10 = 40개의 Task가 동시에 실행 가능

- 병렬성 조절 팁
    - 입력 데이터 파티션 수 파악하기 → 데이터 크기 / 블록 크기 기준으로 Partition 수 확인
    - Stage마다 Task 개수 확인하기 → Spark UI → Stage → Tasks에서 확인
    - Task가 과도하게 적으면 → 병렬도 부족 → 느려짐 → spark.default.parallelism / spark.sql.shuffle.partitions 조절
    - Task가 과도하게 많으면 → 스케줄링 오버헤드 / 작은 Task로 인한 비효율 발생 
        - 적절한 파티션 크기 기준: 128MB ~ 256MB 추천 (파일 포맷과 작업 종류에 따라 다름)
    - Dynamic Allocation 사용 가능성 고려 → Task 수에 따라 Executor 수를 자동 조절 가능 → spark.dynamicAllocation.enabled=true


##### 3 - 2. Narrow vs Wide Transformation 차이점? Wide Transformation이 발생할 때 성능 최적화 방안은?

차이점: Spark에서 Stage를 나누는 기준이자, Shuffle 발생 여부와 성능 최적화의 핵심

- Narrow Transformation: 데이터가 파티션 간 이동 없이, 같은 파티션 내에서 처리되는 연산.

- 특징
    - 데이터 재분배(Shuffle)가 발생하지 않음
    - Pipeline 병합이 가능 → Catalyst가 Transformation을 묶어서 최적 실행 계획 생성
    - Stage가 나뉘지 않고, 빠른 실행 가능
    - 메모리/네트워크/디스크 I/O 부하가 거의 없음
    - Executor가 데이터 로컬리티를 활용해서 빠르게 실행

- 예시 (DataFrame 기준)
    - select(): 필요한 컬럼만 선택
    - filter() / where(): 조건에 맞는 데이터만 필터링
    - withColumn(): 컬럼 추가 또는 변형
    - limit(): 일정 수만 가져오기
    - mapPartitions(): 파티션 단위 연산

- Wide Transformation: 데이터가 파티션 간에 이동(Shuffle)이 발생하는 연산.

- 특징
    - 데이터 재분배(Shuffle)가 필수
    - Stage가 나뉘고, 다음 Stage에서 데이터를 다시 정렬하거나 그룹화해서 처리
    - 네트워크 I/O 발생 → Executor 간 통신이 필요
    - 디스크 Spill 가능성 있음 → 메모리 초과 시 디스크에 저장 후 다시 읽어야 함
    - 성능 저하 원인이 되기 쉬움 (대규모 데이터 이동으로 인한 병목)

- 예시 (DataFrame 기준)
    - groupBy(): 그룹화 → Aggregation 시 Shuffle
    - distinct(): 중복 제거 시 전체 데이터 이동
    - join(): 조인 시 키 기준으로 재분배 필요
    - repartition(): 파티션 재분배 (파티션 수 변경 시 Shuffle)
    - orderBy() / sort(): 정렬 시 전체 데이터 정렬 필요

- Narrow Transformation
    - Shuffle 발생: 없음
    - Stage 나뉨 여부: 같은 Stage
    - 병목 가능성: 낮음
    - 실행 최적화: Pipeline 병합 → 빠름
    - 예시: select, filter

- Wide Transformation
    - Shuffle 발생: 발생
    - Stage 나뉨 여부: Stage 경계가 나뉨
    - 네트워크 I/O: 네트워크 통신 필요
    - 병목 가능성: 높음 (네트워크, 디스크, GC 병목)
    - 실행 최적화: 데이터 스큐/조인 최적화 필요
    - 예시: groupBy, join, repartition


- Wide Transformation이 발생할 때 성능 최적화 방안: Shuffle을 줄이고, 발생할 경우 병목을 최소화하는 게 핵심 전략!

1. Partition과 병렬성 최적화: `spark.sql.shuffle.partitions` 조정, 기본값은 200
    - 데이터가 크면 Partition을 늘려서 병렬성 확보 → 하지만 너무 많아도 오버헤드가 발생함
    - 권장 기준
        - Shuffle 이후 파티션당 데이터 크기 128MB ~ 256MB
        - "데이터 사이즈 / 적정 파티션 크기"로 계산해서 튜닝

```python
spark.conf.set("spark.sql.shuffle.partitions", "400")
```

2. coalesce()와 repartition() 올바르게 사용
    - repartition(): 파티션 수를 늘리거나 데이터 재분배할 때 사용
        - Shuffle 발생 → 데이터가 재분배되며 비용 발생 → Wide Transformation

```python
df = df.repartition(100, "keyColumn")
```

    - coalesce(): 파티션 수를 줄일 때 사용, Shuffle 없음
        - Narrow Transformation으로 처리 가능 → 특정 Executor에 파티션이 집중될 수 있으므로 주의!

```python
df = df.coalesce(10)
```

3. 조인(Join) 최적화 → Shuffle 비용 줄이기
    - Broadcast Join 사용하기: 작은 테이블은 모든 Executor로 복제(Broadcast)
    - Shuffle이 발생하지 않아서 네트워크 I/O와 디스크 IO 감소
    - Spark가 자동으로 판단하지만 직접 설정 가능
    - Broadcast 기준: `spark.sql.autoBroadcastJoinThreshold` → 기본 10MB 이하면 자동 Broadcast

```python
# 브로드 캐스트 조인 명시적 지정
from pyspark.sql.functions import broadcast
df_large.join(broadcast(df_small), "id")

# 브로드 캐스팅 조인 기준
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "50MB")
```

- Skew Join (데이터 스큐) 처리: 특정 Key에 데이터가 몰리면 Executor가 한쪽만 과부하됨

- 해결 방법
    - Salting → Key에 랜덤값을 추가해서 데이터를 고르게 분산
    - Adaptive Query Execution (AQE) 활성화 → Skew Join 자동 처리

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")  # AQE 활성화
```

4. Adaptive Query Execution (AQE) 활용

- AQE: Spark 3.0부터 제공되는 실행 시점 동적 최적화 기능

- 주요 기능
    - 동적 파티션 재분배 → 실제 실행 중 파티션 크기를 분석해서 재조정
    - Skew Join 처리 자동화 → Skew가 발견되면 자동으로 분리/다른 방법 사용
    - Broadcast Join 자동화 → 실행 중 Join 크기 판단해서 Broadcast 여부 결정

- 사용법

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")  # AQE 사용 설정
spark.conf.set("spark.sql.adaptive.shuffle.targetPostShuffleInputSize", "64MB")  # Shuffle 이후 각 Task가 가져가는 Partition의 크기 기준값, 대략 이정도가 되도록 파티션을 나눠줌.
```

5. 파일 포맷 최적화 → Shuffle 데이터 줄이기

- 컬럼 기반 포맷 사용 (Parquet / ORC): Parquet + Predicate Pushdown을 통한 읽는 데이터 최소화

- Catalyst가 필터를 Pushdown 시켜서 읽기 I/O 절감

- 불필요한 데이터 안 읽으면 → Shuffle 대상 데이터도 줄어듦!

- Parquet 저장 예시

```python
df.write.mode("overwrite").parquet("/path/to/output")
```

6. 리소스 최적화

- Executor와 Core 수 조정
    - Executor 당 적절한 코어 수 → 4 ~ 5개 권장 (너무 많으면 GC 지연 발생)

- 메모리 크기 → 작업에 맞는 적절한 메모리 할당 (Shuffle Spill 고려)

```bash
--executor-cores 4
--executor-memory 8G
--num-executors 10
```

- 최적화 전략 요약
    - Partition 수 최적화: spark.sql.shuffle.partitions 조정 → 데이터 크기 기반 병렬성 확보
    - 조인 최적화: Broadcast Join 사용, Skew 처리 (AQE, Salting)
    - AQE 활성화: Adaptive Query Execution으로 실행 시점 최적화
    - 데이터 포맷 최적화: Parquet / ORC 사용, Predicate Pushdown → 읽기 I/O 감소
    - 리소스 튜닝: Executor/Memory/Core 최적값 설정
    - Coalesce / Repartition 최적화: 필요한 시점에 정확히 사용, 불필요한 Shuffle 방지


##### 3 - 3. Shuffle 과정은 왜 비용이 많이 드는가? Shuffle을 피하거나 최적화하는 방법은?

- Shuffle: 파티션 간 데이터 재분배 과정
    - 특정 연산이 데이터를 기존 파티션으로 처리할 수 없을 때 발생
    - 데이터를 키 기반으로 재분배(분산)하거나, 정렬 및 그룹화가 필요할 때 실행됨

- 보통 Wide Transformation 이후 발생 => 예: groupBy(), join(), distinct(), orderBy()

- Shuffle가 발생하는 이유
    - 데이터의 키에 따라 그룹화해야 할 때 → 각 Executor가 가지고 있는 파티션에 같은 키가 있는 데이터가 모여있지 않음
    - 데이터를 다시 파티셔닝해야 할 때 → repartition(), coalesce()(증가 시), distinct()

- Shuffle 과정 상세
    - Stage 1 (Map Side)
        - 각 Partition에서 데이터를 분할 및 정렬 → 메모리 버퍼
        - 메모리 초과 시 Spill(디스크 임시 저장)

    - 네트워크 전송 (Shuffle)

    - Stage 2 (Reduce Side)
        - 다른 Executor에서 데이터를 수신
        - 데이터를 다시 정렬 및 병합 → 메모리 버퍼
        - 메모리 초과 시 Spill(디스크 임시 저장)

- Shuffle이 비용이 많이 드는 이유 (심화)
    - 네트워크 IO: Executor 간 데이터 전송 필요 → 클러스터 네트워크 부하 발생
    - 디스크 IO (Spill): 메모리에 다 못 올리는 데이터는 디스크에 임시 저장 → 디스크 읽기/쓰기 비용 발생
    - CPU Overhead: 데이터 정렬(Sort), 압축/역압축, 직렬화/역직렬화 비용 발생
    - 메모리 사용량: 정렬/병합 처리에 메모리 많이 씀 → GC(가비지 컬렉션) 부담 증가
    - GC Pause: 메모리에서 객체가 늘어나면 JVM GC가 자주 발생 → Stop-The-World 지연

- Shuffle을 피하거나 최적화하는 방법

1. Narrow Transformation 우선 사용
    - filter(), select(), withColumn() → Shuffle 안 일어나니까 빠름!
    - Wide Transformation은 꼭 필요한 경우에만 사용

2. Partition 수와 사이즈 최적화
    - spark.sql.shuffle.partitions → Shuffle 이후 생성할 파티션 수 조정
    - 기본값: 200개 (과하거나 부족하면 병목/오버헤드 발생), 데이터 크기에 비례해서 조정, Shuffle 후 파티션당 데이터 크기 기준 128MB ~ 256MB 추천

```python
spark.conf.set("spark.sql.shuffle.partitions", "400")  # 데이터 크기에 따라 조정
```

3. Broadcast Join 사용으로 Shuffle 피하기

- Join하는 한쪽 데이터가 작은 경우 (기본 10MB 이하) 작은 테이블을 모든 Executor로 복제 → Shuffle 없이 Local Join 가능!

```python
from pyspark.sql.functions import broadcast
df_large.join(broadcast(df_small), "id")
```

- 관련 파라미터

```python
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "50MB")  # 크기 상향 가능
```

4. Skew(데이터 쏠림) 처리

- 특정 Key에 데이터가 몰리면 → 일부 Executor만 과부하 → 나머지는 Idle → Shuffle이 오래 걸리고 Task가 비효율적 실행

- 해결책

1. Salting 기법: Key에 랜덤값 추가 → Key를 인위적으로 분산시킴

```python
import pyspark.sql.functions as F
salted_df = df.withColumn("salt", F.rand() * 10).withColumn("new_key", F.concat_ws("_", "key", "salt"))
```

2. Adaptive Query Execution (AQE) 사용

- Spark 3.x 이상, 실행 중 데이터 스큐 탐지 후 자동으로 동적 분할 / 재분배

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
```

5. Repartition / Coalesce 사용법 최적화

- repartition(): 파티션 수 늘릴 때 사용, Shuffle가 발생하므로 남발 금지!

```python
df.repartition(100, "id")
```

- coalesce(): 파티션 수 줄일 때 사용, Shuffle 없이 Narrow Transformation 처리 가능

```python
df.coalesce(10)
```

6. 파일 포맷과 파티셔닝 전략 최적화

- Parquet / ORC 사용: 컬럼 기반 포맷 → Predicate Pushdown / Projection Pruning 가능

- Predicate Pushown: 필터 조건을 더 하위 시스템(데이터 저장소/파일 포맷)에 전달해서, 처음부터 걸러서 가져오는 최적화 기법
    - Spark가 필터 조건(WHERE절)을 파일 포맷(Parquet, ORC), 데이터베이스, 스토리지 엔진 에 넘겨서 필요한 데이터만 읽게 하는 최적화 기법
    - Parquet/ORC은 Columnar 포맷이라서, 컬럼별로 데이터가 정렬돼 있고, 메타데이터(통계 정보)가 포함돼 있음 => 더 강력한 최적화 효과
    - Parquet, ORC, JDBC(일부 DB만) 지원, Avro는 지원하지 않음.

```python
spark.conf.set("spark.sql.parquet.filterPushdown", "true")
spark.conf.set("spark.sql.orc.filterPushdown", "true")
```
- Projection Pruning: Spark가 SELECT 절에서 지정한 컬럼만 읽도록 파일 포맷(Parquet, ORC), DB에서 컬럼을 제한해서 데이터 읽는 최적화 기법
    - 역시 Parquet, ORC는 Columnar 포맷, 컬럼 단위로 저장됨 => 읽기 IO가 컬럼 단위로 이루어지기 때문에, 필요한 컬럼만 읽으면 나머지 컬럼은 아예 디스크 접근 안 하므로 더 최적화에 좋음.
    - 특히 Spark SQL / DataFrame에서는 Catalyst가 이 최적화를 자동으로 적용

```python
spark.conf.set("spark.sql.parquet.columnPruning", "true")  # 기본 true
```


- 디렉토리 파티셔닝
    - S3나 HDFS에서 데이터를 디렉토리 기준으로 파티셔닝 => 필터 푸쉬다운 + 파티션 프루닝 → 불필요한 데이터 안 읽음 → Shuffle 감소

```python
df.write.partitionBy("country").parquet("/path/to/output")
```

7. AQE (Adaptive Query Execution) 활성화

- 실행 시점에 파티션 크기, 조인 방식, Skew 처리 동적 최적화

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.shuffle.targetPostShuffleInputSize", "64MB")
```

8. Compression 설정

- Shuffle 데이터는 기본적으로 압축하여 전송 가능 => 네트워크 비용 감소, 디스크 IO 절감

```python
spark.conf.set("spark.shuffle.compress", "true")  # 기본 true
spark.conf.set("spark.shuffle.spill.compress", "true")  # 기본 true
```


##### 3 - 4. Speculative Execution이란 무엇인가? 언제 유용하고, 언제 오히려 독이 되는가?

- Speculative Execution: 느려터진 Task(느린 노드)가 있다면 뒤처진 작업을 복제해서 다른 노드에서 동시에 실행하는 것
    - 누가 더 빨리 보고 가장 먼저 끝난 결과만 사용하고, 나머지는 버림. => 두 개의 Task 중 먼저 끝난 것을 취하고, 나머지는 Kill함.

- 언제 작동하나
    - 일부 노드가 느리면 전체 Job이 느려진다 → 이것 때문에 전체 작업이 지연됨.
    - Spark는 이를 해결하기 위해, 진행률이 평균보다 현저히 낮은 Task를 감지하면 다른 Executor(Node)에 복사해서 재시도


- Speculative Execution이 유용한 경우

1. 노드 성능 차이가 있을 때

- 클러스터에 있는 노드들이 똑같이 빠르지 않다면, 어떤 노드는 느리게 동작할 수 있음. → 이런 성능 편차를 완화시켜줌.


2. 하드웨어 문제나 장애가 있을 때

- 네트워크 불량, 디스크 느림, CPU 병목 같은 일시적인 슬로우 노드가 있을 경우에 효과적.

3. 작업이 균등하게 분할되지 않을 때

- 데이터 Skew(데이터가 한쪽에 치우쳐 있는 현상)가 발생하면 어떤 Task는 데이터가 많아서 오래 걸릴 수 있음. 이럴 땐 뒤처진 Task를 복제해서 빠른 노드에서 병렬 처리 가능!


- Speculative Execution이 오히려 독이 되는 경우
    - 리소스 낭비: 복제 실행은 리소스를 두 배로 사용 → 클러스터 전체 자원이 빡빡하다면 다른 작업까지 지연될 수 있음.
    - I/O 부하 증가: 동일한 데이터를 다시 읽어야 하니까 네트워크 대역폭, 디스크 I/O가 과부하될 수 있음.
    - 데이터 Skew 해결엔 한계: 데이터 Skew가 심하면? 복제해도 결국 똑같이 느릴 뿐임. → Speculative Execution이 근본적 해결이 아님.
    - 실행 환경이 이미 최적화돼 있다면 오히려 방해: 노드들이 동일한 성능이고 클러스터가 리소스에 민감한 상황에서는 리소스 낭비만 초래하고 전반적인 처리 속도를 떨어뜨릴 수 있음.

- 설정법

```bash
spark.speculation                 # 기본값: false (비활성화)
spark.speculation.quantile        # 느린 Task 판별 기준 (기본 0.75 → 75%보다 느린 경우 의심)
spark.speculation.multiplier      # 평균보다 몇 배 느리면 재실행할지 기준 (기본 1.5배)
spark.speculation.task.duration.threshold  # 특정 시간보다 오래 걸려야 의심 (예: 10초 이상)
```



### 4. 메모리와 스토리지 관리

##### 4 - 1. Spark 메모리 구조(Execution vs Storage)는 어떻게 동작하는가? Dynamic Allocation은 어떤 상황에서 비효율적일까?

- Spark 메모리 구조: Execution vs Storage
    - Spark는 기본적으로 JVM 위에서 동작 => 메모리 관리를 Heap 기반으로 함.
    - 하지만 RDD 캐싱, 셔플, Aggregation 등 고성능 처리를 위해 메모리 관리 전략이 따로 존재

- Unified Memory Management (통합 메모리 관리, Spark 1.6 이전은 Old 방식, 1.6 이후 기본은 Unified 방식!)
    - 전체 메모리 공간: Executor Memory 전체에서 → Reserved Memory 조금 빼고 → 나머지를 Unified Memory로 씀.

- Unified Memory의 두 가지 영역
    - Execution Memory: 셔플, 조인, 집계(aggregation), 정렬(sort) 등 계산에 쓰는 메모리
    - Storage Memory: RDD Cache/Persist, 브로드캐스트 변수 저장 등에 사용
    - 기본적으로 Execution과 Storage가 유동적으로 공유됨.
    - 예를 들어 Execution이 부족하면 Storage를 잠식해서 더 가져갈 수 있음. (반대로 Storage도 필요하면 가져감)

- Execution vs Storage 동작 예시
    - 셔플 작업이 발생해서 Execution Memory가 부족하다 => Storage 공간을 뺏어오고, 필요하면 RDD Cache도 지워버린다.
    - 반대로 Cache가 필요할 때 Execution이 여유롭다 → Execution에서 메모리 가져와서 Storage에 사용 가능.

- 메모리 할당 흐름

```
Executor JVM 메모리 (heap)
├── Reserved Memory (고정 영역, 대략 300MB)
└── Usable Memory
     └── Unified Memory
          ├── Execution Memory
          └── Storage Memory
```

- Dynamic Allocation이란?
    - Executor 개수를 동적으로 조절하는 기능 → 필요할 때 Executor를 늘리고 → 놀고 있는 Executor는 죽여서 자원 아끼는 전략.
    - 동작 방식: 잡이 데이터를 많이 처리 중이면 → Executor를 늘린다!
    - 잡이 Idle 상태거나 Task가 없다면 → Executor를 줄인다!
    - 핵심 메커니즘: Task 수 모니터링 → Executor 수 결정
    - 외부 리소스 매니저(YARN, Kubernetes 등)와 연동해서 동적 요청/반납 수행


- Dynamic Allocation이 비효율적인 경우

1. Executor 초기화 시간이 긴 경우
    - Executor를 늘렸다 줄였다 할 때 → 초기화 시간이 오래 걸리면 오히려 비효율. (특히 컨테이너 기반 Kubernetes 환경에서 느릴 수 있음)

2. 셔플 파일이 많을 때
    - Executor가 죽으면 로컬에 있던 Shuffle 파일도 사라짐! → 나중에 다른 Executor가 다시 파일 찾으려면 → 네트워크 I/O가 폭증 → 퍼포먼스 저하 (특히 Large Shuffle 시나리오에서 심각)
    - 이 문제를 해결하려고 등장한 게 External Shuffle Service (ESS): Executor가 죽어도 Shuffle 데이터는 외부 서비스가 관리해줌!
    - Spark on Kubernetes는 ESS 기본 지원 없음 → 이게 약점

3. Streaming 같은 Long-Running Job
    - Streaming은 계속 Task가 들어왔다 나갔다 하니까 Executor가 동적으로 생겼다 없어졌다 반복되면 → 오히려 안정성 저하 + 오버헤드 증가

4. 데이터 Skew나 Task 불균형
    - Task가 한쪽 Executor에 집중될 수 있음 → 일부는 Idle이라 줄이고, 일부는 Task 몰려서 느려짐 → 리소스 할당의 불균형이 생김.



- 튜닝 방법
    - `spark.dynamicAllocation.enabled` → true/false
    - `spark.dynamicAllocation.minExecutors`
    - `spark.dynamicAllocation.maxExecutors`
    - `External Shuffle Service` 활성화 필수 (클러스터 환경에 따라 다름)


##### 4 - 2. GC(가비지 컬렉션)가 Spark Job 성능에 미치는 영향과 튜닝 방안은?

- GC(가비지 컬렉션)가 Spark Job 성능에 미치는 영향
    - Spark는 대용량 데이터를 처리하면서 RDD/Persist/Shuffle 등으로 객체를 엄청나게 생성함.
    - 이 객체들이 계속 JVM Heap 메모리를 차지하고, 메모리가 부족하면 GC가 빈번하게 발생함.
    - GC 시간이 길어지면 Executor가 멈춰버림 → CPU는 GC만 돌고 있어서 → Task 처리 시간 지연, Job이 느려짐 → 심하면 OutOfMemoryError(OOM)로 Executor 죽음

- GC가 Spark 성능에 미치는 영향 (현상별로 정리)
    - GC 시간이 너무 길다: Executor가 Pause 상태, Task가 멈추고 Job 전체 지연 발생
    - Full GC가 자주 일어난다: 모든 Thread가 멈춤 → Job 전체가 정지 상태
    - 메모리 부족으로 OOM 발생: Executor가 죽고 다시 실행됨 → Retry 증가, Shuffle 데이터 유실
    - Shuffle 데이터 유실: Executor 재시작 시 Shuffle 파일이 사라져 네트워크 병목 발생

- Spark에서 자주 보이는 GC 관련 문제 상황
    - Shuffle-heavy Job → 데이터가 많아서 객체 생성 폭발 → 셔플 데이터를 계속 유지해야 해서 GC 빈번
    - RDD를 persist 했는데 메모리 부족 → RDD가 Storage 메모리를 먹고 있으니 Execution 메모리가 부족해지고, GC가 과다하게 발생함.
    - 데이터 Skew가 심해서 특정 Executor만 터짐 → 메모리 과점유 → GC 폭발 → Executor 죽음


- Spark GC 튜닝 전략과 방안

1. 메모리 구조를 이해하고 분배를 최적화하자

- Executor Memory 설정

```bash
spark.executor.memory              # Executor 한 개당 메모리 크기
spark.executor.memoryOverhead      # JVM 외 영역 (native code, shuffle buffer 등)
```

- 튜닝 포인트
    - 메모리가 부족하면 GC가 많이 발생함.
    - memoryOverhead 부족하면 native memory 부족으로 crash → 특히 셔플/네트워크가 많으면 넉넉하게 주자
    - 기본값: executorMemory * 0.10 또는 최소 384MB → 보통 512MB 이상 추천

2. GC 알고리즘 선택이 중요하다

- JVM 기본은 Parallel GC, 하지만 Spark에 더 적합한 경우도 있음!
    - Parallel GC: Throughput은 높지만 Stop-the-World가 길 수 있음 => 기본값 (작업 단순할 때 무난)
    - G1GC: Pause Time 짧고 메모리 큰 경우 안정적 => 대규모 Executor 메모리 할당 시 추천
    - ZGC/Shenandoah: 지연 시간 최소화 (초저지연) => 최신 JVM 버전 사용 가능 시 실험해볼만함

- G1GC로 세팅하는 법

```bash
spark.executor.defaultJavaOptions=-XX:+UseG1GC
spark.driver.extraJavaOptions=-XX:+UseG1GC
```

3. 객체 수 줄이기 & 메모리 관리 최적화

- 데이터 직렬화 포맷 변경: 기본은 Java Serialization → 비효율적임
- Kryo Serialization으로 변경 추천 → 객체 크기 감소 → GC 오버헤드 감소

```bash
spark.serializer=org.apache.spark.serializer.KryoSerializer
```

- RDD persist()에 storage level 최적화
- MEMORY_ONLY vs MEMORY_AND_DISK 선택 잘해야 함. → 메모리 부족하면 MEMORY_AND_DISK로 디스크 쓰자. → 메모리에만 넣으려고 억지 쓰다 OOM + GC 폭발

4. Shuffle 데이터 최적화

- Shuffle-intensive Job은 GC에 악영향

```bash
spark.shuffle.compress=true  # Shuffle 데이터 크기 줄이기 → 메모리 사용 절약
spark.shuffle.spill.compress=true  # Disk Spill 시 I/O 최적화
```

5. Dynamic Allocation을 피하거나 External Shuffle 사용

- Executor가 죽고 살아나면 Shuffle 재다운로드 필요 → GC 부담 + 네트워크 부담 → External Shuffle Service 활성화 필수 (특히 YARN)

6. Task 수 조정으로 GC 분산

```bash
spark.default.parallelism

spark.sql.shuffle.partitions
```
- Task 수를 늘리면 Executor당 메모리 부담이 줄어들어 GC 부하 완화 (너무 늘리면 오버헤드 있음 → 적절히 조정!)


- 문제 상황에서 GC 확인하는 법

- Spark UI → Executor → GC Time(%) 확인 → GC Time이 전체 작업 시간의 10% 이상이면 위험 신호!

```bash
jstat -gc <pid>
jmap -histo:live <pid>
```

- GC 로그 활성화해서 분석:

```bash
spark.executor.extraJavaOptions=-verbose:gc -XX:+PrintGCDetails -XX:+PrintGCTimeStamps
```

##### 4 - 3. Spill-to-Disk가 발생하는 조건과 이를 줄이기 위한 방법은?

- Spill-to-Disk: 메모리가 부족하면 디스크로 데이터를 흘린다 → 계산 중 메모리에 다 못 담아서 디스크로 저장하는 현상.

- Spark는 기본적으로 메모리 기반 처리 엔진 하지만 메모리 부족하면 어쩔 수 없이 중간 결과 데이터나 임시 데이터를 디스크로 Spill(흘림)

- Spill이 발생하는 경우

1. Aggregation(집계)나 Join, Shuffle 단계
    - 데이터를 메모리에 올려서 집계/정렬/조인하려는데 메모리 초과하면 일부 데이터를 디스크에 써버림.
    - 예시: `groupByKey()`, `reduceByKey()`, `sortBy()`
    - shuffle join (특히 SortMergeJoin, ShuffleHashJoin)

2. Shuffle 단계에서

- map-side에서 데이터를 정렬하거나 파티션으로 나누고 reduce-side에서 다시 집계하거나 정렬할 때 → 메모리 초과 → Spill 발생.

3. Sort, Hash 테이블이 메모리를 넘칠 때

- Sort 연산이 많을 경우: 정렬 과정 중 메모리 부족하면 Spill. Hash Aggregation이 많을 경우: 해시 테이블이 메모리 초과하면 Spill.


- Spill이 문제인 이유
    - 디스크 I/O가 느리다!
    - 메모리 → 디스크 → 다시 메모리로 로드 → 느려진다.
    - 네트워크 오버헤드: Shuffle Spill이 많아지면 네트워크도 병목 발생!
    - Job 전체 속도 저하: Spill이 자주 발생하면 계속 디스크 I/O → 전반적인 작업 시간 증가

- Spill-to-Disk 발생 조건
    - Execution Memory 부족: 집계, 정렬, 조인 등에서 메모리 부족 시 발생
    - Hash 테이블이 메모리 초과: Hash Aggregation/Join 시 테이블 크기가 너무 클 때
    - Sort 메모리 부족: 정렬을 위한 데이터가 커서 메모리 초과할 때
    - Shuffle 데이터 큼: Shuffle Stage에서 데이터가 크면 Spill 발생 가능

- Spill을 줄이기 위한 방법

1. 메모리 확보가 최우선

- Executor 메모리와 오버헤드 늘리기: 메모리가 충분하지 않으면 Spill은 필연적
```bash
spark.executor.memory=8g
spark.executor.memoryOverhead=1g
```


- Task 수 늘리기 (더 많은 Executor로 분산): Task 수 늘리면 각 Task가 처리하는 데이터가 적어짐 → Spill 줄어듦

```bash
spark.sql.shuffle.partitions=800    # 기본값은 200, 데이터 크기에 따라 증가 추천!
spark.default.parallelism=800
```


2. 집계 방식 바꾸기

- `groupByKey()` → `reduceByKey()` 또는 `aggregateByKey()`로 대체 => groupByKey()는 모든 값을 메모리에 모으기 때문에 → Spill 유발이 심하다
    - reduceByKey()는 로컬에서 미리 집계 후 Shuffle → 메모리 사용량 절감!

3. Join 전략 변경하기

- SortMergeJoin 사용: 큰 테이블 조인할 경우 Broadcast Hash Join보다 효율적

- SortMergeJoin은 메모리를 덜 쓰고 Spill도 줄어듦

```bash
spark.sql.autoBroadcastJoinThreshold=-1    # Broadcast Join 비활성화
```

- 데이터 Skew 조정: Skew 심하면 특정 Task만 데이터 폭주 → Spill 폭발
    - Salting 같은 방법으로 Skew 분산 추천

4. Shuffle 관련 최적화: Shuffle 파일과 Spill 파일을 압축해서 I/O 비용 줄이기

- 압축 설정

```bash
spark.shuffle.compress=true
spark.shuffle.spill.compress=true
```


- spark.shuffle.file.buffer 조정: Shuffle 파일 쓸 때 버퍼 크기, (기본값 32k → 데이터 클 경우 64k 이상 추천)

```bash
spark.shuffle.file.buffer=64k
```


5. Serialization 개선

- Kryo 직렬화 사용: 기본 Java Serializer보다 빠르고 공간 절약됨 → 객체 크기 줄여서 Spill 방지!

```bash
spark.serializer=org.apache.spark.serializer.KryoSerializer
```


6. Spark SQL 옵션 튜닝 → 동적 파티셔닝 재조정, Skew 처리 자동화 등으로 Spill 줄이기 가능!

```bash
spark.sql.adaptive.enabled=true                   # AQE (Adaptive Query Execution)
spark.sql.adaptive.shuffle.targetPostShuffleInputSize=64MB
```


- 추가 팁
    - 모니터링으로 Spill 확인: Spark UI → Stage/Task Details에서 Spill 기록 확인 가능
    - "Shuffle Spill (Memory)", "Shuffle Spill (Disk)" 값이 높으면 → 손을 대야 함



### 5. 조인과 데이터 스큐(Data Skew)

##### 5 - 1. Broadcast Join과 Shuffle Hash Join 차이점? 언제 Broadcast Join을 강제로 써야 할까?

1. Broadcast Join vs Shuffle Hash Join

- Broadcast Join: 작은 테이블 하나를 전체 Executor에 "방송"해서 큰 테이블을 각 Task가 로컬에서 조인하는 방식
    - 장점: Shuffle 발생 안 함 → 성능 매우 빠름, 큰 테이블 쪼개기 없이 로컬에서 바로 조인 가능
    - 단점: Broadcast 대상 테이블이 너무 크면 OOM 발생 위험, Executor 메모리에 테이블을 담을 수 있어야 함

- 사용 조건: Broadcast 대상 테이블이 10MB ~ 수백 MB 이하, Executor 메모리에 올릴 수 있어야 함

- 강제로 사용하는 법

```python
broadcast(df_small)
```

```sql
SELECT /*+ BROADCAST(df_small) */ ...
```

- 자동 Broadcast 조건

```bash
spark.sql.autoBroadcastJoinThreshold = 10MB   # 이 값보다 작으면 자동 Broadcast Join
```

- Shuffle Hash Join: 두 테이블 모두 키 기준으로 Shuffle => 같은 키끼리 같은 파티션으로 모은 뒤 => 각 파티션 내에서 조인
    - 장점: 테이블 크기에 제한 없음, 대용량 조인에 적합
    - 단점: Shuffle I/O 비용 큼, Skew 발생 위험 큼 (키가 한쪽에 몰리면 특정 Task에 병목)


##### 5 - 2. 데이터 스큐가 생기는 원인과 해결책? (Salting, Skew Join 등 실무 경험 녹여서)

- Data Skew
    - 특정 키가 너무 많아서 몇몇 Task만 엄청 느려지는 현상
    - 대부분 Task는 몇 초 만에 끝났는데, 특정 Task 하나만 몇 분~몇 시간 걸리는 케이스 → Job 전체가 늦어짐

- 원인
    - 불균형한 키 분포
        - 예: groupByKey() 했는데 "null" 키가 전체의 70%인 경우
    - Hot Key 존재: 특정 제품, 유저, 시간대에 데이터 몰림
        - 예: user_id = 'admin' 같은 특이 케이스
    - Join 시 공통 키가 집중
        - 예: "대한민국"이 모든 행에 있음 → "대한민국" 파티션만 폭발

- 데이터 스큐 해결 전략

1. Salting 기법 (핫 키 분산): Hot Key에 랜덤 prefix 붙여서 분산
    - user_id = "admin" → "admin_1", "admin_2", ..., "admin_n"
    - Join Key를 인위적으로 확장해서 분산 처리 유도하는 방법.

- 예시 (PySpark)

```python
from pyspark.sql.functions import col, concat_ws, lit, rand

# 1. 큰 테이블에 salt 붙이기
df_large_salted = df_large.withColumn("salt", (rand() * 5).cast("int"))
df_large_salted = df_large_salted.withColumn("join_key_salted", concat_ws("_", col("join_key"), col("salt")))

# 2. 작은 테이블에 salt 확장
from pyspark.sql.functions import explode, array

df_small_salted = df_small.withColumn("salt", explode(array([lit(i) for i in range(5)])))
df_small_salted = df_small_salted.withColumn("join_key_salted", concat_ws("_", col("join_key"), col("salt")))

# 3. 조인
df_result = df_large_salted.join(df_small_salted, on="join_key_salted", how="inner")
```


2. Skew Join 전략

- Spark 3.x부터 지원하는 Skew Join Detection + 자동 처리 (AQE) => Spark가 자동으로 skew 파티션을 쪼개서 분산 처리함.

```bash
spark.sql.adaptive.enabled=true
spark.sql.adaptive.skewJoin.enabled=true
```

3. Selective Filtering + Join 순서 변경

- 큰 테이블 필터 먼저 해서 줄인 다음에 Join 수행

- Join 순서를 바꿔서 Hot Key 집중을 피함



##### 5 - 3. Skew가 심각한 Task의 리소스는 어떻게 잡아야 하나? (Executor Memory, Task 병렬도 등)

1. Executor Memory 증가

```bash
spark.executor.memory=8g
spark.executor.memoryOverhead=1g
```

- Skew Task는 엄청난 중간 데이터 생성 가능 => 메모리가 넉넉하지 않으면 OOM + Spill 발생

2. Task 병렬도 조정

- Skew 파티션을 쪼갤 수 있도록 `spark.sql.shuffle.partitions` 값을 늘려줘야 함
    - 기본 200은 보통 데이터에 비해 부족함

```bash
spark.sql.shuffle.partitions=800
```



3. 특정 Key 분리 처리

- "대한민국"처럼 정말 특이한 키가 있다면, 해당 Key만 별도로 처리하고 Union하는 전략도 있음.



### 6. 클러스터와 리소스 관리

##### 6 - 1. YARN, Standalone, Kubernetes 클러스터 매니저의 차이점과 Spark가 Kubernetes 환경에서 가지는 이점

- YARN, Standalone, Kubernetes 클러스터 매니저
    - 공통점: 모두 클러스터 리소스 할당 + Executor 스케줄링 역할 수행
    - Spark Application = Driver + Executor 조합으로 실행됨
    - 차이는 리소스를 누가 어떻게 배분하느냐에서 생김

- YARN (Hadoop Yarn Resource Manager)
    - 탄생 배경: Hadoop 에코 기반에서 사용됨
    - 리소스 관리: YARN이 컨테이너로 리소스를 할당함
    - 인프라 의존: Hadoop 클러스터 필요
    - 장점: 대규모 배치에 강하고 안정성 높음
    - 단점: 설치 복잡하고 Kubernetes보다 유연성 낮음
    - 대부분의 온프레미스 빅데이터 시스템은 아직 YARN 기반 많이 사용함
    - Spark UI 자동 연결, External Shuffle, 동적 리소스 관리 등 지원이 잘 되어 있음

- Standalone Mode
    - 탄생 배경: Spark 기본 내장 클러스터 매니저
    - 리소스 관리: Spark 자체가 리소스 스케줄링
    - 인프라 의존: 거의 없음 (로컬, 간단한 실험에 적합)
    - 장점: 설정 간단, 빠른 테스트 가능
    - 단점: 분산 시스템에선 기능 부족 (HA, 장애 복구 등 미흡)

- Kubernetes
    - 탄생 배경: Cloud Native 환경 대응
    - 리소스 관리: K8s가 Executor/Driver를 Pod로 관리
    - 장점: 컨테이너화된 배포, 동적 확장, GitOps 연계 쉬움
    - 단점: 설정 복잡도 높고, Spark 기능 중 일부는 미지원도 있음 (예: External Shuffle 기본 없음)

- Spark가 Kubernetes 환경에서 가지는 이점
    - 동적 리소스 확장/축소: K8s 오토스케일링 연동 가능 (HPA)
    - ArgoCD + GitOps 연계: GitHub에서 DAG 관리 → 자동 배포 가능
    - 컨테이너 기반 실행: Spark Image 관리 용이 (DockerHub 연동)
    - 복잡한 MSA 환경에 유리: Kafka, Flink, API 서버 등 다양한 컴포넌트 연동 쉬움
    - 멀티 클러스터/멀티테넌시 관리: GKE/EKS 등 퍼블릭 클라우드 인프라와 잘 맞음


##### 6 - 2. Executor 개수와 코어, 메모리 조합을 결정하는 기준은? 실무에서 고려하는 변수는 무엇인가?

- Executor 개수 / 코어 / 메모리 조합 기준

```text
총 Executor 수 = (전체 코어 수) / (Executor당 코어 수)
```

- 실무에서 고려하는 주요 변수들
    - 데이터 크기: 수십 GB → 소형 Executor, 수 TB → 대형 Executor
    - Job 타입: Batch (메모리 중심) / Streaming (지속적 처리)
    - Shuffle 발생 여부: Shuffle이 많으면 Executor 수 늘리기 / 메모리도 넉넉히
    - GC 문제: 코어 수 과하면 GC Pause 시간 길어짐 → 4~5개 이하 권장
    - Task 병렬도: spark.sql.shuffle.partitions와 연동해서 계산
    - Node Spec: 클러스터 노드가 8코어/32GB라면 Executor 2개씩 (코어 4, 메모리 14~15GB) 추천

- 예시 세팅 (GKE 기준)
    - 메모리 오버헤드는 넉넉히 (네트워크 + shuffle buffer 포함되기 때문)
    - 한 노드당 12 Executor, 코어는 35개 선에서 시작해서 튜닝

```bash
spark.executor.instances=8
spark.executor.cores=4
spark.executor.memory=8g
spark.executor.memoryOverhead=1g
```


##### 6 - 3. Dynamic Resource Allocation이 오히려 병목을 만드는 경우는 어떤 케이스인가?

1. Executor 생성/종료에 시간이 오래 걸리는 환경
    - 예: Kubernetes에서 Executor 생성에 10~30초 소요 => 스파크는 Task 대기 중인데 Executor는 아직 생성 중 => 빈틈 많은 리소스 운영 → 성능 저하

2. Shuffle-heavy 작업에서 Executor가 죽으면 Shuffle 파일은 Executor 로컬에 저장
    - Executor가 사라지면 Shuffle 재다운로드 필요 => I/O 폭증 + 성능 저하

- 해결법
    - YARN은 External Shuffle Service로 해결 가능
    - Kubernetes는 기본 지원 ❌ → 직접 설정하거나 피하는 게 안전

3. Streaming / Long-running Job
    - Executor가 계속 늘고 줄면 → State 유지 어려움 + Latency 불안정 → 특히 Kafka, Flink 연동 시 심각

4. Data Skew 상태에서 병목 Task가 죽었다 살아남
    - 특정 키에 Task가 몰려있는데 => Dynamic Allocation이 그 Task가 있는 Executor를 없애버림 → 같은 Skew Task 재시작 → 또 죽음 → 무한 반복

- 대처법
    - Static Executor 할당: spark.dynamicAllocation.enabled=false
    - Initial Executor 넉넉히 확보: spark.dynamicAllocation.initialExecutors=8
    - Skew Join + Salting 조합: Dynamic Allocation + Skew Join은 위험할 수 있음
    - External Shuffle 구성: YARN에서만 안정적 / K8s는 실험적으로 도입해야 함


### 7. 성능 튜닝 및 베스트 프랙티스

##### 7 - 1. Partition 개수는 어떻게 잡아야 최적일까? 데이터 사이즈, CPU, Task 수 기준을 고려해서.

- 기본적으로는 `spark.sql.shuffle.partitions` (기본값: 200)

- 병렬성 = partition 수 = task 수 → CPU 사용량과 밀접히 관련

- 기준 소개
    - Input Data Size: 1개 partition이 100~200MB 정도면 적절. (압축파일 기준은 더 작게)
    - Executor 수 & Core 수: 전체 task 수 = partition 수가 executor × core 수 × 2~3 정도 되면 적당
    - 작업 성격
        - Wide Transformation (e.g. join, groupBy) 많이 쓸수록 파티션 수 조절 중요
        - 파일 개수 많으면 파티션도 그에 맞게 세분화 필요

- 파티션 개수는
    - 너무 적으면 → CPU 놀고 있음
    - 너무 많으면 → Task Scheduling + Shuffle Overhead 증가

```python
df = spark.read.parquet("...").repartition(400)  # 직접 조정 가능
```


##### 7 - 2. Caching과 Persistence는 언제 유효하고, 잘못하면 왜 오히려 성능이 나빠질까?

- Spark는 Lazy Execution이므로, DataFrame을 여러 번 사용할 때마다 매번 다시 계산됨.

- `.cache()`나 `.persist()`를 사용하면, 첫 실행 결과를 메모리/디스크에 저장해서 재계산 방지 가능.


```python
df = spark.read.parquet("...").filter("type = 'click'")
df.cache()  # 이후 이 df를 여러 번 join/filter/etc 할 때 성능 향상
```

- 오히려 성능이 나빠지는 경우 존재
    - 캐싱할 DF가 너무 큼: 메모리 부족 → 디스크 spill 발생 → 느려짐
    - 한 번만 사용: 굳이 cache 필요 없음 → 오히려 불필요한 메모리 할당
    - 자주 업데이트 되는 DF: 캐싱된 내용이 stale → 버그 위험

- 추천: .cache() 사용 후 .count()로 트리거 실행 → 실제 메모리에 올라가는지 확인


##### 7 - 3. Whole-stage Code Generation이란 무엇인가? 성능이 어느 정도 개선되는지, 그리고 예외 케이스는?

- Whole-Stage Code Generation (WSCG)이란: Catalyst 최적화 이후, 물리 실행 계획을 Java 바이트코드로 통째로 생성해주는 기능

- 여러 연산(예: filter + projection + aggregation 등)을 하나의 루프로 병합해서 실행

- 기존엔 Row마다 함수 호출 → WSCG는 루프 내부에 모든 연산을 Inline

- 성능 향상 정도
    - 메소드 호출/객체 생성 비용 절감.
    - CPU 캐시 활용도 올라감.
    - 최대 수십 배 빠름 (특히 많은 Row 처리 시)

- 예외 케이스 (WSCG 비활성화됨)
    - UDF 사용: JVM에서 직접 인라인 못함
    - 복잡한 표현식: 코드가 너무 커져서 JVM의 method size 제한 (64KB) 초과
    - Interpreted Mode 강제: `spark.sql.codegen.wholeStage=false` 설정 시

- 확인 방법
```python
df.explain(True)  # Physical Plan에 WholeStageCodegen 나타나는지 확인
```



### 8. 실시간 스트리밍 (Structured Streaming)

##### 8 - 1. Spark Structured Streaming이 Micro-batch 방식인데, 실시간 시스템이라 부를 수 있는 이유는?

- Micro-batch = 실시간과의 타협점
- Structured Streaming은 내부적으로 짧은 간격의 반복적인 배치 처리 (micro-batch)로 동작
- 즉, 정해진 Trigger 시간마다 새로운 데이터를 Pull + 처리 + Sink에 Write 함.

```text
Trigger: 1초 (default) → 1초 간격으로 데이터를 묶어서 처리
```

- 그럼에도 실시간이라 부르는 이유
    - Latency가 짧기 때문: 트리거 간격이 매우 짧으면, 사용자는 거의 실시간처럼 느낍니다. (1초 또는 수백 ms 단위 가능)
    - Continuous 처리 모델과 유사하게 동작: 내부적으로는 배치지만, 사용자는 streaming query abstraction을 쓰기 때문에 이벤트 기반처럼 다룰 수 있음
    - Windowing / Aggregation / Join 등 스트리밍 특화 기능 제공: 시간 기반 연산도 배치가 아니라 streaming semantic으로 해석됨

- 정리: Spark는 Streaming의 API 철학을 유지하면서, Batch 엔진의 안정성을 같이 취하는 구조
    - Flume/Storm 대비 높은 신뢰성과 유지보수 편리함이 장점


##### 8 - 2. Watermark는 왜 필요한가? Late Data 처리와 관련해서 실무에 적용하려면 뭘 고려해야 하나?


- Watermark는 "이 시점 이후엔 더 이상 늦은 데이터가 오지 않을 거라고 가정"하는 기준 시간입니다.

- 이벤트 타임 기반 스트리밍 처리에서, 늦게 도착한 데이터(=Late Data)가 있을 수 있음

- 하지만 무한정 기다릴 순 없으므로, 어느 시점에서 늦은 데이터 무시 또는 별도로 처리해야 함

```python
df.withWatermark("eventTime", "10 minutes")  # 10분보다 늦게 들어온 데이터는 무시
```

- 적용 시 고려사항
    - 데이터 도착 지연 패턴 분석: 얼마나 늦게 들어오는 데이터가 있는지 실측 필요
    - 유저 행동 데이터/센서 로그 등: 모바일/IoT 환경에서는 지연이 흔하므로 Watermark 꼭 써야 함
    - Join/Window 연산 시 필수: Watermark 없으면 상태정보가 계속 메모리에 쌓임 → OOM 위험
    - 필드 기준: eventTime 필드는 정확히 파싱되고 timestamp type이어야 함
    - 복합 처리: late data는 별도 sink로 분기하거나, 보정 처리 루틴 추가 가능

- watermark 설정이 너무 짧으면 유실되고, 너무 길면 리소스 낭비 => 적절한 타협 필요.



##### 8 - 3. Exactly-once를 Spark Structured Streaming이 보장할 수 있는 구조적 근거는?

- Structured Streaming의 "exactly-once"는 Sink 기준의 보장
    - 즉, 결과가 중복되지 않고 한 번만 기록되는지를 보장하는 것.

- 구조적 메커니즘

1. Checkpointing: 
    - Streaming Query의 상태와 Offset을 주기적으로 저장
    - 장애 발생 시, checkpoint 기준으로 정확히 복원 가능

```python
writeStream.option("checkpointLocation", "/path/to/checkpoint")
```

2. Write-Ahead Logging (WAL)
    - 처리 전 Offset과 연산 결과를 저장해놓고, 성공 시에만 Commit
    - 따라서 중복 실행이 일어나도 중복 기록은 방지됨

3. Idempotent Sink or Transactional Sink
    - Sink가 "한 번만 쓰기"를 보장할 수 있어야 진짜 Exactly-once가 성립됨
    - Sink 유형, Exactly-once 가능 여부 정리
        - File Sink (Parquet, Delta): 기본 제공
        - Kafka Sink: 필요 조건 있음 (transactional Kafka + idempotent producer)
        - Foreach Sink: X. 직접 처리하면 보장 어려움 (직접 구현 필요)

- Kafka Sink에서 Exactly-once를 쓰려면: Kafka 0.11 이상 + enable.idempotence=true + acks=all + transactional.id
    - Structured Streaming에서는 내부적으로 이 옵션을 설정할 수 있도록 설계되어 있음 (kafka.sink.* 설정)


### 9. Spark와 빅데이터 에코시스템 연계

##### 9 - 1. Spark가 Hadoop HDFS와 어떻게 통신하고 데이터를 읽는가? (InputFormat, Block Reading)

- 기본 개념: Spark는 Hadoop InputFormat API를 통해 HDFS와 통신함.

- HDFS 저장 구조
    - 파일이 여러 Block (보통 128MB or 256MB) 단위로 나뉘고
    - 각 Block은 여러 DataNode에 분산 저장됨

- Spark 동작 흐름
    1. NameNode에 메타데이터 질의 => Block 위치 확인
    2. 각 Executor가 해당 Block의 DataNode로부터 데이터를 Pull
    3. InputFormat, RecordReader를 사용해 데이터를 Row 단위로 파싱

- 주요 포인트
    - Data Locality: Spark는 Block이 있는 곳에 Executor를 배치하려고 시도함 (Data Local Scheduling)
    - InputFormat: TextInputFormat, ParquetInputFormat 등, Hadoop의 읽기 규칙을 따름
    - Splitable File: Gzip처럼 Split 안 되는 파일은 → 1 Executor만 사용 → 성능 하락
    - Spark는 HDFS뿐 아니라 S3, GCS, Azure Blob 등도 Hadoop FileSystem 인터페이스를 통해 동일하게 접근함 (s3a://, gs:// 등)


##### 9 - 2. Kafka Consumer로서 Spark Streaming과 Structured Streaming의 차이점은?

- 핵심 차이: API 철학, 추상화 수준, 안정성

- Spark Streaming (DStreams)
    - API: RDD 기반
    - 추상화 수준: Low-level
    - Kafka 통합: 수동 오프셋 관리 필요
    - Exactly-once: 직접 구현 필요
    - 복잡한 연산: 직접 연산 처리 (복잡함)
    - 성능/유지보수	구버전, deprecated 예정

- Structured Streaming
    - API: DataFrame 기반
    - 추상화 수준: High-level SQL + streaming abstraction
    - Kafka 통합: 자동 관리 (KafkaSource 내장)
    - Exactly-once: 기본 제공 (with checkpoint)
    - 복잡한 연산: Windowing, Join, Watermark 모두 지원
    - 성능/유지보수: 최신 Spark 주력 기능

- 선택 기준
    - 새 프로젝트 or 확장성 고려: → Structured Streaming 강력 추천
    - 기존 레거시 유지보수: DStream 일부 사용 가능성 존재

- Structured Streaming은 Kafka의 consumer group 개념 그대로 따르고, `maxOffsetsPerTrigger` 등으로 batch 단위 메시지 양 조절도 가능


##### 9 - 3. Spark와 Delta Lake, Iceberg 같은 레이크하우스 솔루션이 결합될 때 어떤 이점이 있나?

- 레이크하우스: 데이터 웨어하우스의 ACID/Schema 관리 기능 + 데이터 레이크의 대용량 유연성을 결합한 모델
    - 대표 엔진: Delta Lake, Apache Iceberg, Apache Hudi

- Spark와 함께 쓸 때 장점
    - ACID 트랜잭션: 여러 Spark job이 동시에 read/write 해도 consistency 유지 (로그 기반 atomic write)
    - Time Travel: 이전 버전 데이터 조회 가능 → 분석 reproducibility 보장
    - Schema Evolution: 컬럼 추가/삭제 시에도 유연하게 처리 가능
    - Streaming + Batch 통합: 실시간 ingest + 배치 분석을 하나의 테이블에서 처리
    - Compaction / Vacuum: 파일 수 많아질 때 자동 병합, 정리 (Delta, Iceberg 모두 지원)

- Delta Lake 예시

```python
# Append data with ACID guarantees
df.write.format("delta").mode("append").save("/delta/events")

# Stream write도 가능
df.writeStream.format("delta")...
```

- Iceberg는 Presto, Trino, Flink와도 잘 통합됨 → Spark만의 전유물이 아님
    - 반면 Delta Lake는 Spark 중심 개발이라 Spark 유저에게 특히 유리



### 10. 케이스 스터디 및 트러블슈팅

##### 10 - 1. Out of Memory(OOM) 오류가 발생했을 때, 어디서부터 어떻게 진단할 것인가?


- 진단 순서
    1. 로그 확인: Container killed by YARN for exceeding memory limits or GC overhead limit exceeded 메시지
    2. 어떤 메모리인가 확인: Executor Memory / Driver Memory / JVM Heap / Off-Heap / Shuffle
    3. 어떤 연산인지 확인: join, groupByKey, collect 등 wide + shuffling + large data
    4. Data Skew 확인: 특정 task가 지나치게 많은 데이터를 처리 중인지.

- 대응 전략
    - Executor 메모리 부족: `spark.executor.memory` / `spark.executor.memoryOverhead` 값 증가
    - Driver OOM: `collect()` 대신 `.write()` 등 lazy 방식 사용
    - Shuffle spill: `spark.sql.shuffle.partitions` 감소시키기 또는 Spark 3.x 이상 AQE 활용
    - GC Overhead: `spark.executor.extraJavaOptions` 로 GC 옵션 조정 (G1GC 등 다른 GC 알고리즘 사용)
    - Skew로 인한 쏠림: Salting, Skew Join 전략 도입

```bash
spark-submit \
  --conf spark.executor.memory=4g \
  --conf spark.executor.memoryOverhead=1g \
  --conf spark.executor.extraJavaOptions="-XX:+UseG1GC"
```


##### 10 - 2. 스테이지가 특정 Task에서 멈춰있을 때, 원인 분석과 대응 방안은?

- 주 원인
    - 특정 Task가 오래 걸림: Data Skew (특정 키에만 데이터 집중)
    - Task Retry 반복: Task 실패 후 재시도 중 (로그에 Retrying task 메시지 확인)
    - 외부 I/O 지연: S3/HDFS/network 이슈, UDF 내부 DB/API call 등
    - UDF, UDAF 예외: 내부 함수에서 무한 루프, 예외 발생 시 log 없이 멈춘 듯 보이기도 함

- 분석 방법
    - Spark UI > Stages > Task 시간 분포 확인
    - 로그 분석: 해당 Task 로그만 따로 보기
    - Spark History Server, Ganglia, CloudWatch 등 모니터링 도구도 활용

- 해결 방안
    - Skew: Salting, custom partitioner, broadcast join 활용
    - 외부 API: 시간 제한 / 타임아웃 설정, 비동기 처리 고려
    - 불균형 Partition: df.repartition() or coalesce()로 조정
    - 병렬성 부족: Executor/Core 수 증가 + 적절한 partition tuning


##### 10 - 3. 스팟 인스턴스 기반 클러스터에서 Spark 잡이 안정적으로 실행되게 하려면?


- 스팟 인스턴스란
    - AWS, GCP 등에서 제공하는 저가형 일시적 인스턴스
    - 언제든지 회수될 수 있는 리스크 존재

- 문제 상황
    - Executor 회수됨: 작업 중이던 Spark Task가 중단됨 → Stage Retry or 전체 Job 실패 가능
    - Skewed 작업: 특정 Executor에만 Task 몰릴 경우, 해당 인스턴스 회수 시 대미지 큼

- 안정화 전략
    - 혼합 클러스터 구성: On-Demand + Spot 조합 (예: 70% Spot, 30% On-Demand)
    - Speculative Execution 활성화: 느린 Task 자동 대체 → spark.speculation=true
    - checkpoint + job 재시도 전략: streaming이면 checkpoint 필수, batch도 실패 감지 후 자동 재시도 설계
    - Kubernetes에선 NodeSelector/Tolerations으로 온디맨드 유지 영역 확보
    - 데이터 저장 시점 분리: Long-running job이면 중간 결과 저장 필요 (delta, parquet 등으로 커밋)

