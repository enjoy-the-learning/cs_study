
# 3. OS

- 운영 체제는 프로그램 간의 올바른 실행을 돕고 다양한 하드웨어의 자원을 프로그램에 배분하는 '프로그램'

- 하드웨어를 동작시키는 프로그램, 컴퓨터 전체에서 가장 중요한 프로그램이라고 할 수 있음.

- 실행, 개발할 프로그램을 알기 위해서는 운영체제에 대한 이해가 필수임.


### 1. 운영 체제의 큰 그림

- 윈도우, 맥OS, iOS, 안드로이드 등. 운영 체제에는 다양한 종류가 있으나 핵심 기능은 비슷함. (크게 아래의 두가지)
    - 자원 할당 및 관리
    - 프로세스 및 스레드 관리

- OS의 핵심적인 기능을 담당하는 부분을 Kernel 이라고 함. (이 책에서는 일반적으로 커널을 OS라고 지칭함)


##### 1 - 1. 운영 체제의 역할 - 자원 할당 및 관리

- 자원 혹은 시스템 자원 (System resource)은 프로그램의 실행에 필요한 것들을 총칭
    - 데이터, 하드웨어 등이 포함됨. 

- OS는 CPU, 메모리, 보조기억장치 등에 접근, 효율적으로 사용하도록 관리하고 자원을 프로그램에 할당.

- CPU 관리: CPU 스케줄링
    - 메모리와 달리 다수의 프로그램이 동시에 CPU를 사용할 수는 없음.
    - CPU의 한정된 자원을 할당 받기 위해서는 다른 프로그램의 작업이 끝날 때 까지 기다려야 함.
    - OS가 각각의 프로그램이 CPU를 할당받을 합리적인 순서, 사용 시간을 결정함. => 'CPU 스케줄링' 이라고 부름

- 메모리 관리: 가상 메모리
    - OS는 실행하는 프로그램을 메모리 위에 적재하고, 종료된 프로그램을 메모리에서 삭제함.
    - 낭비되는 메모리가 없도록 효율적으로 관리하기도 함. => 이를 위해 가상 메모리 기술을 주로 활용
    - 가상 메모리: OS의 메모리 관리 방법 중 하나, 실제 물리적인 메모리보다 더 큰 메모리를 사용할 수 있도록 함.

- 파일, 디렉토리 관리: 파일 시스템
    - 원하는 정보를 비교적 큰 저장 공간을 가진 보조 기억 장치에서 빠르고 효율적으로 찾기 위해, OS는 이를 파일 시스템으로 관리함.
    - 파일 시스템: 보조 기억 장치 내의 데이터를 폴더 단위로 접근, 관리 가능하게 하는 OS의 내부 프로그램

- 캐시 메모리와 입출력 장치
    - 이 역시 OS에 의해서 관리되는 자원임.
    - OS는 입출력 장치의 장치 드라이버, 하드웨어 인터럽트 서비스 루틴 제공, 캐시 메모리 일관성 유지 등을 함.

- 프로세스, 스레드 관리
    - 실행중인 프로그램은 프로세스 라고 함.
    - 스레드는 프로세스를 이루는 실행 단위를 말함.
    - 메모리 상에는 여러 프로세스가 적재될 수 있으며, OS가 프로세스마다 필요한 자원을 할당함.
    - 스레드는 프로세스가 할당 받은 자원을 사용하여 작업을 수행함.
    - 스레드가 둘 이상이라면 같은 작업을 동시에 실행할 수 있음.
    - OS는 여러 프로세스와 스레드들 사이의 실행 순서를 제어하며 요구 자원을 적절히 배부하는 역할을 함.



##### 1 - 2. 운영 체제 지도 그리기

- 운영 체제
    - 운영 체제의 큰 그림
    - 프로세스 및 스레드 관리
    - 자원 할당 및 관리

- 운영 체제의 큰 그림
    - 커널
    - 시스템 콜

- 프로세스 및 스레드 관리
    - 프로세스와 스레드
    - 동기화와 교착 상태

- 자원 할당 및 관리
    - CPU 관리: CPU 스케줄링
        - 기본 개념: 우선 순위, 스케줄링 큐, 선점형과 비선점형
        - CPU 스케줄링 알고리즘
        - 리눅스 CPU 스케줄링
    - 메모리 관리: 가상 메모리
        - 물리 주소, 논리 주소
        - 메모리 할당
        - 페이징, 페이지 교체 알고리즘
    - 파일, 디렉토리 시스템: 파일 시스템
        - 파일과 디렉토리
        - 파일 시스템




##### 1 - 3. 시스템 콜과 이중 모드

- 운영 체제 역시 일종의 프로그램, 메모리 위에 올라 실행되어야 함.
    - 특별하므로, Kernel Space(커널 영역) 이라는 별도의 메모리 공간에 적재되어 실행됨.
    - 운영 체제의 기능을 제공받기 위해서는 커널 영역에 적재된 운영 체제 코드를 실행해야 한다는 점에 주목
    - 커널 영역 외에 사용자 응용 프로그램은 User Space(사용자 영역) 이라고 부르는 메모리 공간에 적재됨.

- 일반적으로 웹 브라우저, 게임과 같은 응용 프로그램은 CPU, 메모리와 같은 자원에 직접 접근하거나 조작할 수 없음.
    - 특정 자원에 접근하기 위해서는 그를 위한 OS의 코드를 실행해야 함.
    - 응용 프로그램은 System Call을 호출하여 운영 체제 코드를 실행할 수 있음.
    - 시스템 콜(System Call): 운영 체제의 서비스를 제공받기 위한 인터페이스, 호출 가능한 함수의 형태를 가짐
    - 운영 체제에 따라 시스템 콜의 개수와 기능은 다양함.

- 유닉스 시스템의 대표적인 시스템 콜 중 하나는 fork()임.
    - 새로운 자식 프로세스를 생성함.
    - 프로세스는 그 하위에 여러 프로세스를 생성할 수 있고, 이를 자식 프로세스라고 함.
    - 반대로 분화되어 나온 원래 프로세스를 부모 프로세스라고 함.

- 컴퓨터 내부에서 시스템 콜이 호출되면 수행되는 작업 순서
    - 소프트웨어 인터럽트 발생
    - CPU의 커널 모드 전환
    - 운영 체제 코드 실행
    - 사용자 모드로 재전환

- 소프트웨어 인터럽트 발생
    - 운영체제에는 '인터럽트' 를 발생시키는 특정 명령어가 존재 => 이런 명령어로 발생하는 인터럽트를 '소프트웨어 인터럽트' 라고 함.
    - 시스템 콜은 소프트웨어 인터럽트의 일종.
    - 사용자 영역을 처리하던 CPU는 시스템 콜이 발생하면, 현재 수행중인 작업을 백업하고 커널 영역 내의 인터럽트 처리를 위한 코드를 실행한 후, 다시 사용자 영역의 코드를 실행
    - 이 과정에서 CPU 사용자 영역을 실행하는 모드를 사용자 모드(user mode), 커널 영역을 실행하는 모드를 커널 모드(kernel mode)로 구분함. => 이를 이중 모드(dual mode) 라고 부름.
    - CPU의 실행 모드 구분은 플래그 레지스터 속 슈퍼바이저 플래그를 통해 확인할 수 있음. 
    - 사용자 모드에서는 OS의 서비스 제공 X => 커널 영역에 접근 불가 => 입출력과 같이 자원에 접근하는 명령어를 만나도 실행 X => 실수로라도 자원에 접근 못함.
    - 커널 모드에서는 OS의 서비스 O => 커널 영역의 코드를 실행 가능 => 자원 접근 포함, 모든 명령어 실행 가능 
    - 응용 프로그램에서 시스템 콜은 매우 자주 호출됨 => python 에서 hello world를 출력하는 간단한 프로그램도 약 600회를 호출함. => CPU 역시 매우 빈번하게 사용자 모드와 커널 모드를 전환해서 프로그램을 실행함.






### 2. 프로세스와 스레드

- 메모리에는 컴퓨터가 실행될 때 부터 매우 다양한 프로그램이 적재되어 실행됨. 

- 프로세스의 유형
    - foreground process: 사용자가 보는 공간에서 사용자와 상호작용하며 실행되는 프로세스
    - background process: 사용자가 보지 못하는 공간에서 실행되는 프로세스
        - daemon: 사용자와 상호작용 없이 주어진 명령어만 수행하는 백그라운드 프로세스(윈도우에서는 Service라고 부름)

- 프로세스를 구성하는 메모리 내의 정보
    - 다양한 프로세스의 종류에도 거의 비슷한 유형을 가짐
    - 커널 영역 내: PCB(Process Controll Block, 프로세스 제어 블록)
    - 사용자 영역 내: 코드 영역, 데이터 영역, 힙 영역, 스택 영역
    - 코드 영역, 데이터 영역은 프로그램 실행 중 크게 크기가 변하지 않음. => '정적 할당 영역' 이라고 부름.
    - 반면 힙영역과 스택 영역은 가변적 크기 => '동적 할당 영역'

- 코드 영역
    - 실행 가능한 명령어가 저장
    - 텍스트 영역(text segment)라고도 함
    - cpu가 실행할 명령어를 모아둠. => 쓰기 금지, 읽기 전용 공간

- 데이터 영역
    - 프로그램이 실행되는 동안 유지될 데이터를 저장
    - 정적 변수, 전역 변수가 대표적

- BSS 영역
    - 대표적인 영역은 아니나 실제로는 추가되어 프로세스를 구성하기도 함
    - 데이터 영역과 유사하나 초기화 여부에 따른 차이를 가짐
    - 정적 변수, 전역 변수와 같이 초기값이 존재 => 데이터 영역에 저장
    - 초기값이 없는 데이터 => BSS 영역에 저장

- 힙 영역
    - 개발자가 직접 할당 가능한 저장 공간 => 프로그램 실행 도중 비교적 자유롭게 할당하여 사용 가능
    - 힙영역의 메모리를 할당 받으면 언젠가는 반환해야 함. => 반환하지 않으면 메모리 공간이 계속 메모리를 낭비하는 메모리 누수 문제 발생.
    - 프로그래밍 언어 자체적으로 사용되지 않는 힙 메모리를 정리하는 GC(가비지 콜렉션)을 제공하기도 함.

- 스택 영역
    - 데이터 영역과 달리 일시적으로 사용되는 값이 담기는 영역
    - 함수 실행이 끝나면 사라지는 파라미터, 지역변수, 함수 복귀 주소 등을 저장
    - stack trace: 특정 시점에 스택 영역에 저장된 함수 호출 정보를 말함 => 문제 발생 지점을 알기 쉬워 디버깅에 주로 사용됨.

- PCB와 문맥 교환
    - OS가 메모리 상의 다수의 프로세스 관리를 위해서 프로세스 식별자를 커널 영역 내에 저장함 => 이 공간을 PCB 라고 함. 
    - PCB는 프로세스와 관련한 다양한 정보를 내포한 Struct의 일종, 새로운 프로세스가 메모리에 적재될 때 생성되고 해당 프로세스 종료 시 폐기됨.
    - OS마다 다르느 다양한 정보를 PCB에 담음 => 대표적으로 아래와 같은 정보를 담음.
        - 프로세스 ID(PID) 
        - 프로세스가 실행 중 사용한 레지스터 값
        - 프로세스 상태
        - 프로세스가 언제, 어떤 순위로 CPU를 할당 받을지를 보여주는 CPU 스케줄링(우선순위) 정보
        - 프로세스의 메모리 상 적재 위치 정보
        - 프로세스가 사용한 파일 입출력 장치 관련 정보

- 여러 PCB들은 프로세스 테이블(Process Table)형태로 관리되는 경우가 많음.
    - 프로세스 테이블은 실행중인 프로세스들의 PCB의 모음을 말함
    - 새롭게 실행되는 프로세스 => 프로세스 테이블에 추가되고, 리소스를 할당 받음.
    - 종료되는 프로세스 => 프로세스 테이블에서 삭제되고, 사용 중이던 자원을 반환
    - 프로세스가 비정상적으로 종료되어서 자원은 회수되었으나 프로세스 테이블에 PCB가 남는 경우가 있음. => '좀비 프로세스' 라고 부름.

- 일반적으로 메모리 위에 올라온 프로세스들은 번갈아가며 실행됨.
    - 프로세스의 실행은 OS에게 CPU와 자원을 할당받았다는 말과 같음. 
    - 프로세스의 CPU 사용 시간은 타이머 인터럽트에 의해 제어 => '타임아웃 인터럽트' 라고도 하며, 시간이 끝났음을 알리는 인터럽트임.
    - 프로세스는 부여된 시간 동안 CPU를 사용하고, 타이머 인터럽트가 발생하면 반환하고 다시 대기하는 과정을 반복함. 
    - 타이머 인터럽트가 발생하면 프로세스는 프로그램 카운터, 레지스터 값, 메모리 정보 등을 백업함 => 수행 재개를 위해 백업하는 이런 정보를 Context(문맥)라고 함
    - 문맥은 PCB에 명시됨, 즉 OS가 해당 프로세스의 문맥을 백업할 때 PCB를 사용. 다시 차례가 돌아오면 이 문맥을 복구하여 사용.
    - 위의 일련의 과정을 context switching(문맥 교환)이라고 함. 
    - 프로세스 간의 잦은 context swtiching은 cash miss의 잦은 발생을 유도함. => 메모리에서 실행할 프로세스의 내용을 로드해야 함 => 큰 오버헤드로 이어짐.

- 프로세스의 상태
    - PCB에 프로세스의 현재 상태가 저장됨. => OS마다 조금 차이가 있으나 생성, 준비, 실행, 대기, 종료 등이 있음.
    - 생성 상태: 프로세스를 생성 중인 상태, 메모리에 적재 후 PCB를 할당받은 상태 => 이후 준비가 되면 준비 상태가 되어 CPU 할당을 기다림.
    - 준비 상태: CPU를 할당만 받으면 바로 실행할 수 있으나 차례가 아니라서 기다리는 상태, CPU를 할당 받으면 실행 상태가 됨 => 이 전환을 dispatch 라고 함.
    - 실행 상태: CPU를 할당받아 일시적으로 실행 중인 상태, 타이머 인터럽트가 발생하면 다시 준비 상태로 돌아감. 실행 도중 입출력장치 등을 기다려야 하는 경우 대기 상태로 전환
    - 대기 상태: 프로세스가 입출력 작업을 대기하거나 바로 할당받을 수 없는 자원을 요청한 상태, 다시 실행 가능한 상태(입출력 완료 등)가 되면 다시 준비 상태로 돌아감.
    - 종료 상태: 프로세스가 종료된 상태, OS는 프로세스 종료 후 PCB와 프로세스가 사용한 메모리를 정리함.

- 블로킹 / 논블로킹 입출력 
    - 일반적으로 입출력 작업을 수행하면 프로세스는 대기 상태로 전환, 완료를 기다림 => 'Blocking I/O'
    - 입출력 장치에게 해당 작업을 맡기고 바로 다음 명령어를 실행 => 'Non-blocking I/O'

- 멀티 프로세스와 멀티 스레드
    - 하나의 프로세스를 구성하는 코드를 동시에 실행하는 방법 두가지

- 멀티 프로세스
    - 같은 코드를 읽어들여 여러개의 프로세스로 실행, 대표적 예시는 브라우저의 탭
    - 프로세스 간의 자원을 공유하지 않고 독립적으로 실행
    - 같은 작업을 수행하더라도 PID가 다르고 프로세스 별로 파일, 입출력 장치 등이 독립적으로 할당됨.
    - 따라서 한 프로세스에 문제가 생겨도 다른 프로세스에 영향을 미치지 않음. 

- 멀티 스레드
    - 스레드: 스레드 ID(고유 식별자), 프로그램 카운터, 레지스터 값, 스택 등으로 구성됨.
    - 스레드 마다 프로그램 카운터와 스택을 가지므로 다음 실행 주소와 연산 값의 저장이 가능함. => 병렬 실행 가능.

- 멀티 프로세스 vs. 멀티 스레드
    - 자원의 공유 여부가 가장 큰 차이점 => 여러 스레드는 한 프로세스의 자원을 공유하지만 프로세스 간의 공유는 없음.
    - 스레드들은 동일한 공간의 코드, 데이터, 힙 영역, 열린 파일 등을 공유 => 쉽게 협력, 통신이 가능함.
    - 그러나 그만큼 서로 영향도 더 많이 받음. => 한 스레드의 문제가 프로세스 전체의 문제로 번지기도 함.

- 다양한 언어(C, C++, 자바, 파이썬, 고랭 등)에서 스레드 생성, 관리를 지원함
    - 아래와 같은 예제 코드를 들 수 있음.

```python
import threading, os

def foo():
    pid = os.getpid()
    tid = threading.get_native_id()
    print(f"foo: PID={pid}, Thread ID={tid}")

def baz():
    pid = os.getpid()
    tid = threading.get_native_id()
    print(f"baz: PID={pid}, Thread ID={tid}")

def bar():
    pid = os.getpid()
    tid = threading.get_native_id()
    print(f"bar: PID={pid}, Thread ID={tid}")

if __name__ == "__main__":
    threa1 = threading.Thread(target=foo)
    threa2 = threading.Thread(target=bar)
    threa3 = threading.Thread(target=baz)

    threa1.start()
    threa2.start()
    threa3.start()

# 예시 실행 결과
# foo: PID=5113 TID=2149548
# bar: PID=5113 TID=2149549
# baz: PID=5113 TID=2149550
```

- 위 코드에서 멀티 스레딩 => 여전히 같은 프로세스이므로 PID 동일하나 TID는 모두 다름.
    - 워드가 사용자 입력을 받고, 동시에 그를 출력하며, 동시에 문법 검사를 하는 등의 기능은 이렇게 멀티 스레딩을 활용하면 구현이 가능해짐.

- 스레드 조인
    - join의 의미: 스레드 생성 주체가 해당 스레드 종료까지 대기한다는 의미
    - 예를 들어 위 코드에서 `thread1.join()` 이라고 적으면 이를 생성한 main 스레드는 1번 스레드의 종료를 기다린 뒤 종료됨.

- 프로세스 간 통신 (IPC, Inter-Process Communication)
    - 기본적으로는 프로세스간 자원을 공유하지 않지만 통신하는 방법이 있음. => 'IPC' 라고 함.
    - 2가지 유형이 존재 => '공유 메모리', '메세지 전달'
    - 공유 메모리: 말 그대로 두 프로세스가 공유해서 사용할 메모리 영역을 지정
    - 메시지 전달: 프로세스 간 데이터를 메시지 형식으로 주고 받음

- 공유 메모리
    - 두 프로세스가 공유해서 사용하는 특수한 메모리, 공유 메모리를 할당받아 사용
    - 이 IPC는 공유 영역을 확보하는 시스템 콜을 호출하거나, 간단히 프로세스 간 공유하는 변수나 파일을 활용하여 가능케하기도 함.
    - 특징은 각 프로세스 입장에서 마치 자신의 메모리 영역을 사용하는 것과 유사하며, 커널의 개입 없이 프로세스간 통신이 이루어짐.
    - 따라서 뒤에 설명할 메시지 전달 방식보다 속도가 빠름. => 사용자 영역 중의 특수한 메모리를 읽고 쓰는 것 뿐이므로. 
    - 하지만 동시에 이를 읽고 쓸 경우 데이터의 일관성 훼손 가능 => 이를 '레이스 컨디션' 이라고 함. => '동기화와 교착 상태' 에서 다룸.

- 메시지 전달
    - 프로세스 간 데이터가 커널을 거쳐 송수신 됨
    - 메시지를 보내고 받는 수단이 명확히 구분됨 => 시스템 콜(`send()`, `recv()`)이 정해져 있고 이를 호출하여 데이터를 송수신함.
    - 커널의 도움을 받으므로 레이스 컨디션과 동기화 관련 문제를 상대적으로 적게 고려할 수 있음.
    - 그러나 커널을 통해 데이터를 주고 받아서 상대적으로 느림

- 메시지 기반 IPC 수단: 파이프, 시그널, 소켓, 원격 프로시저 호출(RPC) 등.

- 파이프: 단방향 프로세스 간 통신 도구, FIFO, 두개를 사용하여 양방향 통신을 하기도 함.
    - 위에서 말한 파이프는 '익명 파이프(unnamed pip)' 라고 함. (양방향 X, 부모 - 자식 프로세스 간에서만 통신이 가능)
    - FIFO 혹은 지명 파이프(named pipe): 익명 파이프의 확장, 양방향을 지원하며 임의의 프로세스간 통신을 지원

- 시그널: 프로세스에게 특정 이벤트가 발생했음을 알리는 신호
    - 시그널은 IPC만을 위해 존재하지는 않으므로, 이를 적절히 활용해서 IPC를 수행할수도 있다는 느낌.
    - 시그널을 발생시키는 이벤트는 다양함 => 리눅스 OS의 대표적인 시그널들은 아래와 같음.
        - SIGINT: 키보드 인터럽트
        - SIGKILL: 프로세스 종료 - 핸들러 재정의 불가능
        - SIGTERM: 프로세스 종료 - 핸들러 재정의 가능
        - 이외 다양
    - 프로세스는 시그널 발생 시 여타 인터럽트와 같이 하던 일을 중단하고 시그널을 처리하는 시그널 핸들러를 실행한 후 복귀함. 
    - 프로세스는 직접 시그널을 발생시킬 수 있으며, 직접 일부 시그널 핸들러를 재정의할 수도 있음. 
    - 프로그래밍 언어 단에서 특정 시그널 발생 시의 동작을 정의하기도 함 => 특정 시그널을 보내서 프로세스간 통신을 수행할 수도 있음.
    - 특히 프로세스 간 비동기적으로 원하는 동작을 수행하기에 좋은 방법임.
    - 시그널들 마다 수행할 기본 동작이 정해져 있고 대부분 종료 혹은 코어 덤프를 생성 
    - 코어 덤프란 비정상적으로 종료 시 생성되는 파일, 프로그램이 특정 시점에 작업하던 메모리 정보가 기록됨. => 디버깅 용도로 쓰임

- RPC: 원격 프로시저 호출, 즉 '원격 코드를 실행하는 IPC 기술'
    - 반대로 한 프로세스 내에서의 특정 코드 실행을 로컬 프로시저 호출이라고 함.
    - RPC => 프로그래밍 언어, 플랫폼과 무관하게 성능 저하 최소화하며 메시지 송수신이 가능
    - 따라서 대규모 트래픽 처리 혹은 서버 간 통신 환경에서 자주 사용
    - rpc관련 기능 중 가장 대표적인 프레임 워크가 gRPC (구글 개발)

- 소켓은 나중에 배움


### 3. 동기화와 교착 상태

- 공유 메모리를 통해 여러 프로세스가 데이터를 주고 받는 경우의 공유 메모리, 혹은 여러 스레드가 한 파일을 읽고 쓰면서 공유하는 경우의 파일을 '공유 자원' 이라고 함.

- 공유 자원은 메모리나 파일, 혹은 전역 변수나 입출력 장치 등 다양할 수 있음. 

- 공유 자원에 다양한 스레드나 프로세스가 동시 다발적으로 접근하는 경우 문제가 생길 수 있음. 
    - 이렇게 공유 자원에 접근하는 코드 중 동시에 실행할 때 문제가 될 수 있는 부분을 임계 영역, critical section 이라고 부름.
    - 동시에 실행되는 프로세스, 스레드가 critical section에 진입하여 실행하면 문제가 될 수 있음.

- 멀티 프로세스, 멀티 스레드를 다룰 때는 항상 임계 구역을 신경 써야 함.
    - 두번 이상의 임계 구역의 동시 실행을 레이스 컨디션, race condition 이라고 함.
    - 이런 경우 하나가 임계 구역을 실행 중이라면 나머지는 이를 실행하지 않도록 해야 함. => 자원의 일관성을 해치지 않기 위해
    - 레이스 컨디션은 소스코드 단에서 발생. => 아래와 같은 예제 코드 참고

```c
#include <stdio.h>
#include <phtread.h>

int shared_data = 0;  // 공유 데이터

void* increment(void* arg) {
    int i;
    for (i = 0; i < 100000; i++) {
        shared_data++;
    }
    return NULL;
}

void* decrement(void* arg) {
    int i;
    for (i = 0; i < 100000; i ++) {
        shared_data--;
    }
    return NULL;
}

int main() {
    pthread_t thread1, thread2;

    pthread_create(&thread1, NULL, increment, NULL);
    pthread_create(&thread2, NULL, decrement, NULL);

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    printf("Final value of shared_data: %d\n", shared_data);

    return 0;
}
```

- 아래는 자바 예시 코드

```java
public class Race {
    static int sharedData = 0;  // 공유 데이터

    public static void main(String[] args) {
        Thread thread1 = new Thread(new Increment());
        Thread thread2 = new Thread(new Decrement());

        thread1.start();
        thread2.start();

        try {
            thread1.join();
            thread2.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // 최종값 출력
        System.out.println("Final value of sharedData: " + sharedData);
    }

    static class Increment implements Runnable {
        public void run() {
            for (int i = 0; i < 100000; i++) {
                sharedData++;  // 공유 데이터 증가
            }
        }
    }

    static class Decrement implements Runnable {
        public void run() {
            for (int i = 0; i < 100000; i++) {
                sharedData--;  // 공유 데이터 감소
            }
        }
    }
}
```

- 위 코드의 실행 결과는 0이여야 할 것 같지만, 레이스 컨디션의 결과로 -3394, 1187 등의 일정하지 않은 값이 출력되게 됨. 

- 이런 레이스 컨디션을 방지하고 임계 구역을 관리하고 싶다면 프로세스, 스레드를 동기화할 수 있음.
    - 프로세스, 스레드의 동기화, syncronization 이란 아래 2가지 조건을 만족하며 실행되는 것을 말함
    - 실행 순서 제어: 프로세스, 스레드를 올바른 순서로 실행하는 것을 말함.
    - 상호 배제: 동시에 접근해서는 안되는 자원에는 하나의 프로세스 및 스레드만 접근함.
    - 따라서 동기화란, 두가지로 구분 됨 => 실행 순서 제어를 위한 동기화, 상호 배제를 위한 동기화가 있음.

- 지금부터 말하는 동기화 기법들은 많은 프로그래밍 언어에서 지원하고 있다는 점을 참고



##### 3 - 1. 동기화 기법 - 뮤텍스 락

- 뮤텍스 락, Mutext lock: 동시에 접근해서는 안되는 자원에 동시 접근할 수 없도록 보장하는 동기화 도구
    - 뮤텍스는 MUtual EXclusion의 약자, 즉 상호 배제를 뜻함.
    - 원리는 임계 구역에 접근하고자 한다면 먼저 lock을 획득하는 것을 강요하는 것 => 임계 구역에서의 작업이 끝나면 lock을 해제함.
    - 전형적인 구현 방법은 아래와 같음.
        - lock (공유 변수), acquire과 release 함수로 구현함.
        - lock 공유 변수는 뮤텍스 락의 락 기능
        - acquire는 락을 획득하기 위한 함수, 특정 락에 대해 한번만 호출 가능하며 release는 획득한 락을 해제하는 함수
        - 따라서 lock.acquire()를 호출했을 때 다른 프로세스나 스레드가 사용중이라면 획득 불가, 대기하게 됨.
        - lock.acquire()와 lock.release()로 임계구역을 감싸듯이 구현하면 됨.

- 파이썬, C, C++은 뮤텍스 락을 지원, 자바는 다른 이름이지만 뮤텍스 락을 지원함. => 아래와 같은 예제 코드 참고

```c
#include <stdio.h>
#include <phtread.h>

int shared_data = 0;  // 공유 데이터
pthread_mutex_t mutex;  // 뮤텍스 선언

void* increment(void* arg) {
    int i;
    for (i = 0; i < 100000; i++) {
        pthread_mutex_lock(&mutex);  // 뮤텍스 락 획득
        shared_data++;
        pthread_mutex_unlock(&mutex);  // 뮤텍스 락 해제
    }
    return NULL;
}

void* decrement(void* arg) {
    int i;
    for (i = 0; i < 100000; i ++) {
        pthread_mutex_lock(&mutex);
        shared_data--;
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

int main() {
    pthread_t thread1, thread2;

    pthread_mutex_init(&mutex, NULL);  // 뮤텍스 초기화

    pthread_create(&thread1, NULL, increment, NULL);
    pthread_create(&thread2, NULL, decrement, NULL);

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    printf("Final value of shared_data: %d\n", shared_data);

    pthread_mutex_destroy(&mutex);  // 뮤텍스 해제

    return 0;
}
```

```java
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class Race {
    static int sharedData = 0;  // 공유 데이터
    static Lock lock = new ReentrantLcok();  // 락 선언

    public static void main(String[] args) {
        Thread thread1 = new Thread(new Increment());
        Thread thread2 = new Thread(new Decrement());

        thread1.start();
        thread2.start();

        try {
            thread1.join();
            thread2.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // 최종값 출력
        System.out.println("Final value of sharedData: " + sharedData);
    }

    static class Increment implements Runnable {
        public void run() {
            for (int i = 0; i < 100000; i++) {
                lock.lock();  // 락 획득
                try {
                    sharedData++;  // 공유 데이터 증가
                } finally {
                    lock.unlock();  // 락 해제
                }
                
            }
        }
    }

    static class Decrement implements Runnable {
        public void run() {
            for (int i = 0; i < 100000; i++) {
                lock.lock();
                try {
                    sharedData--;  // 공유 데이터 감소
                } finally {
                    lock.unlock();
                }
                
            }
        }
    }
}
```




##### 3 - 2. 동기화 기법 - 세마포어

- 뮤텍스 락은 하나의 공유 자원만 고려하는 경우의 도구라면, 세마포어(Semaphore)는 한번에 다수의 프로세스 혹은 스레드에게 공유 자원을 허용할 수 있는 경우 사용하는 동기화 도구
    - 뮤텍스 락의 조금 더 일반화된 버전.
    - 공유 자원이 여러개 있는 경우에도 동기화가 가능함
    - 세마포어의 어원은 철도 신호기, 그 어원처럼 멈춤, 가도 좋음 신호로 임계 구역을 관리함.

- 세마포어는 뮤텍스 락과 비슷하게 하나의 공유 변수와 두개의 함수로 구성됨
    - 변수 S: 사용 가능한 공유 자원 개수
    - wait 함수: 임계 구역 진입 전 호출하는 함수, S를 1 감소 시킨 후 0 이상인지를 검사 => 이상이라면 진입, 미만이라면 대기 상태로 프로세스나 스레드를 전환함
    - signal 함수: 임계 구역 진입 후 호출하는 함수, S를 1 증가 시킨 후 0 이상인지를 검사 => 이상이라면 공유 자원이 남는 것, 미만이라면 대기 상태인 프로세스나 스레드가 존재하는 것 => 대기 상태의 프로세스나 스레드 하나를 실행 상태로 전환함

- 구현 예제 코드

```java
import java.util.concurrent.Semaphore;

public class Sem {
    static int sharedData = 0;

    static Semaphore semaphore = new Semaphore(1);

    public static void main(String[] args) {
        Thread thread1 = new Thread(new Increment());
        Thread thread2 = new Thread(new Decrement());

        thread1.start();
        thread2.start();

        try {
            thread1.join();
            thread2.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("Final value of sharedData: " + sharedData);
    }

    static class Increment implements Runnable {
        public void run() {
            for (int i = 0; i < 100000; i++) {
                try {
                    semaphore.acquire();
                    sharedData++;
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } finally {
                    semaphore.release();
                }
            }
        }
    }

    static class Decrement implements Runnable {
        public void run() {
            for (int i = 0; i < 100000; i++) {
                try {
                    semaphore.acquire();
                    sharedData--;
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } finally {
                    semaphore.release();
                }
            }
        }
    }
}
```

```cpp
#include <iostream>
#include <thread>
#include <semaphore.h>

int sharedData = 0;
sem_t semaphore;

void increment() {
    for (int i = 0; i < 100000; i++) {
        for (int i = 0; i < 100000; i++) {
            sem_wait(&semaphore);
            sharedData++;
            sem_post(&semaphore);
        }
    }
}

void decrement() {
    for (int i = 0; i < 100000; i++) {
        for (int i = 0; i < 100000; i++) {
            sem_wait(&semaphore);
            sharedData--;
            sem_post(&semaphore);
        }
    }
}

int main() {
    sem_init(&semaphore, 0, 1);

    std::thread thread1(increment);
    std::thread thread2
}
```

- 이진 세마포 vs. 카운팅 세마포 (세마포의 종류)
    - 카운팅 세마포, counting semaphore: 위에서 다룬 세마포, 공유 자원이 여러개일 경우 사용하기 좋음.
    - 이진 세마포, binary semaphore: S 공유 변수가 0 혹은 1의 값을 가지는 세마포
        - 사실상 뮤텍스 락과 동일하게 작동함
        - 따라서 세마포라는 용어는 거의 모든 경우 카운팅 세마포를 의미함




##### 3 - 3. 조건 변수와 모니터

- 동기화 기법, 모니터에 대해. 
    - 조건 변수, conditional variable: 실행 순서 제어를 위한 동기화 도구, 특정 조건 하에서 프로세스를 실행/일시 중단함 => 실행 순서 제어
    - 조건 변수에 대해 wait, signal 함수를 호출할 수 있음. 
    - wait 함수: 호출한 프로세스의 상태를 대기 상태로 전환
    - signal 함수: (wait에 의해) 일시 중지된 프로세스 및 스레드를 재실행
    - 여기부터 재시작


