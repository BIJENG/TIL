from fastapi import FastAPI, Path, Query

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

# 회원 검색 API
# @app.get("/users/search")
# def search_user_handler():
#     return {"msg": "Welcome"}

# {user_id}번 사용자 조회 API -> 단일
# Path(경로) + Parameter(매개변수) -> 동적으로 바뀌는 값을 한 번에 처리
# Path Parameter에 type hint 추가하면 -> 명시한 타입에 맞는지 검사 & 보장

# @app.get("/users/{user_id}")
# def get_user_handler(user_id: int):
#     # 1, 2, 3, 4
#     # 0, -1, -2, ...
#     if user_id < 1:
#         return {"msg": "잘못된 user_id 값입니다."}
#     return users[user_id - 1]

# @app.get("/users/{user_id}")
# def get_user_handler(
#     user_id: int = Path(..., ge=1, description="user_id는 1이상")
# ):
    # gt : 초과
    # ge : 이상
    # lt : 미만
    # le : 이하
    # max_digits: 최대 자리수 000000
    # return users[user_id - 1]

# GET /items/{item_name}
# item_name: str & 최대 글자수(max_length = 6)
# 응답 형식: {"item_name": ...}
items = [
    {"id": 1, "name": "apple"},
    {"id": 2, "name": "banana"},
    {"id": 3, "name": "cherry"},
]

@app.get("/items")
def get_item_handlers():
    return items

@app.get("/items/{item_name}")
def get_item_handler(
    item_name: str = Path(..., max_length=6, description="item_name는 문자형식이고 최대6자까지 가능")
):
    return {"item_name": item_name}


# Query Parameter
# google.com/search?q=...
# Path 뒤에 붙어서 key = value 형태로 오는 값
# 필터링, 정렬, 검색, 페이지네이션 등 데이터를 조회시 부가조건을 명시

@app.get("/users/search")
def search_user_handler(
    name: str = Query(..., min_length=2), # default=... 이랑 같은 의미
    age: int = Query(None, ge=1) # 선택적(optional)
):
    #name이라는 key로 넘어오는 Query Parameter 값을 사용하겠다.
    return {"name": name, "age": age}

# ?field=id => id값만 반환
# ?field=name => name 값만 반환
@app.get("/users/{user_id}")
def get_user_handler(
    user_id: int = Path(..., ge=1, description="user_id는 1이상"),
    field: str = Query(None, description="출력할 필드 선택(id 또는 name)"),
):
    user = users[user_id -1]

    if field in ("id", "name"):
        return {field: user[field]}
    return user


##################################################################################

#FastAPI의 핵심 동작이 Type Hints 위에 설계되어 있음