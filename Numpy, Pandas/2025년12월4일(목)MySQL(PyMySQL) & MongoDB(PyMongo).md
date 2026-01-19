📘 Python + MySQL(PyMySQL) & MongoDB(PyMongo) 정리
📌 1. PyMySQL이란?

파이썬에서 MySQL 데이터베이스와 연결할 수 있게 해주는 라이브러리.

✔ 설치
pip install pymysql

✔ 사용
import pymysql

📌 2. MySQL 연결 기본 흐름
단계	기능
connect()	DB 연결
cursor()	SQL 실행할 준비
execute()	SQL 쿼리 실행
commit()	INSERT/UPDATE 후 저장
fetchone()/fetchall()	SELECT 결과 가져오기
📌 3. Aiven에서 MySQL 무료 서버 사용하기

Aiven 회원가입

프로젝트 생성

Create service → MySQL → Free tier 선택

Host, User, Password, Port, DB명 확인

✔ Python에서 연결
conn = pymysql.connect(
    host="호스트",
    user="avnadmin",
    password="비번",
    db="defaultdb",
    port=포트번호,
    charset='utf8'
)

cursor = conn.cursor()
print("Connected MySQL!")

📌 4. 테이블 생성 예시
tables_to_create = {
    'patients': """
    CREATE TABLE IF NOT EXISTS patients (
        patient_id INT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        gender VARCHAR(10),
        birth_date DATE
    )""",

    'visits': """
    CREATE TABLE IF NOT EXISTS visits (
        visit_id INT PRIMARY KEY,
        patient_id INT NOT NULL,
        visit_date DATE,
        reason VARCHAR(255),
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
    )"""
}

for name, sql in tables_to_create.items():
    try:
        cursor.execute(sql)
        conn.commit()
        print(f"{name} 생성 완료")
    except pymysql.Error as e:
        print(f"에러 발생: {e}")
        conn.rollback()

📌 5. 데이터 INSERT / SELECT 기본 구조
✔ INSERT (반드시 commit 필요!!)
with conn.cursor() as cur:
    sql = "INSERT INTO patients VALUES (%s, %s, %s, %s)"
    cur.execute(sql, (1, "홍길동", "M", "1990-01-01"))
    conn.commit()

✔ SELECT + fetchall()
with conn.cursor() as cur:
    sql = "SELECT * FROM patients WHERE patient_id = %s"
    cur.execute(sql, (1,))
    rows = cur.fetchall()
    print(rows)

📌 6. %s 플레이스홀더

SQL 값을 안전하게 넣기 위한 문법

SQL Injection 방지

절대 f-string으로 직접 값을 넣지 않음

📌 7. 긴 SQL문은 변수로 관리
sql_1 = """
SELECT p.name, v.visit_date, v.reason
FROM visits v
JOIN patients p ON v.patient_id = p.patient_id
ORDER BY v.visit_date DESC
LIMIT 5;
"""

with conn.cursor() as cur:
    cur.execute(sql_1)
    result = cur.fetchall()

🟩 8. MongoDB / NoSQL 개념
✔ RDBMS vs NoSQL
RDBMS	NoSQL
고정된 스키마	스키마 자유
JOIN 많음	문서(document) 구조
수직 확장	수평 확장 (scale-out)
정형 데이터	비정형/반정형 가능
구조 변경 어려움	구조 변경 쉬움
📌 9. MongoDB 기본 구조
MongoDB	RDBMS
Database	Database
Collection	Table
Document(JSON/BSON)	Row
Field	Column
📌 10. BSON vs JSON
JSON	BSON
텍스트 기반	바이너리 기반
가볍다	빠르고 효율적
날짜 타입 없음	날짜 타입 지원
문자열 중심	이진(binary) 데이터 지원

MongoDB는 내부적으로 BSON 사용.

📌 11. MongoDB(PyMongo) 사용 절차

MongoDB Atlas 회원가입

Project 생성

Cluster 생성

샘플 데이터 Load

Username/Password 생성

Network Access → IP 0.0.0.0/0 추가 (외부 접속 허용)

"Connect → Drivers"에서 Python 코드 복사

Colab 또는 VSCode에 붙여넣기
