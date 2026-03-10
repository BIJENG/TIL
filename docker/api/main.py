import json
import uuid
from redis import asyncio as aredis
from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from sqlalchemy import text
from database import SessionFactory

# 답변 생성을 요청하면, 대기 발생
# 대기하는 동안, 다른 일(HTTP 요청) 처리

redis_client = aredis.from_url("redis://redis:6379", decode_responses=True)

app = FastAPI()

# [쿼리 파라미터(QueryParameter)]
# GET google.com/search?q=python -> 새로운 데이터를 만들어내거나, 데이터 변경 X

# Post -> 새로운 데이터를 생성

# [1] 클라이언트에서 질문(question)을 요청한다.
@app.post("/chats")
async def chat_handler(
    question: str = Body(..., embed=True)
):
    # 1. 고유 식별자(job_id)를 가장 먼저 만듭니다.
    job_id = str(uuid.uuid4()) 
    
    # 2. 생성된 job_id를 사용하여 채널 이름을 정의합니다.
    channel = f"result:{job_id}"

    # 3. 구독을 시작합니다.
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(channel)

    try:
        # 4. 이제 작업을 큐에 넣습니다. (Worker가 이 job_id를 보고 답변을 보냅니다.)
        job = {"id": job_id, "question": question}
        await redis_client.lpush("inference_queue", json.dumps(job))
        
        # 5. 결과를 기다립니다.
        async def event_generator():
            async for message in pubsub.listen():
                if message["type"] == "message":
                    data = message["data"]
                    if data == "[DONE]":
                        break
                    yield data
                    


        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream"
        )
        
    finally:
        # 6. (중요) 작업이 끝나면 구독을 해제하고 연결을 닫습니다.
        await pubsub.unsubscribe(channel)
        await pubsub.close()

'''
1) Path
2) Query
3) Request Body
    3-1) xxx: UserSignUpRequest = Body(...)
    3-2) xxx: str = Body(..., embed=True) -> 요청 본문 데이터가 1개일 때

'''