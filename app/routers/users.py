from typing import Annotated, List, Sequence
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, Path, Query, status

from core.database.models import User, UserPublic, UserCreate, UserUpdate
from dependencies import get_async_session
from password_utils import PasswordUtils
from utils import user_not_found

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
    hashed_password = PasswordUtils.hash_password(user.password)
    db_user = User.model_validate(
        user, update={HASHED_PASSWORD: hashed_password})
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
    db_user = user_not_found(db_user)
    user_data = user.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(
        user_data,
        update=(
            {HASHED_PASSWORD: PasswordUtils.hash_password(user_data[PASSWORD])}
            if PASSWORD in user_data
            else {}
        ),
    )
    session.add(db_user)
    return db_user


@router.delete("/{user_id}")
async def delete_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_id: Annotated[int, Path(title="The ID of user to delete")],
):
    user = await session.get(User, user_id)
    user = user_not_found(user)
    await session.delete(user)
    return {"deleted user": user}


# @router.put("/{user_id}")
# async def replace_user(
#     session: Annotated[AsyncSession, Depends(get_async_session)],
#     user_data: UserReplace,
#     user_id: int = Path(title="The ID of user to update"),
# ):
#     # user = (await session.scalars(select(User).where(User.id == user_id))).one()
#     user = select(User).where(User.id == user_id)
#     db_user = await session.get(User, user_id)
#
#     for key, value in user_data.model_dump().items():
#         setattr(user, key, value)
#     return {"msg": "user replaced"}
