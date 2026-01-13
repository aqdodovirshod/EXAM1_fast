from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./tasks.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine)

async def get_session():
    async with async_session() as session:
        yield session

class BaseModel(DeclarativeBase):
    pass