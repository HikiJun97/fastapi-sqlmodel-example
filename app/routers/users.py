from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, Query, Path, status
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schemas import UserUpdate, UserCreate, UserReplace
from app.core.database.models import User
from app.dependencies import get_async_session


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_user(
    id: Annotated[int, Query(title="Query user through user id")],
    session: AsyncSession = Depends(get_async_session),
):
    try:
        users = (await session.scalars(select(User).where(User.id == id))).all()
        return users
    except:
        raise


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        session.add(
            User(
                name=user_data.name, email=user_data.email, password=user_data.password
            )
        )
        return {"msg": "new user inserted"}

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("/{user_id}")
async def update_user(
    user_data: UserUpdate,
    user_id: int = Path(title="The ID of user to update"),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        user = (await session.scalars(select(User).where(User.id == user_id))).first()
        for key, value in user_data.model_dump(exclude_unset=True).items():
            # As it's the PATCH method, configure dictionary from BaseModel with non-default key-value pairs through "exclude_unset=True" option.
            setattr(user, key, value)
        return {"msg": "user updated"}
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/{user_id}")
async def replace_user(
    user_data: UserReplace,
    user_id: int = Path(title="The ID of user to update"),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        user = (await session.scalars(select(User).where(User.id == user_id))).first()
        for key, value in user_data.model_dump().items():
            setattr(user, key, value)
        return {"msg": "user replaced"}
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int = Path(title="The ID of user to update"),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        await session.execute(delete(User).where(User.id == user_id))
        return {"msg": "user deleted"}
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
