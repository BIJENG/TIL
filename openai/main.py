from contextlib import asynccontextmanager
from fastapi import FastAPI, Body, Request
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI
from pydantic import BaseModel, Field

from config import settings

# # 1. .env 파일의 내용을 환경 변수로 불러옵니다.
# load_dotenv()

# # 2. os.getenv를 이용해 환경 변수에 저장된 키를 가져옵니다.
# api_key = os.getenv("OPENAI_API_KEY")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.openapi_client = AsyncOpenAI(api_key=settings.openai_api_key)
    yield

app = FastAPI(lifespan=lifespan)

# 원하는 응답의 형식을 고정
class ResultSchema(BaseModel):
    result: str = Field(..., description="질문에 대한 답변")
    confidence: float = Field(..., description="답변에 대한 신뢰도 점수 (0.0 ~ 1.0)")


@app.post(
    "/gpt"
)
async def call_gpt_handler(
    request: Request,
    user_input: str = Body(..., embed=True)
):
    client = request.app.state.openapi_client

    async def event_generator():
        # 1) OpenAI 서버로 스트리밍 요청을 보낸다
        async with client.responses.stream(
            model="gpt-4.1-mini",
            input= user_input,
            text_format= ResultSchema,
        ) as stream:
            # 2) 스트리밍 데이터를 하나씩 event라는 형태로 응답 받는다.
            async for event in stream:
                # 3-1) event 값이 delta면, 그 안의 값(token)을 꺼낸다
                if event.type == "response.output_text.delta":
                    yield event.delta
                # 3-2) event가 complete면, 스트리밍을 종료한다
                elif event.type == "response.completed":
                    break

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )


# 비동기 함수로 만들어 놓고, 내부 동작은 동기 함수다.
# from OpenAPI -> from AsyncOpenAPI
# response = client.responses.parse... -> response = await client.responses.parse...


