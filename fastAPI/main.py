from fastapi import FastAPI, Path, Query, Body, status, HTTPException
from schema import UserSignUpRequest, UserResponse, UserUpdateRequest

app = FastAPI()


# HTTP 요청 -> '게시물' 을 '생성' 하고 싶다.
# GET /users
# DELETE/ comments/1

# 서버에 GET / 요청이 들어오면, root_handler를 실행한다.

from fastapi import FastAPI

app = FastAPI()

# 1. 데이터를 밖으로 빼서 어디서든 접근 가능하게 합니다.
users = [
    {"id": 1, "name": "alex", "age": 20},
    {"id": 2, "name": "tom", "age": 30},
    {"id": 3, "name": "hank", "age": 40},
    {"id": 4, "name": "jane", "age": 50},
    {"id": 5, "name": "mike", "age": 60},
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
@app.get("/users",
        response_model=list[UserResponse], # 응답은 UserResponse 형태의 리스트로 반환하겠다.
        status_code=status.HTTP_200_OK
        )
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

@app.get("/users/search",
        response_model=list[UserResponse],
        status_code=status.HTTP_200_OK
        )
def search_user_handler(
    name: str = Query(..., min_length=2), # default=... 이랑 같은 의미
    age: int = Query(None, ge=1) # 선택적(optional)
):
    #name이라는 key로 넘어오는 Query Parameter 값을 사용하겠다.
    return {"id": 0, "name": name, "age": age}

# ?field=id => id값만 반환
# ?field=name => name 값만 반환
@app.get("/users/{user_id}",
        response_model=UserResponse,
        status_code=status.HTTP_200_OK
        )
def get_user_handler(
    user_id: int = Path(..., ge=1, description="user_id는 1이상"),
    field: str = Query(None, description="출력할 필드 선택(id 또는 name)"),
):
    if user_id > len(users):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 사용자의 ID입니다.")
    
    user = users[user_id -1]

    if field in ("id", "name"):
        return {field: user[field]}
    return user


##################################################################################

#FastAPI의 핵심 동작이 Type Hints 위에 설계되어 있음

# 회원가입 API
# 회원가입에 필요한 데이터
# 휴대폰 번호 -> 토스
# 소셜 로그인 ->
# 하나의 계정 -> 두 가지 인증 (비밀번호 기반 / 간편 로그인)
@app.post(
        "/users/sign-up", 
        status_code=status.HTTP_201_CREATED,
        response_model=UserResponse # 응답은 UserResponse 형태로 반환하겠다.
        )
def sign_up_handler(body: UserSignUpRequest):
    # 핸들러 함수에 선언한 매개 변수의 타입힌트가 BaseModel을 상속 받은 경우, 요청 본문에서 가져옴
    # 데이터 가져오면서, 타입힌트에 선언한 데이터 구조와 맞는지 검사

    # body = UserSignUpRequest(name=..., age=...)
    # body 데이터가 문제 없으면 -> 핸들러 함수로 전달
    # body 데이터가 문제 있으면 -> 422 에러 발생

    new_user = {
        "id": len(users) + 1,
        "name": body.name,
        "age": body.age
    }
    users.append(new_user)
    # name, age만 응답 -> response_model이랑 안 맞음 -> FastAPI ResponseValidationError 발생

    return {"name": body.name, "age": body.age}

################################################################################################

# 코딩할 때 Tips
'''
1. 입력(ex 데이터 전처리)
2. 연산
3. 출력
'''

# 사용자 정보 수정 API
# PUT -> {name, age} 한 번에 교체
# PATCH -> {name} 또는 {age} 일부분만 교체
@app.patch(
        "/users/{user_id}",
        status_code=status.HTTP_200_OK,
        response_model=UserResponse
        )
def update_user_handler(
    user_id: int = Path(..., ge=1),
    body: UserUpdateRequest = Body(...)
    
):
    # 1) user_id 유효성 검사
    if user_id > len(users):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 사용자의 ID입니다.")
    
    if body.name is None and body.age is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="수정할 정보가 없습니다.")
    
    # 2) 사용자 조회
    user = users[user_id - 1]

    # 3) 사용자 정보 수정

    if body.name is not None:
        user["name"] = body.name

    if body.age is not None:
        user["age"] = body.age

    # 4) 응답 반환
    return user