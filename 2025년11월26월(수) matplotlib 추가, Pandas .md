AI 헬스케어 데이터 분석 – 1일차 정리
주제
데이터 다루기의 시작 – CSV 불러오기와 정제
데이터: train.csv (당뇨병 환자 데이터)

학습 목표
pd.read_csv()로 CSV를 DataFrame으로 불러오기
DataFrame의 행, 열, 인덱스, dtype 이해
Pandas의 기본 조작: 생성, 선택, 필터링, 정렬, 수정, 추가/삭제 실습
결측치 개념 이해 및 처리: isnull(), dropna(), fillna()
Seaborn 샘플 데이터셋 불러와 기초 탐색 및 시각화

데이터·데이터사이언스·데이터엔지니어링 한 줄 정리
용어	              의미
데이터 분석	        데이터를 정리·요약·해석해 무슨 일이 있었고 왜 그런지 설명하고 의사결정 근거를 만드는 활동
데이터 사이언스	    데이터를 통해 세상의 패턴을 발견하고, 미래를 예측하거나 의사결정을 돕는 모델을 만드는 학문
데이터 엔지니어링	  데이터를 수집·저장·옮기는 파이프라인 구축 (도로 깔기)
데이터 사이언스	    데이터 위에서 분석·모델링 수행 (도로 달리기)

1. Pandas란?
엑셀을 코딩으로 조작할 수 있는 도구
표 형태 데이터를 DataFrame 구조로 관리
통계, 필터링, 그룹화, 시각화 가능
리스트/딕셔너리만으로는 불편한 행·열 단위 분석을 편리하게 수행 가능
import pandas as pd
from IPython.display import display

data = {
    "Name": ["Tom", "Jane", "Alice", "Bob"],
    "Age": [28, 34, 29, 42],
    "Score": [85, 92, 88, 75]
}

df_sample = pd.DataFrame(data)
display(df_sample)

print("\n데이터 타입(dtypes):")
print(df_sample.dtypes)

핵심 차이
구분	      Series	            DataFrame
구조	      1차원	              2차원
구성	      인덱스 + 값	        인덱스 + 여러 열(Series 모음)
예시	      하나의 컬럼 데이터	  전체표(엑셀 시트 같은 구조)

2. 데이터 선택과 수정
2-1. loc & iloc
메서드	설명
iloc	위치 기반 인덱싱 (정수 index)
loc	이름(label) 기반 인덱싱
# Tom의 Score 수정
df_sample.loc[df_sample["Name"] == "Tom", "Score"] = 90
display(df_sample)

# Passed 컬럼 추가 (Score >= 80)
df_sample["Passed"] = df_sample["Score"] >= 80
display(df_sample)


loc: [행조건, 열] → 행과 열 선택 가능

새로운 컬럼 지정 시 존재하지 않으면 자동 생성됨

2-2. 조건부 컬럼 추가 예시
df_sample.loc[df_sample["Score"] >= 85, "Level"] = "High"
df_sample.loc[df_sample["Score"] < 85, "Level"] = "Normal"
display(df_sample)


Score >= 85 → Level = "High"

Score < 85 → Level = "Normal"

없는 컬럼도 loc로 값 대입 시 자동 생성됨
내부적으로는 각 행을 검사하여 조건에 맞는 경우 값 대입 (자동 반복)

2-3. 새 컬럼 추가
df_sample["Habit"] = ["야구", "농구", "축구", "수영"]  # 행 수와 동일해야 함
display(df_sample)

2-4. 새 행 추가
df_sample.loc["e"] = ["Farmer", 20, 100, True, "Normal", "테니스"]  # 컬럼 수와 동일
display(df_sample)

3. 기초 통계
평균(Mean)
import numpy as np
scores = np.array([80, 90, 100])
print(f"평균 점수: {np.mean(scores)}")  # 90.0

전체 합계를 인원수로 나눈 값
장점: 모든 데이터 반영
단점: 극단값(outlier)에 민감

중앙값(Median)
salaries = np.array([3000, 3200, 3100, 8000])
print(f"연봉 중앙값: {np.median(salaries)}")  # 3150.0

데이터 크기순 정렬 후 가운데 값
극단값 영향을 거의 받지 않음

표준편차(Standard Deviation)
class_a_scores = np.array([85, 88, 82])
class_b_scores = np.array([100, 60, 95])

print(f"A반 표준편차: {np.std(class_a_scores):.2f}")  # 2.49
print(f"B반 표준편차: {np.std(class_b_scores):.2f}")  # 18.50


평균 주변 데이터 흩어짐 정도
작을수록 안정적, 클수록 변동 심함
실생활 활용
정상 범위 설정: 건강 지표 평균 + 표준편차 계산
위험 신호 감지: 평균에서 벗어난 데이터 확인
그룹 비교: 약 효과, 치료 효과 검증 등

4. CSV 파일 불러오기
df = pd.read_csv("/content/drive/MyDrive/판다스/train.csv")

print("데이터 크기 (행, 열):", df.shape)
display(df.head())
df.info()
print(df.dtypes)

shape: 데이터 크기 확인
head(): 상위 5행 확인
info(): 컬럼별 타입/결측 여부 확인

오늘의 회고

CSV 파일을 불러와 직접 다뤄보니 실제 데이터 분석의 첫걸음을 체험함
코드로 그래프를 자동 생성하는 것이 신기하고, 시각화가 이해를 돕는다는 점 확인
Pandas 함수/메서드가 아직 익숙하지 않지만 반복 학습으로 내 것으로 만들어야겠다
