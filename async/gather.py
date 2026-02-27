# gater =  모으다
import asyncio
# 코루틴 = 동시에 실행되는 함수들

async def hello():
    print("Hello")


coro1 = hello()  # 코루틴 객체 생성
coro2 = hello()  # 코루틴 객체 생성

async def main():
    await asyncio.gather(coro1, coro2)  # coro1, coro2 동시에 실행


asyncio.run(main())  # main 실행

# [정리]
# 1. 코루틴은 동시에 같이 실행되기 위한 함수들이다.
# 2. 코루틴은 하나만 실행할거면, 굳이 비동기로 할 이유가 없다.
# 3. 비동기 문법을 쓰더라도, 실제 프로그램의 동작은 동기식으로 동작 할 수 있다. (조심)
# 4. 코루틴을 동시에 실행하는 방법은 gather() 를 사용
