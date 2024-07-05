import os
import secrets
from typing import Annotated

from config import Config
from core.database.engine import async_engine
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader, HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession


async def get_async_session():
    async_session = async_sessionmaker(
        expire_on_commit=False,
        autoflush=False,
        bind=async_engine,
        class_=AsyncSession,
    )

    async with async_session.begin() as session:
        yield session


def auth_api_key(
    api_key: str = Security(APIKeyHeader(name="Authorization")),
):
    if api_key != Config.API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
