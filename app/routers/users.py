from typing import Annotated, List, Sequence, Dict, cast
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, Path, Query, HTTPException, status

from core.database.models import User, UserPublic, UserCreate, UserUpdate, UserReplace
from dependencies import get_async_session
from password_utils import PasswordUtils

router = APIRouter(prefix="/users", tags=["users"])

HASHED_PASSWORD = "hashed_password"
PASSWORD = "password"


@router.get("", response_model=List[UserPublic])
async def get_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    id: Annotated[int | None, Query(ge=1)] = None,
    name: Annotated[str | None, Query()] = None,
    email: Annotated[str | None, Query()] = None,
    offset: Annotated[int, Query(ge=0, le=100)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    select_query = select(User).offset(offset).limit(limit)
    if id is not None:
        select_query = select_query.where(User.id == id)
    if name is not None:
        select_query = select_query.where(User.name == name)
    if email is not None:
        select_query = select_query.where(User.email == email)

    users: Sequence[User] = (await session.exec(select_query)).all()
    return users


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def create_user(
    session: Annotated[AsyncSession, Depends(get_async_session)], user: UserCreate
):
    hashed_password = PasswordUtils.hash(user.password)
    extra_data = {HASHED_PASSWORD: hashed_password}
    db_user = User.model_validate(user, update=extra_data)
    session.add(db_user)
    # Commit is necessary for validating response model as "id" is None before commit
    await session.commit()
    print(db_user)
    return db_user


@router.patch("/{user_id}", response_model=UserPublic)
async def update_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user: UserUpdate,
    user_id: Annotated[int, Path(title="The ID of user to update")],
):
    db_user = await session.get(User, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user_data = user.model_dump(exclude_unset=True)
    extra_data = dict()
    if password := user_data[PASSWORD]:
        hashed_password = PasswordUtils.hash(password)
        extra_data[HASHED_PASSWORD] = hashed_password

    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    return db_user


@router.delete("/{user_id}", response_model=Dict[str, UserPublic])
async def delete_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_id: Annotated[int, Path(title="The ID of user to delete")],
):
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    await session.delete(user)
    return {"deleted user": user}


@router.put("/{user_id}", response_model=UserPublic)
async def replace_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user: UserReplace,
    user_id: int = Path(title="The ID of user to replace/create"),
):
    db_user = await session.get(User, user_id)
    hashed_password = PasswordUtils.hash(user.password)
    extra_data = {HASHED_PASSWORD: hashed_password}

    # If user exists, replace it, else create a new user
    if db_user is None:
        db_user = User.model_validate(user, update=extra_data)
    else:
        user_data = user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(user_data, update=extra_data)

    session.add(db_user)
    await session.commit()
    return db_user
