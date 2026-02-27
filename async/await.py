# await 키워드 = I/O 대기가 발생하는 순간, 실행권을 양보하는 키워드
import asyncio
import time

# 동기방식
def task_a():
    print("Task A 시작")
    time.sleep(3)
    print("Task A 끝")

def task_b():
    print("Task B 시작")
    time.sleep(3)
    print("Task B 끝")

# 비동기식
async def coro_a():
    print("Coro A 시작")
    await asyncio.sleep(3)
    print("Coro A 끝")

async def coro_b():
    print("Coro B 시작")
    await asyncio.sleep(3)
    print("Coro B 끝")

async def main():
    a = coro_a()  # 코루틴 객체 생성
    b = coro_b()  # 코루틴 객체 생성
    await asyncio.gather(a, b)  # coro_a, coro_b 동시에 실행

print("===== 동기식 실행 =====")
sync_start = time.time()
task_a()  # Task A 시작 -> 3초 대기 -> Task A 끝
task_b()  # Task B 시작 -> 3초 대기 -> Task B 끝
sync_end = time.time()
print(f"동기식 실행 시간: {sync_end - sync_start:.2f}초")

print("===== 비동기식 실행 =====")
async_start = time.time()
asyncio.run(main())  # main 실행
async_end = time.time()
print(f"비동기식 실행 시간: {async_end - async_start:.2f}초")

# [정리]
# 1. await 키워드를 통해서 코루틴 함수 안에서 실행권을 양보할 수 있다.
# 2. await 키워드는 대기가 발생하는 코드(sleep, I/O 대기) 앞에 붙인다.
# 3. 대기시간 동안 다른 코루틴이 실행되어, 전체 프로그램 대기시간을 줄일 수 있다.

# 3초씩 대기하는 함수 3개를 실행한다면,
# 동기식 -> 3초 + 3초 + 3초 = 9초
# 비동기식 -> 3초 (모두 동시에 대기) = 3초

# 비동기 방식의 단점
# 1. 어떤게 어떤 순서로 실행될지 보장할 수 없음
# 2. 실행을 잘못 시키면, 동기식으로 실행될 수 있음 (조심) -> 오히려 더 비효율적
