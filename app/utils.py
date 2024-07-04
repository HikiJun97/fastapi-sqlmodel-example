from fastapi import HTTPException, status
from core.database.models import User


def user_not_found(user: User | None):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
