## Network

### **1. OSI & TCP/IP Models in Data Engineering**

- How does the OSI model apply when a distributed ETL job fetches data from a remote PostgreSQL database? Which layers are involved?
    - **Application Layer (Layer 7):** The ETL tool communicates with PostgreSQL using the PostgreSQL protocol over TCP/IP.
    - **Transport Layer (Layer 4):** TCP ensures reliable data transmission between the ETL job and PostgreSQL.
    - **Network Layer (Layer 3):** IP handles routing the packets across networks.
    - **Data Link & Physical Layers (Layers 2 & 1):** Ethernet, Wi-Fi, or other physical connections transmit the data packets.
- When designing a data pipeline that ingests data from an SFTP server into a data warehouse, which protocols and OSI layers are most relevant?
    - **Application Layer (Layer 7):** SFTP protocol is used for secure file transfers.
    - **Transport Layer (Layer 4):** TCP ensures ordered and reliable delivery.
    - **Network Layer (Layer 3):** IP routes packets across networks.
    - **Data Link Layer (Layer 2):** Ethernet/Wi-Fi manages physical addressing.
- You are designing a distributed ETL pipeline that transfers large volumes of data between multiple data centers. Given the OSI and TCP/IP models, how would you **optimize** data transmission to minimize packet loss and latency?
    - Use **compression** to reduce payload size.
        - **Application-level compression**: Compressing files (e.g., using Parquet or ORC format in Spark).
        - **Network-level compression**: TCP can apply compression (e.g., TLS compression in HTTPS).
        - **Protocol-specific compression**: Kafka’s Snappy compression, gRPC’s built-in Protobuf compression.
    - Optimize **TCP window scaling** for better throughput.
        
        TCP **window scaling** is a feature that allows TCP to handle high-speed and high-latency networks efficiently by increasing the size of the receive window beyond the default 65,535 bytes.
        
        - The **receive window** determines how much data a receiver can accept before sending an acknowledgment (ACK).
        - In high-latency networks (e.g., cross-data-center transfers), a small window can **bottleneck throughput**.
        - Window scaling uses a multiplier to expand the window size up to **1GB**, allowing more data to be in transit before waiting for ACKs.
    - Implement **Load Balancing & CDNs** to distribute traffic efficiently.
        - Round-robin, Least connections, etc… for kafka → kafka distributes partitions automatically
        
        A **CDN** is useful if your ETL pipeline **serves large datasets** (e.g., pre-aggregated analytics).
        
        **Example 1: Cloudflare or AWS CloudFront for Cached Data**
        
        If your ETL pipeline serves pre-processed reports, store them in **S3 + CloudFront** to reduce load on the origin server:
        
        - ETL job stores results in **S3**.
        - **CloudFront caches the data**, reducing data transfer costs.
        - Users in different regions **fetch from the nearest edge server**.
        
        **Example 2: Kafka MirrorMaker for Cross-Region Replication**
        
        - If you have a **Kafka cluster in two data centers**, use **Kafka MirrorMaker** to replicate topics across regions.
        - Clients **consume from the nearest cluster** to reduce latency.
    - Use **parallelism & partitioning** to divide data into manageable chunks.
- In a real-time data ingestion system, when would you prefer TCP over UDP? How would factors like reliability, ordering, and speed impact your choice in a data engineering pipeline?
    - **TCP:** Preferred when reliability and ordering are critical (e.g., financial transactions).
    - **UDP:** Used for real-time, high-frequency ingestion where latency is a concern (e.g., stock market ticker updates).

### **2. Network Packets & Headers in Data Transmission**

- When transmitting large dataset chunks over an API, how does TCP packet fragmentation impact performance? How would you optimize data transmission?
    - Large payloads are split into multiple TCP packets.
    - Use **MTU tuning** and **chunked transfer encoding** to optimize performance.
    - Enable **keep-alive and persistent connections** to minimize re-transmissions.
- If your data ingestion pipeline frequently encounters corrupted JSON payloads from a remote Kafka producer, which network-level headers would you inspect to debug the issue?
    - Inspect **IP headers** for fragmentation.
    - Check **TCP checksums** for data integrity.
    - Analyze **Kafka message headers** for encoding issues.
- A real-time data streaming job is experiencing unexpected packet drops and inconsistencies in received messages. How would you use networking tools (e.g., Wireshark, TCPDump) to diagnose the issue at different OSI layers?
    - Use **Wireshark/TCPDump** to inspect TCP retransmissions and dropped packets.
    - Monitor **network congestion and buffer overflows**..
    - Adjust **socket buffer sizes**.

### **3. Network Bottlenecks in ETL Pipelines**

- Your ETL jobs running on a cloud-based data lake are significantly slower than expected. What networking factors (e.g., MTU size, TCP window scaling, congestion control) could contribute to this, and how would you troubleshoot them?
    - **MTU size mismatches** leading to fragmentation.
    - **TCP congestion control** reducing throughput.
    - **Network latency & bandwidth limitations**.
    - **Use of CDN & edge computing** to offload traffic.

### **4. Encapsulation & Decapsulation in Data Movement**

- How does encapsulation/decapsulation work when transferring large datasets via Apache Kafka over a network? Which headers are involved?
    - Kafka messages are wrapped in protocol headers.
    - Each message passes through **TCP/IP, Ethernet headers** before transmission.
- In a Spark job that reads from an S3 bucket, how do network layers handle chunking, transfer, and reassembly?
    - **HTTP layer:** Manages requests.
    - **Transport layer:** Ensures reliable data streaming.
    - **Data Link & Physical layers:** Handle data movement.
- When moving data between microservices in a Kubernetes cluster, explain how encapsulation and decapsulation happen at different OSI layers. How does this impact latency and throughput?
    - Use **HTTP/gRPC over TCP** for inter-service communication.
    - **Service mesh (Istio/Linkerd)** handles encapsulation and load balancing.

### **5. Network Topology & Data Pipelines**

- Your company has multiple data centers, and you need to design a pipeline that replicates data efficiently between them. What network topologies would you consider, and how would they affect data consistency?
    - **Star topology:** Centralized but prone to bottlenecks.
    - **Mesh topology:** Higher fault tolerance.
    - **Hybrid topology:** Balances efficiency and redundancy.
- In a distributed environment where data processing happens across multiple nodes, how does network topology impact data shuffling and partitioning?
    - **Closely connected nodes reduce shuffle costs.**
    - **Load-aware partitioning improves throughput.**

### **6. Ethernet & Packet Transmission in Data Engineering**

- If you're streaming IoT sensor data into a warehouse, how would Ethernet MTU (Maximum Transmission Unit) affect performance? What strategies would you use to prevent fragmentation?
    - Large MTU reduces overhead but may cause fragmentation.
    - Use **Jumbo Frames** for high-throughput networks.
- How do VLANs and subnets impact data access control when deploying a data warehouse across multiple availability zones?
    - **VLAN segmentation** restricts access based on departments.
    - **Subnets enforce access control policies.**
- Your on-premise data warehouse connects to a Spark cluster for analytics. Would you recommend using Ethernet or Wi-Fi for high-throughput data transfers? Explain your reasoning in terms of latency, collision domains, and reliability.
    - **Ethernet:** Preferred for stability, low latency.
    - **Wi-Fi:** Higher packet loss, less reliable for high-throughput.

### **7. Protocols & Data Engineering**

- Your data ingestion pipeline relies on RESTful APIs and sometimes experiences slow responses. How would switching from HTTP/1.1 to HTTP/2 or gRPC impact performance?
    - HTTP/2 enables **multiplexing**, reducing latency.
    - gRPC uses **protobufs**, lowering payload size.
- Why might you choose UDP over TCP for high-frequency real-time data ingestion, such as stock market ticker updates?
    - UDP preferred for low-latency, real-time updates.
    - TCP used when data integrity matters.

### **8. Cast Methods & Load Balancing in Data Engineering**

- When streaming data to multiple downstream consumers, when would you use unicast, multicast, or broadcast?
    - **Unicast:** One-to-one communication (e.g., client-server queries).
    - **Multicast:** One-to-many (e.g., real-time analytics).
    - **Broadcast:** Used in small, contained networks.
- How would you implement load balancing for an Apache Kafka consumer group in a cloud-based deployment?
    - **Partitioned consumption** to distribute load.
    - **Sticky consumers** to ensure ordered processing.

### **9. HTTP vs. gRPC for Data API Endpoints**

- Your team is developing a data ingestion API. When would you use HTTP/REST vs. gRPC over TCP, considering performance, payload size, and protocol overhead
    - REST: More compatible, but slower.
    - gRPC: Faster with lower overhead, ideal for microservices.

### **10. Handling Network Failures in Data Pipelines:**

- A batch job extracts data from a remote API every hour, but network failures sometimes cause incomplete datasets. What strategies (e.g., retries, exponential backoff, idempotency) would you use to handle these failures gracefully?
    - Implement **retries with exponential backoff**.
    - Ensure **idempotency** for safe reprocessing.

### **11. Load Balancers & Data Engineering APIs:**

- You have a high-traffic API serving data to multiple clients. How does a load balancer improve network performance, and what considerations should you make when handling sticky sessions vs. stateless requests?
    - Use **round-robin, least connections** for stateless requests.
    - Use **sticky sessions** for stateful transactions.

### **12. Edge Computing & Data Engineering:**

- In an IoT data pipeline, sensor devices send data packets to a cloud-based data warehouse. How does edge computing reduce network congestion, and what protocols (e.g., MQTT, WebSockets) would you consider for efficient data transfer?
    - **Process data closer to the source**.
    - **Use MQTT/WebSockets** for real-time updates.

### **13. Network Topologies & Data Flow Optimization:**

- Your company is setting up a multi-region data pipeline for processing customer transactions. How does network topology (e.g., mesh vs. star vs. hybrid) impact the efficiency and fault tolerance of your data architecture?
    - **Mesh topology for resilience**.
    - **Star topology for centralized control**.

### **14. CDN & Data Warehousing Performance:**

- Your data engineering team needs to serve pre-aggregated analytics data to global users. How can a Content Delivery Network (CDN) help reduce network latency, and what caching mechanisms would you implement?
    - Cache pre-aggregated data.
    - Use **regional edge servers** for faster access.

---

## Study Week 1

### 1-1 사용자가 API에 요청을 해서 응답을 받기까지의 과정을 데이터 계층 모델로 묘사해보시유?

🔎 **1. 응용 계층 (Application Layer - HTTP / REST API / JSON)**

- **무슨 일이 일어나나요?**
    
    클라이언트(브라우저, Postman, curl 등)가 HTTP 요청을 생성합니다.
    
    예시:
    
    `GET /api/data HTTP/1.1`
    
- 헤더, 인증 토큰 등이 포함됩니다.
- **전송할 데이터 형식:** JSON (`Content-Type: application/json`)
- **역할:** 사용자 데이터(요청)를 전송하고 응답을 받는 최상위 계층

➡️ 작성된 요청은 아래 전송 계층으로 전달됩니다.

---

🔎 **2. 전송 계층 (Transport Layer - TCP)**

- **무슨 일이 일어나나요?**
    - HTTP 요청을 **TCP 세그먼트**로 나누고, 신뢰성 있게 전송
    - 연결 과정: **3-way 핸드셰이크 (SYN → SYN-ACK → ACK)**
    - 순서 보장, 패킷 재전송 처리
- **포트 번호:** 서버는 보통 **80(HTTP)** 또는 **443(HTTPS)** 포트로 대기
- **역할:** 데이터가 빠짐없이 순서대로 도착하도록 보장

---

🔎 **3. 네트워크 계층 (Network Layer - IP)**

- **무슨 일이 일어나나요?**
    - TCP 세그먼트를 **IP 패킷**으로 감싸고,
    - **출발지 IP**(내 컴퓨터), **목적지 IP**(API 서버) 부여
- **라우팅:** 여러 라우터를 거쳐 목적지로 이동 (경로 결정)
- **주의:** 패킷 크기 초과 시 분할 (Fragmentation), TTL 감소

---

🔎 **4. 데이터 링크 계층 (Data Link Layer - 이더넷 / Wi-Fi / 5G)**

- **무슨 일이 일어나나요?**
    - IP 패킷을 **프레임(Frame)**으로 감싸 전송 준비
        - 유선이면 Ethernet Frame
        - 무선이면 Wi-Fi Frame
        - 모바일이면 5G/LTE 프레임
    - **MAC 주소**를 사용해 같은 네트워크 내 장치로 전달
    - **ARP 프로토콜:** IP를 MAC 주소로 변환해줌

---

🔎 **5. 물리 계층 (Physical Layer - 전선 / 광섬유 / 무선 신호)**

- **무슨 일이 일어나나요?**
    - 0과 1로 이루어진 비트가 **전기 신호 / 빛 신호 / 전파**로 변환되어 전송
    - 예시:
        - 랜선 → 전기 신호
        - 광케이블 → 빛 신호
        - Wi-Fi / 5G → 무선 전파
- **역할:** 실제 데이터를 물리적으로 이동시키는 구간

---

🔄 **서버 응답 과정도 동일하게 반대 방향으로 진행**

- 서버가 요청을 받아 처리하고 **JSON 데이터를 포함한 HTTP 응답**을 생성
- 응답 데이터가 다시 **물리 계층 → 데이터 링크 → 네트워크 → 전송 → 응용 계층** 순으로 올라오고
- 최종적으로 클라이언트가 **JSON 데이터 파싱 및 처리**

### 1-2. 대용량 데이터를 수집힐 때, 전송, 네트워크 계층에서 어떤 문제가 발생할 수 있을까요?

**Transport Layer Problems & Solutions**

The **transport layer (Layer 4)** is responsible for end-to-end communication, error recovery, and congestion control.

**1. High Latency & Packet Loss**

- **Problem:** Large data transfers may experience significant delays due to congestion, leading to dropped packets and retransmissions.
- **Solutions:**
    - Use **Multipath TCP (MPTCP)** to split traffic across multiple network paths.
    - Implement **QUIC (Quick UDP Internet Connections)** for faster, low-latency data transfer.
    - Use **optimized congestion control algorithms** (e.g., BBR instead of Reno/Cubic).

**2. TCP Throughput Bottlenecks**

- **Problem:** TCP's congestion control can throttle throughput when handling large data streams.
- **Solutions:**
    - Use **UDP-based transport** (e.g., QUIC, RDMA over Converged Ethernet). TCP에서 병목이 발생한다고 UDP로 바꿔버리는게 해결책 ?! … ← ㅁㄴㅇㄻㄴㅇㄻㄴㅇㄻㄴㅇㄹ
    - Optimize TCP window scaling and buffer sizes.
    - Deploy **parallel TCP streams** to maximize bandwidth.

**3. Inefficient Data Serialization**

- **Problem:** Poorly formatted or excessive serialization (e.g., JSON) can slow down transport efficiency.
- **Solutions:**
    - Use **binary formats** like **Apache Avro, Protocol Buffers, or FlatBuffers**. → protobuff 쓴다는건 RPC?
    - Compress data before transport (e.g., **Snappy, LZ4**).

**4. Fault Tolerance & Data Integrity**

- **Problem:** Data corruption or partial failures during transfer.
- **Solutions:**
    - Use **checksum-based verification** (e.g., TCP checksum, CRC).
    - Implement **retry and deduplication mechanisms** in applications.

---

**Network Layer Problems & Solutions**

The **network layer (Layer 3)** handles packet forwarding, routing, and addressing.

**1. Bandwidth Constraints**

- **Problem:** Limited bandwidth slows down big data transfers.
- **Solutions:**
    - Use **Data Compression** before sending data.
    - Optimize **routing and load balancing** across multiple paths.
    - Deploy **Content Delivery Networks (CDNs)** to distribute traffic efficiently.

**2. Network Congestion & Packet Reordering**

- **Problem:** Large-scale data transfers can congest networks, causing packet delays or reordering.
- **Solutions:**
    - Use **Quality of Service (QoS) policies** to prioritize critical data.
    - Enable **Explicit Congestion Notification (ECN)** in TCP/IP stacks.
    - Use **Software-Defined Networking (SDN)** to optimize routing dynamically.

**3. IP Fragmentation Issues**

- **Problem:** Large data packets may be fragmented, causing reassembly issues.
- **Solutions:**
    - Adjust **MTU (Maximum Transmission Unit)** sizes to avoid fragmentation.
    - Use **Jumbo Frames** (9,000 bytes) in high-performance networks.

**4. Routing Inefficiencies & Failures**

- **Problem:** Poor routing decisions or failures increase latency.
- **Solutions:**
    - Implement **BGP optimizations** for inter-data-center transfers.
    - Use **Anycast routing** to reduce data travel distances.

---

### 1-3. 패킷 로스를 방지하기 위해서 ? (1-2랑 같은듯)

- 요청 청킹

✅ **1. 압축(Compression)으로 페이로드 크기 감소**

- **애플리케이션 레벨 압축**: 데이터 파일을 압축된 포맷으로 저장 (예: Spark에서 Parquet 또는 ORC 포맷 사용)
- **네트워크 레벨 압축**: TCP 전송 시 압축 적용 가능 (예: HTTPS에서 TLS 압축)
- **프로토콜 별 압축**: Kafka의 Snappy 압축, gRPC의 Protobuf 내장 압축 등

---

✅ **2. TCP 윈도우 스케일링(Window Scaling) 최적화**

- TCP **윈도우 스케일링**은 고속 및 고지연 네트워크 환경에서 수신 윈도우 크기를 기본값(65,535 바이트)보다 크게 확장해 전송 효율을 높이는 기능입니다.
- *수신 윈도우(Receive Window)**란, 수신 측에서 ACK 없이 한 번에 수신 가능한 데이터의 양을 의미합니다.
- 데이터 센터 간 전송처럼 지연이 큰 네트워크에서는 윈도우 크기가 작으면 **처리량(Throughput) 병목**이 발생할 수 있습니다.
- TCP 윈도우 스케일링을 적용하면 **최대 1GB까지 윈도우 확장**이 가능해져 ACK를 기다리지 않고 더 많은 데이터를 전송할 수 있습니다.

---

✅ **3. 로드 밸런싱 및 CDN 활용으로 트래픽 분산**

- Kafka는 파티션을 통해 기본적으로 분산 처리하지만, 추가적으로 **라운드 로빈(Round Robin), 최소 연결(Least Connections)** 등의 전략을 고려할 수 있습니다.
- *CDN(Content Delivery Network)**은 대규모 데이터셋(예: 사전 집계된 분석 결과)을 제공하는 ETL 파이프라인에서 유용합니다.

📌 **예시 1: Cloudflare 또는 AWS CloudFront 활용 (캐시 데이터 제공)**

- ETL 작업이 생성한 결과물을 **S3**에 저장하고, **CloudFront**로 캐싱하여 원본 서버의 부하를 줄일 수 있습니다.
- CloudFront가 데이터를 캐싱하므로 데이터 전송 비용 절감 및 사용자별 **가장 가까운 엣지 서버에서 데이터 제공**이 가능합니다.

📌 **예시 2: Kafka MirrorMaker를 통한 데이터 센터 간 복제**

- 두 개 이상의 데이터 센터에 Kafka 클러스터가 있는 경우, **Kafka MirrorMaker**를 사용해 토픽을 지역 간 복제할 수 있습니다.
- 클라이언트는 **가장 가까운 클러스터에서 소비(Consume)** 하여 지연을 줄일 수 있습니다.

---

✅ **4. 병렬 처리(Parallelism) 및 파티셔닝(Partitioning) 활용**

- 데이터를 적절한 크기의 조각으로 나누어 병렬로 처리함으로써 대용량 전송을 효율화할 수 있습니다.

---

### 2-1**. 리버스 프록시(Reverse Proxy)는 무엇인가요? 일반 프록시와 어떤 차이가 있나요?**

**A.**

리버스 프록시는 클라이언트가 아닌 서버 측에 위치하는 프록시입니다. 클라이언트는 리버스 프록시를 통해서만 서버에 접근하고, 리버스 프록시가 여러 서버 중 적절한 서버로 요청을 전달합니다.

일반 프록시는 클라이언트가 목적지 서버에 접근하는 것을 대신하는 반면, 리버스 프록시는 서버가 클라이언트의 요청을 직접 받지 않고 리버스 프록시가 대신 받아 처리한다는 점이 가장 큰 차이입니다.

리버스 프록시는 주로 **로드 밸런싱, SSL 종료, 보안 강화, 캐싱** 등의 목적으로 사용됩니다.

### 2-2 **프록시나 리버스 프록시가 데이터 엔지니어링 환경에서 어떻게 사용될 수 있을까요?**

**A.**

데이터 엔지니어링 환경에서는 API 서버 앞단에 리버스 프록시를 두어 다음과 같은 용도로 사용할 수 있습니다:

- 데이터 수집 API의 부하 분산 (로드 밸런싱)
- 인증 및 접근 제어 강화
- 외부 API 호출 시 프록시 서버를 이용해 IP 우회 및 요청 로그 기록
- 캐싱을 통해 중복된 데이터 요청 방지 및 성능 최적화

예를 들어, Nginx나 Envoy 같은 리버스 프록시를 배치해 외부에서 들어오는 데이터 스트림을 분산 처리하고, 내부 데이터 파이프라인으로 전달할 수 있습니다.

### 2-3 **ETL 파이프라인에서 리버스 프록시를 사용하는 사례를 설명해보세요.**

**A.**

ETL 파이프라인에서 리버스 프록시는 주로 **데이터 수집(Extract) 단계**에서 사용됩니다.

예를 들어, 외부 파트너사나 IoT 기기에서 API를 통해 데이터가 들어오는 구조라면, 리버스 프록시(Nginx, Envoy 등)를 앞단에 두어:

- **트래픽 부하 분산**
- **SSL 처리 및 인증 수행**
- **요청 데이터 유효성 검사**
- **임시 캐싱 후 Batch성 처리**

같은 작업을 수행할 수 있습니다. 이렇게 하면 데이터 수집 서버의 부하를 줄이고, 데이터 유입 지점을 일원화해 관리와 모니터링이 쉬워집니다.

### 2-4 **데이터 엔지니어링에서 리버스 프록시를 이용해 트래픽을 어떻게 효율적으로 관리할 수 있을까요?**

**A.**

데이터 파이프라인의 API 수집 구간에 리버스 프록시를 두면:

- **Rate Limiting(속도 제한)** 기능으로 특정 클라이언트의 과도한 요청을 제어할 수 있습니다.
- **캐싱**을 통해 동일한 요청이 반복되는 경우, 백엔드 API 서버로의 호출을 줄여 효율적으로 트래픽을 관리할 수 있습니다.
- **로드 밸런싱** 기능으로 데이터를 수집하는 API 서버들의 부하를 분산시켜 시스템 안정성을 확보할 수 있습니다.

예를 들어, 대용량의 IoT 데이터가 실시간으로 들어오는 환경에서 이런 구조를 적용하면 파이프라인 장애를 예방할 수 있습니다.

### 2-5 트래픽 분산은 백엔드 관점과 하드웨어 관점에서 어떻게 할 수 있을까요?

1. 하드웨어: 리눅스의 경우 NIC