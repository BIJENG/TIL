# (SVM · RFE · 앙상블 · Random Forest 중심)

---

## 1. 오늘 배운 핵심 한 줄 요약

- **SVM은 모델이다**
- **RFE / RFECV는 피처 선택 도구다**
- **선형 모델은 해석과 선택, 비선형 모델은 예측 성능**
- **앙상블은 여러 모델을 묶는 전략**
- **Random Forest와 Extra Trees는 Bagging 기반 앙상블 모델**

---

## 2. SVM 정리 (Support Vector Machine)

### 2-1. SVM이란?
- 데이터를 나누는 **결정 경계(마진)** 를 최대화하는 모델
- 분류/회귀 모두 가능

| 문제 유형 | 모델 |
|---|---|
| 분류 | SVC |
| 회귀 | SVR |

---

### 2-2. 선형 SVM vs 비선형 SVM

#### 🔹 선형 SVM (Linear Kernel)

```text
y = w1x1 + w2x2 + ... + wn xn + b
```

- 직선(혹은 평면)으로 데이터 분리
- 각 피처에 대한 계수(coef_) 존재
- 해석 가능
- 피처 중요도 계산 가능
- RFE / RFECV와 함께 사용 가능
- 비선형 SVM (RBF Kernel)
- 커널 트릭을 사용해 고차원 공간에서 분리
- 복잡한 비선형 패턴 학습 가능
- coef_ 없음
- 해석 어려움
- 최종 예측 모델로 적합

### 2.3 왜 선형 SVM과 비선형 SVM을 함께 쓰는가?

피처 선택 단계에서는 중요도 해석이 필요

예측 단계에서는 성능이 더 중요
| 단계    | 목적     | 모델      |
| ----- | ------ | ------- |
| 피처 선택 | 중요도 판단 | 선형 SVM  |
| 최종 예측 | 성능 극대화 | RBF SVM |

## 3. RFE / RFECV 정리
### 3.1 RFE (Recursive Feature Elimination)
중요도가 낮은 피처를 하나씩 제거
피처 개수는 사용자가 직접 지정

### 3.2 RFECV (RFE + Cross Validation)
RFE에 교차검증(CV)을 결합
피처 개수를 자동으로 선택

### 3.3 RFECV의 역할
RFECV가 하는 일
사용할 피처 선택
최적의 피처 개수 결정
RFECV가 하지 않는 일
C, gamma, epsilon 같은 하이퍼파라미터 튜닝
모델 구조 변경

### 3.4 RFECV vs GridSearchCV
| 구분 | RFECV    | GridSearchCV |
| -- | -------- | ------------ |
| 대상 | 피처(X)    | 모델 파라미터      |
| 목적 | 변수 선택    | 성능 최적화       |
| 예시 | 어떤 컬럼 제거 | C=1 vs C=10  |

## 4. 앙상블(Ensemble) 개념
### 4.1 앙상블이란?
여러 모델을 결합하여 하나의 강력한 모델을 만드는 기법
개별 모델의 약점을 보완
일반화 성능 향상

###4.2 앙상블의 주요 방식
Bagging (Bootstrap Aggregating)
여러 모델을 병렬적으로 학습
예측 결과를 평균 또는 투표로 결합
분산 감소, 과적합 완화
Boosting
이전 모델의 오답을 다음 모델이 학습
순차적으로 성능 개선
(이번 수업에서는 개념만 언급)

## 5. Bagging 기반 트리 앙상블
### 5.1 Random Forest
개념
Decision Tree 여러 개를 Bagging 방식으로 결합
각 트리는 데이터 샘플과 피처를 무작위로 선택

특징
스케일링 불필요
비선형 관계 학습 가능
Gini Importance 제공
과적합에 강함

### 5.2 Extra Trees (Extremely Randomized Trees)
공통점
트리 기반
Bagging 방식
피처 중요도 제공
Random Forest와의 차이
| 항목      | Random Forest | Extra Trees |
| ------- | ------------- | ----------- |
| 데이터 샘플링 | Bootstrap 사용  | 전체 데이터 사용   |
| 분할 기준   | 최적 분할 탐색      | 완전 랜덤 분할    |
| 분산      | 낮음            | 더 낮음        |
| 편향      | 보통            | 약간 높음       |
| 학습 속도   | 느림            | 빠름          |

## 6. Random Forest vs Extra Trees 사용 기준
Random Forest
기본 선택
안정적인 성능
해석이 중요한 경우
Extra Trees
데이터 크기가 큰 경우
학습 속도가 중요한 경우
과적합이 심한 경우
