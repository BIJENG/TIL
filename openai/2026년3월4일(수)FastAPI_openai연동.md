# FastAPI & OpenAI API 연동 및 서버 배포 개념 총정리

## 1. 환경 변수와 보안 관리 (.env & config.py)

- **.env 파일:** API 키(`OPENAI_API_KEY` 등)와 같이 외부에 유출되면 안 되는 비밀 장부. 관례상 상수를 의미하는 **대문자**로 작성한다. GitHub에 절대 올리면 안 됨(`.gitignore` 필수).
- **config.py (Settings):** `.env`의 값을 파이썬 코드에서 안전하고 편리하게 불러오기 위한 중앙 관리소. 코드 곳곳에 `os.getenv`를 뿌리는 대신, `settings.openai_api_key` 형태로 객체화하여 사용한다.

## 2. FastAPI Lifespan (자원 효율화)

- **개념:** 서버의 시작(`yield` 이전)과 종료(`yield` 이후) 시점에 딱 한 번씩만 실행되는 관리자.
- **목적:** 요청이 들어올 때마다 무거운 객체(OpenAI 클라이언트, DB 연결, LLM 모델 등)를 새로 만들면 서버가 느려진다. Lifespan에서 한 번만 생성하여 `app.state`라는 공용 공간에 넣어두고 재사용함으로써 **응답 속도와 자원 효율을 극대화**한다.

## 3. 구조화된 출력 (Structured Outputs & Schema)

- **개념:** AI가 제멋대로 대답하지 못하게, Pydantic `BaseModel`을 이용해 원하는 응답 규격(JSON)을 강제하는 방법.
- **최신 문법:** OpenAI SDK v1.50+ 기준, `client.beta.chat.completions.parse` 메서드와 `response_format` 인자를 사용한다.
- **장점:** 응답에서 텍스트(`result`)와 수치(`confidence`) 등을 깔끔하게 파이썬 객체로 분리해서 받을 수 있어, 프론트엔드로 데이터를 넘겨주거나 DB에 저장하기가 매우 쉬워진다.

## 4. 진짜 비동기(Async) 서버 만들기

- **동기(Sync)의 한계:** 앞사람의 AI 답변이 생성되는 5초 동안 서버 전체가 멈춰서 다른 사람의 요청을 받지 못한다.
- **비동기(Async)의 마법:** AI가 답변을 생성하는 네트워크 대기 시간 동안, 서버는 다른 사람의 요청을 처리한다. 단일 응답 속도(Latency)가 빨라지는 것이 아니라, **서버가 동시에 감당할 수 있는 처리량(Throughput)**이 압도적으로 늘어난다.
- **구현:** 함수만 `async def`로 만드는 것("무늬만 비동기")이 아니라, 내부 클라이언트도 `AsyncOpenAI`를 쓰고 호출 시 `await`를 반드시 붙여야 한다.

## 5. 배포의 정석: Docker와 AWS

- **Docker (포장 기술):** 내 코드가 "내 컴퓨터 환경"을 벗어나 어디서든 똑같이 실행되도록 OS, 라이브러리, 코드를 하나의 박스(컨테이너)로 묶는 도구.
- **AWS (운영 환경):** 도커로 예쁘게 포장된 박스를 24시간 전기가 들어오는 넓은 땅에 올려두고, 전 세계 사람들이 접속할 수 있게 주소를 부여하는 클라우드 서비스. (예: ECS, Fargate 등)

---

## 🚀 [실무 적용] 최종 완성 코드 템플릿

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Body, Request, HTTPException
from openai import AsyncOpenAI  # 진짜 비동기를 위한 라이브러리
from pydantic import BaseModel, Field
from config import settings

# 1. Lifespan: 서버 시작 시 비동기 클라이언트 1회 생성
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.openapi_client = AsyncOpenAI(api_key=settings.openai_api_key)
    yield
    await app.state.openapi_client.close()

app = FastAPI(lifespan=lifespan)

# 2. Schema: AI 응답 규격 강제
class ResultSchema(BaseModel):
    result: str = Field(..., description="질문에 대한 답변")
    confidence: float = Field(..., description="답변에 대한 신뢰도 점수 (0.0 ~ 1.0)")

# 3. Handler: 들어온 요청을 비동기로 처리
@app.post("/gpt")
async def call_gpt_handler(request: Request, user_input: str = Body(..., embed=True)):
    client = request.app.state.openapi_client

    try:
        # 4. await를 통한 완벽한 비동기 호출 및 구조화된 파싱
        response = await client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_input}],
            response_format=ResultSchema,
        )
        return {"output": response.choices[0].message.parsed}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```
