# 비동기 SQLALchemy 설정 파일
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DATABASE_URL = "sqlite+aiosqlite:///./test.db"  # SQLite 예시, 다른 DB를 사용할 경우 URL 형식에 맞게 변경

async_engine = create_async_engine(DATABASE_URL)

AsyncSessionFactory = sessionmaker(
    bind= async_engine, # 엔진을 연결
    # 기본 옵션
    autocommit=False, # 자동 커밋 비활성화
    autoflush=False, # 자동 플러시 비활성화
    expire_on_commit=False, # 커밋 후 객체의 상태 유지
    class_=AsyncSession # 비동기 세션 클래스 지정
)

async def get_async_session():
    session = AsyncSessionFactory() # 비동기 세션 생성
    try:
        yield session # 세션 객체를 반환하면서 함수 일시 중지
    finally:
        # 세션을 종료하면서 네트워크를 사용하기 때문에 await 
        await session.close() # 세션 닫기 (비동기)