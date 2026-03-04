import asyncio

from contextlib import asynccontextmanager
from random import choices
from urllib import response
from llama_cpp import Llama
from fastapi import FastAPI, Request, Body
from fastapi.responses import StreamingResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 실행 전 , 준비되어야 하는 리소스
    app.state.llm = Llama(
        model_path="./models/Llama-3.2-1B-Instruct-Q4_K_M.gguf",
        n_ctx=4096, # 컨텍스트 사이즈
        n_threads=2, # CPU 스레드 수
        verbose=False, # 로그 출력
        chat_format="llama-3", # 응답 생성 포맷
    )
    yield
    # 서버 종료 시 , 정리해야 하는 리소스

app = FastAPI(lifespan=lifespan)



# LLM(Large Language Model)
# 입력: 프롬프트(prompt) -> (LLM) -> 출력: 문장

# role
# system: 시스템 메시지, 모델에게 행동 지침을 제공
# user: 사용자 메시지, 모델에게 질문이나 요청을 전달
# assistant: 모델의 응답 메시지, 모델이 생성한 답변이나 정보를 포함

SYSTEM_PROMPT = (
    "You are a concise assistant. "
    "Always reply in the same language as the user's input. "
    "Do not change the language. "
    "Do not mix languages."
)

@app.post("/chats")
def generate_chat_handler(
    request: Request,
    user_input: str = Body(..., embed=True),
):
    async def event_generator():
        llm = request.app.state.llm
        response = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input},
            ],
            max_tokens=256, # 최대 토큰 수
            temperature=0.7, # 창의성 조절 (0.0 ~ 1.0)
            stream=True, # 스트리밍 응답 활성화
        )
        
        for chunk in response:
            token = chunk["choices"][0]["delta"].get("content")
            if token:
                yield token
                await asyncio.sleep(0)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )

gen = event_generator()

"Python" = next(gen)
"은" = next(gen)
"프로그래밍" = next(gen)
