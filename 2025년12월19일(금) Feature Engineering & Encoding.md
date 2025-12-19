# 📘 머신러닝 심화학습 2일차 정리  
> Feature Engineering & Encoding (OneHotEncoder까지)

---

## 1️⃣ 오늘 심화 2일차에서 다룬 큰 흐름

오늘 수업의 핵심은 **“모델을 바꾸는 것보다, 입력 데이터를 어떻게 만드느냐”**였다.

### 핵심 메시지
- 좋은 모델 ❌
- 좋은 파라미터 ❌
- **좋은 Feature ⭕**

👉 **사람의 도메인 지식을 데이터로 바꾸는 과정 = Feature Engineering**

---

## 2️⃣ Feature Engineering (사람이 만드는 특성)

### 왜 필요한가?
- 실제 데이터는 바로 모델에 쓰기 어렵다
- 모델은 의미를 모른다 → **사람이 의미를 만들어줘야 한다**

---

### 🚲 따릉이 예제 – 날씨 기반 Feature Engineering

#### 가정
- 날씨가 너무 극단적이면 따릉이 이용자 수가 줄어들 것이다.

#### 생성한 Feature들

```python
# 1. 일교차
X_human['temp_diff_info'] = X_human['high_temp'] - X_human['low_temp']

# 2. 덥고 습한 날씨
X_human['sweat_info'] = X_human['high_temp'] * X_human['humidity']

# 3. 춥고 바람부는 날씨
X_human['cold_info'] = X_human['low_temp'] * X_human['wind_speed']

오늘 가장 많이 헷갈렸던 개념 정리
🔹 정규화 vs 표준화
| 구분                   | 의미           |
| -------------------- | ------------ |
| 정규화 (MinMaxScaler)   | 값의 범위를 조정    |
| 표준화 (StandardScaler) | 평균 0, 표준편차 1 |
| 단위 변경                | ❌ 둘 다 아님     |
👉 정확한 표현: 스케일을 맞춘다 / 분포를 기준화한다

🔹 리지(Ridge) & 라쏘(Lasso)
공통점
과적합 방지
가중치에 패널티 부여
차이점
| 항목    | Ridge       | Lasso        |
| ----- | ----------- | ------------ |
| 패널티   | 가중치 제곱 (L2) | 가중치 절댓값 (L1) |
| 가중치 0 | 거의 없음       | 가능           |
| 목적    | 안정화         | 변수 선택        |
“제곱을 한다”는 말의 의미
→ 가중치를 키우는 게 아니라, 큰 가중치에 더 큰 벌점을 주는 것

🔹 Feature Selection vs Dimensionality Reduction
| 구분                       | 방법    | 의미         |
| ------------------------ | ----- | ---------- |
| Feature Selection        | Lasso | 기존 변수 중 선택 |
| Dimensionality Reduction | PCA   | 새로운 축 생성   |
👉 라쏘 = 고른다 / PCA = 압축한다

🔚 마무리 정리
Feature Engineering은 사람이 하는 일
모델은 단순해도 괜찮다
좋은 Feature가 성능을 좌우한다
OneHotEncoder는 범주형 처리의 핵심
