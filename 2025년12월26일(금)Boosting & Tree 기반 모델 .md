# 머신러닝 심화 정리 (Boosting & Tree 기반 모델)
> XGBoost · LightGBM · CatBoost 중심  
> + 실습 중 헷갈렸던 개념 정리

---

## 1. 앙상블(Ensemble) 복습

### 앙상블이란?
- 여러 개의 약한 모델(Weak Learner)을 결합하여
- 하나의 강한 모델(Strong Learner)을 만드는 기법

### 앙상블 종류
| 구분 | 특징 | 대표 모델 |
|---|---|---|
| Bagging | 병렬 학습, 분산 감소 | Random Forest |
| Boosting | 순차 학습, 편향 감소 | XGBoost, LightGBM, CatBoost |
| Stacking | 모델 위에 모델 | Meta Model |

---

## 2. Boosting 핵심 개념

### Boosting의 본질
- 이전 모델이 **틀린 데이터에 더 집중**
- 모델들이 **순차적으로 학습**
- Bias(편향)를 줄이는 데 강력

📌 Bagging과 차이  
- Bagging: 서로 독립 (병렬)
- Boosting: 이전 결과에 의존 (순차)

---

## 3. Gradient Boosting 개념

- 오차(residual)를 다음 모델이 학습
- 손실함수의 **Gradient**를 이용해 보정
- 성능은 좋지만 느림 → 개선한 것이 XGBoost 계열

---

## 4. XGBoost (Extreme Gradient Boosting)

### 특징
- Gradient Boosting + 정규화(L1, L2)
- 과적합 방지에 강함
- 트리 내부 분할은 병렬 처리 가능

### 핵심 포인트
- L1(`reg_alpha`), L2(`reg_lambda`) 정규화
- 결측치 자동 처리
- Level-wise 트리 성장

### 병렬 처리 정리
- ❌ 트리 간 병렬 불가 (Boosting 특성)
- ⭕ 트리 **내부 split 계산 병렬**

---

## 5. LightGBM (LGBM)

### 핵심 특징
- **Histogram 기반 분할**
- **Leaf-wise 트리 성장**
- 대용량 데이터에서 매우 빠름

### 장점
- 메모리 효율적
- 학습 속도 빠름
- 실무에서 가장 많이 사용

### 단점
- 데이터가 작으면 과적합 위험
- 파라미터 튜닝 중요

---

## 6. LightGBM의 범주형 처리 (중요)

### “카테고리화”란?
- One-Hot Encoding ❌
- 숫자 크기 비교 ❌
- **범주 집합 기준 split**

```python
df['col'] = df['col'].astype('category')
```
## 7. CatBoost (Categorical Boosting)
### CatBoost의 강점
- 범주형 변수를 자동 처리
- 별도 인코딩 필요 없음
- Target leakage 방지 설계

### 언제 쓰면 좋은가?
- 범주형 변수가 많을 때
- 데이터 크기가 크지 않을 때
- 튜닝을 최소화하고 싶을 때

## 8. Boosting 3대장 비교
| 모델       | 강점       | 단점  | 추천 상황  |
| -------- | -------- | --- | ------ |
| XGBoost  | 안정적, 정규화 | 느림  | 중간 데이터 |
| LightGBM | 빠름, 대용량  | 과적합 | 실무     |
| CatBoost | 범주형 특화   | 느림  | 범주형 多  |

## 9. Scaler를 쓰지 않는 이유 (헷갈렸던 포인트)
### 결론
Boosting은 스케일러를 자동으로 처리하는 게 아니라, 필요 없는 구조

### 이유
- 트리는 feature <= threshold 비교
- 값의 크기보다 순서(order) 가 중요

| 모델                        | Scaler |
| ------------------------- | ------ |
| XGBoost / LGBM / CatBoost | ❌      |
| Logistic / SVM / KNN      | ⭕      |

## 10. L1 / L2 정규화 개념 정리
### L1, L2는?
- ❌ 분류/회귀 알고리즘 아님
- ⭕ 손실함수에 추가되는 패널티

| 구분    | L1    | L2  |
| ----- | ----- | --- |
| 방식    | 절대값   | 제곱  |
| 효과    | 피처 선택 | 안정화 |
| 가중치 0 | 가능    | 불가  |
📌 Boosting(XGB, LGBM) 내부에서도 사용됨

## 11. 평가 지표(scoring) 정리
### 분류(Classification)
```
accuracy
precision
recall
f1
roc_auc
```
- accuracy: 전체 정답률
-precision: 양성 예측 신뢰도
- recall: 실제 양성 탐지율

## 회귀(Regression)
- r2
- neg_mean_absolute_error
- neg_mean_squared_error
- neg_root_mean_squared_error

📌 GridSearchCV에서는 클수록 좋은 값 기준
→ MAE, MSE는 neg_ 사용
