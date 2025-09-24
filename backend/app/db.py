from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

DB_USER = os.getenv("POSTGRES_USER", "fusion")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "fusionpass")
DB_NAME = os.getenv("POSTGRES_DB", "fusiondb")
DB_HOST = os.getenv("POSTGRES_HOST", "fusiondb")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True, 
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# ✅ No asynccontextmanager here
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
