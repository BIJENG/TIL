# 📘 머신러닝 심화 6·7일차 핵심 정리  
## Stacking · GridSearch · RandomSearch · Optuna

---

## 1. 앙상블(Ensemble) 개요

앙상블은 **여러 모델을 결합하여 단일 모델의 한계를 극복**하는 방법이다.

- Bias(편향) 감소
- Variance(분산) 감소
- 일반화 성능 향상

대표적인 앙상블 기법
- **Bagging**: RandomForest
- **Boosting**: XGBoost, LightGBM, CatBoost
- **Stacking** ⭐

---

## 2. Stacking (스태킹)

### 2.1 Stacking이란?

> 여러 개의 base 모델이 만든 **예측 결과를 새로운 입력 데이터로 사용**하여  
> meta 모델이 최종 예측을 수행하는 앙상블 기법

구조:
원본 데이터
→ 여러 Base Model
→ 예측값(prediction)
→ Meta Model
→ 최종 예측


---

### 2.2 구성 요소

- **Base Model**
  - XGBoost, LightGBM, RandomForest, SVM 등
- **Meta Model**
  - 분류: `LogisticRegression`
  - 회귀: `LinearRegression`, `Ridge`

📌 Meta 모델은 **복잡하지 않은 모델**을 사용  
→ 과적합 방지 목적

---

### 2.3 왜 교차검증(CV)이 필수인가?

잘못된 방식:
- Base 모델이 학습에 사용한 데이터를 다시 예측
- → **Data Leakage(데이터 누수)** 발생

올바른 방식:
- K-Fold 교차검증 사용
- **Validation 데이터에 대한 예측값만** Meta 모델 학습에 사용

이때 생성되는 예측값을  
👉 **OOF (Out-Of-Fold) Prediction** 이라고 한다.

---

### 2.4 Validation 예측과 Test 예측의 역할

| 구분 | 역할 |
|---|---|
| Validation 예측 | Meta 모델 **학습용 데이터 생성** |
| Test 예측 | Meta 모델 **최종 예측 입력** |

👉 두 과정 모두 필요하며, 하나라도 빠지면 올바른 Stacking이 아님

---

### 2.5 Stacking vs Voting

| 구분 | Voting | Stacking |
|---|---|---|
| 학습 여부 | ❌ | ⭕ |
| 결합 방식 | 평균 / 다수결 | Meta 모델 학습 |
| 구조 복잡도 | 낮음 | 높음 |
| 성능 잠재력 | 보통 | 높음 |

---

## 3. GridSearchCV

### 3.1 개념

> 사용자가 지정한 하이퍼파라미터 **모든 조합을 전부 탐색**하는 방식

```python
param_grid = {
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1]
}
```

---

### 3.2 장단점

장점
- 완전 탐색
- 탐색 공간이 작을 경우 신뢰도 높음

단점
- 파라미터 수 증가 → 조합 폭발
- 고차원 공간에서 매우 비효율적
📌 비효율적인 이유는 과적합 때문이 아니라 탐색 전략의 한계

---

## 4. RandomSearchCV
### 4.1 개념
사용자가 정의한 탐색 공간 내에서
일부 조합을 무작위로 샘플링하여 탐색
```python
RandomizedSearchCV(..., n_iter=50)
```

---

### 4.2 왜 범위를 지정하는가?
완전 랜덤 ❌
사람이 의미 있는 탐색 공간(Search Space) 을 정의
그 범위 안에서 무작위 탐색
📌 즉,
RandomSearch는 범위 안에서만 랜덤

---

### 4.3 GridSearch vs RandomSearch

| 항목     | GridSearch | RandomSearch |
| ------ | ---------- | ------------ |
| 탐색 방식  | 모든 조합      | 일부 랜덤        |
| 고차원 효율 | ❌          | ⭕            |
| 실행 결과  | 항상 동일      | 실행마다 다름      |
| 실무 활용  | 낮음         | 높음           |

---

## 5. Optuna (Bayesian Optimization)
### 5.1 Optuna란?
이전 실험 결과를 학습하여
성능이 좋은 영역을 점점 집중적으로 탐색하는
하이퍼파라미터 최적화 프레임워크
핵심 개념:
Study / Trial / Objective
TPE Sampler
Bayesian Optimization

---

### 5.2 Grid / Random과의 결정적 차이

| 방법           | 이전 결과 반영 |
| ------------ | -------- |
| GridSearch   | ❌        |
| RandomSearch | ❌        |
| **Optuna**   | ⭕        |

👉 Optuna는 기억하면서 탐색한다.

---

### 5.3 Optuna 탐색 흐름

초기 Trial: 거의 랜덤 탐색
성능이 좋은 영역 파악
해당 영역을 더 자주 탐색
점진적 수렴
📌 실행마다 결과는 달라질 수 있으나
성능 범위는 일정 수준으로 수렴

---

### 5.4 Optuna를 여러 번 실행해야 하는 이유

확률적 탐색 기법
초기 탐색 경로가 실행마다 다름
→ 5회 이상 반복 실행하여 변화 추세 관찰
관찰 포인트:
최고 성능 범위
파라미터 수렴 경향
시간 대비 성능 효율

---

### 5.5 실습 결과 요약 (Pima Diabetes)

LightGBM: 가장 안정적인 성능
XGBoost: 성능 변동 존재
CatBoost: 범주형 변수가 없어 상대적으로 불리
📌 모델 특성 + 데이터 특성의 중요성 확인

---

## 6. 핵심 요약

GridSearch  → 완전 탐색 (느림)
RandomSearch → 확률 탐색 (빠름)
Optuna → 기억하는 탐색 (효율적)

Voting → 단순 결합
Stacking → 학습 기반 결합 (고성능)
