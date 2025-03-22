from multiprocessing import Process, Value
import time

def increment(counter):
    for _ in range(1_000):
        temp = counter.value
        temp += 1
        time.sleep(0.0001)
        counter.value = temp

def decrement(counter):
    for _ in range(1_000):
        temp = counter.value
        temp -= 1
        time.sleep(0.0001)
        counter.value = temp

if __name__ == "__main__":
    counter = Value('i', 0)

    p1 = Process(target=increment, args=(counter,))
    p2 = Process(target=decrement, args=(counter,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print(f"최종 counter 값: {counter.value}")  # 답: 87, -188 등, 매번 다름. 

# 파이썬의 병렬 처리 방법은 크게 3가지
# 1. 멀티 스레드
# 2. 멀티 프로세스
# 3. async

# 스레드는 GIL의 영향을 크게 받으나, IO 혹은 네트워크 관련 작업의 경우 대기 시간 동안 자동으로 GIL을 반납하는 로직이 내장
# 따라서 해당 경우 병렬성 보장 가능
# 그러나 cpu 기반 작업에서는 cpu가 계속 바쁘므로 GIL을 반납 X, 따라서 5ms 마다 (기본 설정) 스레드는 바뀌지만 실제 현재 실행되는 스레드는 1개
# 따라서 직렬로 실행되는 것과 실행 효율은 크게 다르지 않음 (컨텍스트 스위칭 생각하면 오히려 나쁠지도?)

# 멀티 프로세스는 각자의 프로세스가 별도로 돌아가므로 이들끼리는 GIL의 영향이 없음.
# 따라서 진정한 의미의 병렬성을 보장해줄 수 있음.

# async는 흔히 말하는 비동기식 처리
# 단일 프로세스, 스레드에서도 병렬적으로 작업들을 실행할 수 있는 방법.
# 비동기는 단일 스레드에서도, '시간'을 나누어 쓰는 방식임
# 자신에게 부여된 cpu 시간을 나누어서 쓰는 방법
# 대기할 일이 많은 작업들, 크롤링, 서버, 파일작업, DB 쿼리 등에서 효율적인 방법 => 반대로 cpu가 바쁘면 별 의미없음.
# 예제 코드는 아래와 같음

import asyncio

async def download_file():
    print("다운로드 시작!")
    await asyncio.sleep(2)  # 2초 기다리면서 CPU는 다른 일 함
    print("다운로드 완료!")

async def main():
    task1 = asyncio.create_task(download_file())
    task2 = asyncio.create_task(download_file())

    await task1
    await task2
    print("두 개의 다운로드 완료! 이제 다음 작업 시작!")

asyncio.run(main())
