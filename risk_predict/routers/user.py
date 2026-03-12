from fastapi import Depends, Body, HTTPException, status, APIRouter
from sqlalchemy import select

from auth.password import hash_password, verify_password
from auth.jwt import create_access_token, verify_user
from database.connection import get_session
from database.orm import User, HealthProfile
from request import SignUpRequest, LogInRequest, HealthProfileCreateRequest
from response import UserResponse, LogInResponse, HealthProfileResponse

router = APIRouter(tags=["User"])

@router.post(
        "/users",
        summary="회원가입 API",
        status_code=status.HTTP_201_CREATED,
        response_model=UserResponse,
)
async def signup_handler(
    body: SignUpRequest = Body(...),
    session = Depends(get_session),
):
    # [1] email 중복 검사
    stmt = select(User).where(User.email == body.email)
    user = await session.scalar(stmt)

    if user:
        raise HTTPException(status_code=409, detail="email already exists")
    
    # [2] 새로운 유저 데이터 추가 & 비밀번호 해싱(hashing)
    new_user = User(
        email=body.email,
        password_hash=hash_password(plain_password=body.password),
    )

    # [3] 데이터 저장
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user) # 데이터베이스에서 id랑 created_at 읽어옴

    return new_user

@router.delete(
        "/users",
        summary="회원탈퇴 API",
        status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_handler(
    user_id: int = Depends(verify_user),
    session = Depends(get_session),
):
    stmt = select(User).where(User.id == user_id)
    user = await session.scalar(stmt)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    
    # [2] DB에서 삭제
    # HealthProfile 삭제
    # HealthRiskPrediction 삭제

    # await session.delete(user)
    # await session.commit()
    
    # Soft Delete: 실제로 데이터를 삭제하지 않고, 개인정보를 마스킹
    user.soft_delete()
    await session.commit()



@router.post(
    "/users/login",
    summary="로그인 API",
    status_code=status.HTTP_200_OK,
    response_model=LogInResponse,
)
async def login_handler(
    body: LogInRequest = Body(...),
    session = Depends(get_session),
):
    # [1] email로 사용자 조회
    stmt = select(User).where(User.email == body.email)
    user: User | None = await session.scalar(stmt)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")
    
    # [2] body.passhash & user.password_hash 비교
    verified = verify_password(plain_password=body.password, password_hash=user.password_hash)
    if not verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")
    
    # [3] JWT 발급 (이 부분을 수정하세요)
    access_token: str = create_access_token(user_id=user.id)

    return {"access_token": access_token}

# 프로필 변경
# 1) 프로필 처음 생성 -> 생성
# 2) 프로필 변경 -> 수정

@router.post(
    "/health-profiles",
    summary="건강 프로필 생성 API",
    status_code=status.HTTP_201_CREATED,
    response_model=HealthProfileResponse
)
async def create_health_profile_handler(
    user_id: int = Depends(verify_user),
    body: HealthProfileCreateRequest = Body(...),
    session = Depends(get_session),
):
    stmt = select(HealthProfile).where(HealthProfile.user_id == user_id)
    existing = await session.scalar(stmt)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="health profile already exists")

    # [1] HealthProfile 객체 생성
    profile_data = body.model_dump()
    new_profile = HealthProfile(user_id=user_id, **profile_data)

    # [2] DB 저장
    session.add(new_profile)
    await session.commit()
    await session.refresh(new_profile)
    return new_profile


