import asyncio
import os

from dotenv import load_dotenv
from sqlalchemy import Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncEngine, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

load_dotenv()

DATABASE_URL = f"mysql+aiomysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DATABASE')}"
print("DATABASE_URL:", DATABASE_URL)
async_engine = create_async_engine(DATABASE_URL, echo=True)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(30), nullable=False)


async def create_table(async_engine: AsyncEngine):
    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


async def async_main():
    async_engine = create_async_engine(DATABASE_URL)
    await create_table(async_engine=async_engine)
    await async_engine.dispose()


asyncio.run(async_main())
