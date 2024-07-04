from config import Config
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import SQLModel

DB_URL = f"mysql+aiomysql://{Config.DB_USER}:{Config.DB_PASS}@{
    Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"
print("DATABASE_URL:", DB_URL)
async_engine = create_async_engine(url=DB_URL, echo=False)


async def create_table(async_engine: AsyncEngine):
    async with async_engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
