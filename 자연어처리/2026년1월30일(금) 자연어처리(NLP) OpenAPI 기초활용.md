# 📅 2026-01-30(금) 자연어처리(NLP) 기초 및 OpenAI API 활용

## 📌 1. 학습 목표
- OpenAI API의 최신 버전(v1.0.0+) 문법 익히기
- **Completion(완성형)**과 **Chat(대화형)** 모델의 구조적 차이 이해
- 핵심 파라미터(`Temperature`, `Stop`, `Max_tokens`)의 원리와 튜닝
- **헬스케어 도메인**에서의 적용 포인트(안전성, 정확성, 해석 가능성) 학습

---

## 💡 2. 핵심 개념 정리

### ① Chat 모델 vs Completion 모델
| 구분 | Completion (구형) | Chat (신형/표준) |
| :--- | :--- | :--- |
| **모델명 예시** | `gpt-3.5-turbo-instruct` | `gpt-4o`, `gpt-3.5-turbo` |
| **입력 구조** | 단일 텍스트 문자열 (Prompt) | 메시지 객체의 리스트 (`System`, `User`, `Assistant`) |
| **작동 원리** | 앞 문맥에 이어질 다음 단어 예측 (이어쓰기) | 부여된 역할(Persona)과 대화 맥락에 따른 반응 |
| **헬스케어 활용** | 단순 데이터 정리, 문장 자동 완성 | **환자 상담 챗봇, 문진 시뮬레이션, 역할극** |

### ② 주요 파라미터 (Parameter Tuning)

#### **Temperature (온도)**
- **정의:** AI가 다음 단어를 선택할 때의 **확률 분포**를 조절하는 값 (0.0 ~ 2.0).
- **Low (0.0 ~ 0.2):** 가장 확률이 높은 단어만 선택. **정합성(Consistency)**이 높음.
    - *헬스케어 적용:* 의학적 진단 보조, 약물 정보 추출 등 **정답이 중요한 작업**에 필수.
- **High (0.7 ~ 1.0):** 다양한 단어를 선택. **창의성(Creativity)**이 높음.
    - *헬스케어 적용:* 환자 위로 메시지 작성, 다양한 식단 아이디어 제안 등.

#### **Stop (중단점)**
- **정의:** 특정 문자열(토큰)이 생성되면 그 즉시 텍스트 생성을 멈추는 기능.
- **작동 원리:** AI의 생성 루프(Loop) 내에서 조건문(`if token == stop_word: break`)처럼 작동.
- **활용:**
    - 불필요한 사족 제거 (비용 절감).
    - **구조화된 데이터 추출:** 수치 뒤에 오는 단위나 설명 제거.
    - **개인정보 보호:** 이름이나 주민번호 패턴 직전에서 멈추게 하여 유출 방지.

---

## 💻 3. 실습 코드 (Python OpenAI SDK v1.0+)

### ✅ Chat 모델 기본 구조 (헬스케어 페르소나 적용)
```python
import openai

# 클라이언트 객체 생성 (필수)
client = openai.OpenAI(api_key="YOUR_API_KEY")

def analyze_symptom(patient_input):
    response = client.chat.completions.create(
        model="gpt-4o",  # 최신 Chat 모델 사용
        messages=[
            # System: AI의 인격과 제한사항 설정 (보안/정확성 강화)
            {"role": "system", "content": "당신은 10년 차 응급의학과 간호사입니다. 의학적 진단은 내리지 말고, 응급 처치법만 안내하세요."},
            # User: 실제 환자의 질문
            {"role": "user", "content": patient_input}
        ],
        temperature=0,  # 의료 상담이므로 일관성 유지 (0 설정)
        max_tokens=300  # 답변 길이 제한
    )
    return response.choices[0].message.content

# 실행
print(analyze_symptom("아이가 열이 39도까지 올랐어요."))
```

### ✅ Completion 모델 (Stop 파라미터 실험)
```python
# gpt-3.5-turbo-instruct 사용 (구형 모델 호환)
response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt="아침에 일어나서 해야 할 일 리스트:\n1.",
    stop=["3."], # "3."이 나오면 멈춤 -> 1번과 2번 항목까지만 출력됨
    max_tokens=100
)
print("1." + response.choices[0].text.strip())
```

---

## ⚠️ 4. 트러블 슈팅 (Troubleshooting)

### 🚨 APIRemovedInV1 Error
- **원인:** `openai.Completion.create()` 같은 구형 문법(v0.28 이하)을 최신 라이브러리(v1.0 이상)에서 사용할 때 발생.
- **해결:** `client = openai.OpenAI()`로 클라이언트를 만들고 `client.chat.completions.create()` 형태로 변경.

### 🚨 InvalidRequestError (Model Mismatch)
- **원인:** Chat 모델(`gpt-4o`)을 Completion 엔드포인트(`completions.create`)에서 호출했을 때 발생.
- **해결:** 모델의 타입에 맞는 함수(엔드포인트)를 사용해야 함. (Chat 모델은 무조건 `chat.completions`)

---

## 🏥 5. Key Insights & Considerations

1.  **결과의 해석 가능성 (Explainability):**
    - 의료 AI는 "왜?"에 답할 수 있어야 한다. `CoT(Chain of Thought)` 기법을 통해 AI가 추론 과정을 먼저 출력하게 하면 신뢰도를 높일 수 있다.
    
2.  **데이터 희소성 (Data Sparsity):**
    - 의료 데이터는 부족하다. 따라서 `Temperature`를 낮춰(0.0) 모델이 환각(Hallucination)을 일으키지 않고 학습된 지식 내에서만 답하게 통제해야 한다.

3.  **개인정보 보호 (Privacy):**
    - 환자의 이름, 등록번호 등은 `System Prompt`에서 "비식별화하라"고 지시하거나, 전처리 단계에서 마스킹(Masking)해야 한다. API 호출 시에도 민감 정보가 포함되지 않도록 주의할 것.

---
