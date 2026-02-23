from fastapi import FastAPI

app = FastAPI()


# HTTP 요청 -> '게시물' 을 '생성' 하고 싶다.
# GET /users
# DELETE/ comments/1

# 서버에 GET / 요청이 들어오면, root_handler를 실행한다.

from fastapi import FastAPI

app = FastAPI()

# 1. 데이터를 밖으로 빼서 어디서든 접근 가능하게 합니다.
users = [
    {"id": 1, "name": "alex"},
    {"id": 2, "name": "tom"},
    {"id": 3, "name": "hank"}
]

def hello_world():
    return {"msg": "hello_world"}

# 전체 사용자 리스트를 반환하는 함수
def get_all_users():
    return users

@app.get("/hello")
def root_handler():
    return hello_world()

# 전체 사용자 조회 API
@app.get("/users")
def get_users_handlers():
    return get_all_users()

# {user_id}번 사용자 조회 API
# Path(경로) + Parameter(매개변수) -> 동적으로 바뀌는 값을 한 번에 처리
# Path Parameter에 type hint 추가하면 -> 명시한 타입에 맞는지 검사 & 보장
@app.get("/users/{user_id}")
def get_user_handler(user_id: int):
    return users[user_id - 1]

# "1" -> 1