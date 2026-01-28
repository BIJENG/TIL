# 🏥 헬스케어 텍스트 분석: 기초부터 심화까지(TF-IDF, Network, CONCOR, LDA)

---

## 1. 텍스트의 중요도 평가: TF-IDF

### 💡 개념 (Concept)
단순히 단어가 많이 나왔다고(TF) 무조건 중요한 게 아닙니다. '환자', '병원', '진료'처럼 의료 데이터에서 너무 흔하게 나오는 단어(DF)는 점수를 깎아서 가중치를 조절하는 기법입니다.

* **핵심:** **"여기서만 자주 나오는 단어가 진짜 주인공이다!"**
* **헬스케어 예시:** 모든 진료 기록에 있는 '통증'은 중요도가 낮고, 특정 희귀 질환 환자에게만 나오는 '면역억제제'는 중요도가 높게 나옵니다.

### 🐍 파이썬 구현 (Python Code)

```python
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# 1. 의료 데이터 예시 (문서 집합)
docs = [
    '환자 당뇨 인슐린 처방', 
    '환자 감기 기침 처방', 
    '당뇨 합병증 혈당 관리'
]

# 2. TF-IDF 객체 생성
# min_df=1: 최소 1번 이상 등장한 단어만 계산
tfidf_vect = TfidfVectorizer(min_df=1)

# 3. 행렬 변환 (수학적 계산)
tfidf_matrix = tfidf_vect.fit_transform(docs)

# 4. 결과 확인 (데이터프레임 변환)
features = tfidf_vect.get_feature_names_out()
df_tfidf = pd.DataFrame(tfidf_matrix.toarray(), columns=features)

print("단어별 중요도 점수:")
print(df_tfidf)
```

---

## 2. 단어 관계 지도 그리기: 네트워크 분석 (Network Analysis)

### 💡 개념 (Concept)
단어와 단어 사이의 **동시 출현(Co-occurrence)** 관계를 선(Edge)으로 연결하여 시각화합니다. 어떤 단어들이 함께 다니는지 파악할 수 있습니다.

* **핵심:** **"누가 누구랑 짝꿍인가?"**
* **헬스케어 예시:** '기침'이라는 단어가 나왔을 때 '가래'와 연결되는지, 아니면 '폐렴'과 연결되는지 그 관계를 파악합니다.

### 🐍 파이썬 구현 (Python Code)

```python
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer

# 1. 데이터 준비
data = ['기침 가래 발열', '기침 발열 오한', '복통 설사', '기침 가래 폐렴']

# 2. 동시 출현 행렬 만들기 (Co-occurrence Matrix)
# 누가 누구랑 같이 나왔는지 세는 작업
cv = CountVectorizer()
X = cv.fit_transform(data)
co_occurrence = (X.T * X) # 행렬 곱셈으로 관계 계산
co_occurrence.setdiag(0)  # 자기 자신과의 관계(기침-기침)는 0으로 제거

# 3. 네트워크 그래프 생성
names = cv.get_feature_names_out()
graph = nx.from_numpy_array(co_occurrence)

# 노드 이름을 숫자가 아닌 실제 단어로 변경
mapping = {i: v for i, v in enumerate(names)}
graph = nx.relabel_nodes(graph, mapping)

# 4. 시각화 (한글 폰트 설정 필수)
# 코랩에서는 별도의 한글 폰트 설치 과정이 선행되어야 함
plt.figure(figsize=(5, 5))
nx.draw(graph, with_labels=True, node_color='skyblue', node_size=2000, font_family='NanumGothic')
plt.show()
```

---

## 3. 끼리끼리 뭉치기: CONCOR 분석

### 💡 개념 (Concept)
네트워크 상에서 **구조적 등위성(Structural Equivalence)**을 분석합니다. 직접 연결되지 않았더라도, 연결된 패턴(주변 친구들)이 비슷하면 같은 그룹(Cluster)으로 묶어줍니다.

* **핵심:** **"노는 물(패턴)이 비슷하면 같은 그룹이다!"**
* **헬스케어 예시:** '의사'와 '간호사'가 문장에서 직접 같이 나오지 않더라도, 둘 다 '환자', '치료', '병원'과 연결되어 있다면 **[의료진 그룹]**으로 묶입니다.

### 🐍 파이썬 구현 (Python Code)

```python
import numpy as np

# CONCOR 알고리즘 함수 (상관계수 반복 계산)
def concor(matrix, iter_num=10):
    for _ in range(iter_num):
        # 상관계수(Correlation) 계산
        matrix = np.corrcoef(matrix)
        # NaN 값(계산 불가) 처리 -> 0으로 채움
        matrix = np.nan_to_num(matrix)
    return matrix

# 위 네트워크 분석에서 만든 co_occurrence 행렬을 입력으로 사용
concor_result = concor(co_occurrence.toarray())

# 결과: +1과 -1로 그룹이 명확하게 갈라진 행렬 확인
print("CONCOR 분석 결과 행렬 (상위 3줄):")
print(concor_result[:3]) 
```

---

## 4. 숨겨진 주제 찾기: LDA 토픽 모델링

### 💡 개념 (Concept)
문서 집합(Corpus)에 숨겨진 추상적인 **주제(Topic)**를 확률적으로 찾아내는 기법입니다. (Latent Dirichlet Allocation)

* **핵심:** **"이 수많은 문서들은 결국 몇 가지 이야기로 요약될 수 있는가?"**
* **헬스케어 예시:** 수만 건의 환자 리뷰를 분석해 Topic 1(친절도 관련), Topic 2(위생 상태 관련), Topic 3(치료 효과 관련) 등으로 자동 분류합니다.

### 🐍 파이썬 구현 (Python Code)

```python
from sklearn.decomposition import LatentDirichletAllocation

# 1. 벡터화 (CountVectorizer 사용)
# LDA는 단어의 등장 빈도(Count) 정보를 기반으로 합니다.
cv = CountVectorizer(max_features=1000)
term_matrix = cv.fit_transform(data) # 위 데이터 재사용

# 2. LDA 모델 학습
# n_components=2 : 주제를 2개로 찾아달라고 요청
lda = LatentDirichletAllocation(n_components=2, random_state=42)
lda.fit(term_matrix)

# 3. 주제별 핵심 단어 출력
terms = cv.get_feature_names_out()
for idx, topic in enumerate(lda.components_):
    print(f"Topic #{idx+1}: ", end="")
    # 각 주제에서 가장 비중이 큰(중요한) 상위 단어 3개 출력
    top_terms_indices = topic.argsort()[:-4:-1]
    print([terms[i] for i in top_terms_indices])
```
## 🚀 회고

1. **전처리가 생명이다 (Preprocessing First):** 헬스케어 데이터는 오타도 많고, '감기'='상기도감염'처럼 같은 뜻 다른 단어도 많습니다. `spacy`나 정규표현식을 써서 데이터를 깨끗하게 닦지 않으면 위 분석들은 의미가 없어집니다. (Garbage In, Garbage Out)
2. **해석 가능성 (Explainability):** LDA나 CONCOR로 그룹을 나눴다면, 그 결과가 의학적으로 말이 되는지 반드시 확인해야 합니다. 단순히 "나눴다"에 그치지 말고 "왜 이렇게 나뉘었지?"를 고민하세요.
3. **데이터 보안 (Privacy):** 코드 공유 시 실제 환자 이름이나 병원 정보 등 민감한 정보(PII)가 포함되지 않도록 반드시 마스킹 처리를 하세요.
