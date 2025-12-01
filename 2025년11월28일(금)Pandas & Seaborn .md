📌 Pandas & Seaborn Day 3 회고
1. 데이터 필터링

조건에 맞는 행만 선택할 때 == 연산자 사용

예시:

# Outcome이 1인 환자만 선택
diabetes = df[df['Outcome'] == 1]


여러 조건 조합: &(and), |(or), 반드시 괄호 필요

cond = (df['Age'] >= 50) & (df['Outcome'] == 1)

2. 그룹별 분석

groupby()로 특정 기준으로 묶어 통계 계산

# Outcome별 Glucose 평균
df.groupby('Outcome')['Glucose'].mean()


여러 통계를 동시에 계산할 때 agg() 사용

df.groupby('Outcome')['Glucose'].agg(['mean','median','max','min'])

3. pd.cut()으로 연령대 구간 나누기

연속형 숫자를 구간(카테고리)으로 나눌 때 사용

bins = [0, 30, 40, 50, 100]
labels = ['<=30', '31-40', '41-50', '50+']
df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels, right=True)


그룹별 통계 계산

df.groupby(['AgeGroup','Outcome'])['Glucose'].mean()


표 형태로 보기 쉽게 바꾸기: unstack()

4. 그래프 시각화

Matplotlib + Seaborn 사용

4-1. 범주형 vs 숫자형

평균/비율 비교 → barplot

plt.figure(figsize=(5,4))
sns.barplot(
    x='Outcome',
    y='Glucose',
    data=df,
    estimator="mean"
)
plt.title("Outcome별 평균 Glucose")
plt.xlabel("Outcome (0=비당뇨, 1=당뇨)")
plt.ylabel("평균 Glucose")
plt.show()

4-2. 숫자형 단독

값의 분포 확인 → histplot

plt.figure(figsize=(6,4))
sns.histplot(df['Glucose'], bins=20, kde=True)
plt.title("Glucose 분포")
plt.xlabel("Glucose")
plt.ylabel("빈도수")
plt.show()

4-3. 범주형 vs 숫자형 분포 비교

중앙값, 사분위수, 이상치 확인 → boxplot

plt.figure(figsize=(5,4))
sns.boxplot(x="Outcome", y="BMI", data=df)
plt.title("Outcome별 BMI 분포")
plt.xlabel("Outcome (0=비당뇨, 1=당뇨)")
plt.ylabel("BMI")
plt.show()

4-4. 숫자형 vs 숫자형

두 변수 관계 확인 → scatterplot

plt.figure(figsize=(6,5))
sns.scatterplot(
    x="BMI",
    y="Glucose",
    hue="Outcome",
    data=df,
    alpha=0.7
)
plt.title("BMI vs Glucose (Outcome별)")
plt.xlabel("BMI")
plt.ylabel("Glucose")
plt.show()

4-5. 범주별 개수 비교

빈도 확인 → countplot

plt.figure(figsize=(5,4))
sns.countplot(x="Outcome", data=df)
plt.title("Outcome별 환자 수")
plt.xlabel("Outcome (0=비당뇨, 1=당뇨)")
plt.ylabel("환자 수")
plt.show()

5. 상관분석

두 변수의 함께 움직이는 정도를 수치화

df.corr()로 상관행렬 생성

corr_matrix = df.corr()
corr_with_outcome = corr_matrix["Outcome"].sort_values(ascending=False)


상관계수 해석

+1 : 완전 양의 상관

0 : 상관 없음

-1 : 완전 음의 상관

주의: 상관 = 인과 아님

Seaborn으로 히트맵 시각화

plt.figure(figsize=(8,6))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("당뇨 데이터 상관계수 히트맵")
plt.show()

6. 오늘 회고

다양한 그래프를 통해 데이터를 시각화하는 방법 학습

어떤 상황에 어떤 그래프를 선택해야 할지 판단하는 능력이 아직 부족함

연습을 통해 범주형 vs 숫자형, 숫자형 vs 숫자형 등 상황별 그래프 선택 능력을 키워야 함

Seaborn의 편리함과 직관성을 체감할 수 있었음
