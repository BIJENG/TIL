import asyncio
import time

async def good_task():
    print("착한 작업 시작")
    await asyncio.sleep(5)
    print("착한 작업 끝")

async def bad_task():
    print("나쁜 작업 시작")
    time.sleep(5)  # 동기식으로 대기 -> 다른 작업을 처리하지 못함
    print("나쁜 작업 끝")\

async def main():
    await asyncio.gather(
        good_task(), 
        good_task(), 
        good_task(), 
        good_task(), 
        bad_task()
    )  # good_task, bad_task 동시에 실행

asyncio.run(main())  # main 실행