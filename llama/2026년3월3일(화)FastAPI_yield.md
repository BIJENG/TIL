# TIL (Today I Learned) - 2026.03.03

## 1. Hugging Face 권한 및 인증 (Authentication)

- **권한의 계층 구조**: `Write` 토큰은 `Read` 토큰의 모든 권한(모델 다운로드 등)을 포함하며, 추가로 모델 업로드(Push)까지 가능하다.
- **터미널 로그인 에러 해결**: Windows PowerShell에서 `hf auth login` 명령어가 보안/버전 문제로 `Bad Request`를 뱉을 때, 파이썬 코드로 직접 로그인하는 것이 가장 확실하다.
  ```python
  from huggingface_hub import login
  login()  # 실행 후 발급받은 Write 토큰을 우클릭으로 붙여넣기
  ```

## 2. 로컬 LLM 서빙 (Llama 3.2 1B GGUF)

- **GGUF 포맷**: CPU와 GPU 환경 모두에서 메모리를 효율적으로 쓰기 위해 양자화(Quantization)된 모델 포맷.
- **llama-cpp-python**: C++ 기반의 엔진을 파이썬에서 돌리기 위한 라이브러리. (설치 시 C++ Build Tools 빌드 과정이 진행됨)
- **Trailing Comma (마지막 쉼표)**: 파이썬은 리스트나 함수의 마지막 인자 뒤에 `,`를 남기는 것을 허용(오히려 권장)함. 향후 설정 추가가 쉽고 Git 변경 이력(Diff)을 깔끔하게 관리할 수 있기 때문.

## 3. Python 비동기 및 메모리 관리의 핵심

### ① Coroutine (코루틴)

- `async def`로 선언하는 특별한 함수.
- 실행 도중 `await`를 만나면 작업을 잠시 멈추고 제어권을 시스템(Event Loop)에 넘김. 덕분에 Llama가 답변을 만드는 긴 시간 동안 서버가 뻗지 않고 다른 사용자의 요청을 받을 수 있음.

### ② Generator (제너레이터)와 Yield (산출)

- `return`은 모든 데이터를 한 번에 던지고 함수를 종료(메모리 폭발 위험).
- `yield`는 데이터를 하나씩 산출하고 함수 상태를 **일시 정지(유지)**함.
- **활용**: 대용량 데이터를 다룰 때 메모리를 아끼거나, AI의 답변을 ChatGPT처럼 한 글자씩 실시간으로 화면에 쏴주는 **스트리밍(Streaming)** 기능에 필수적.

### ③ FastAPI의 Lifespan (수명 주기)

- 서버가 시작할 때(Startup)와 종료될 때(Shutdown) 실행할 코드를 제너레이터(`yield`)로 분리해 관리하는 기능.
- 사용자가 질문할 때마다 무거운 AI 모델을 매번 로드하면 서버가 멈추기 때문에, Lifespan을 통해 **서버가 켜질 때 메모리에 딱 한 번만 올려두고 재사용**함.

## 4. Troubleshooting (에러 해결)

- **PowerShell Curl 에러**: 윈도우 PowerShell의 `curl(Invoke-WebRequest)`은 리눅스와 문법이 다름. `-H` 뒤에 헤더를 넣을 때 단순 문자열이 아닌 딕셔너리(`@{}`) 형태로 줘야 함. (명령 프롬프트 CMD를 쓰거나, FastAPI의 `/docs` Swagger UI를 쓰는 것이 정신건강에 좋음)
- **404 Not Found**: 서버는 켜져 있는데 에러가 난다면 코드의 엔드포인트 주소(예: `/ask` vs `/chats`)와 HTTP 메서드(GET vs POST)가 일치하는지 확인 필수.
