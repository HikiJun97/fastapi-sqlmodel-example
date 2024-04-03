import re
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates
from sqlalchemy.ext.asyncio import AsyncAttrs


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

    @validates("name")
    def validate_name(self, key, address):
        if len(address) == 0:
            raise ValueError(f"{key} cannot be empty")
        return address

    @validates("email")
    def validate_email(self, key, address):
        if not address:
            raise ValueError(f"{key} cannot be empty")
        if not re.match(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", address
        ):
            raise ValueError(f"{key} must be a valid email address")
        return address

    @validates("password")
    def validate_password(self, key, address):
        if len(address) < 10:
            raise ValueError(f"{key} must be longer than 10 letters")
        return address
