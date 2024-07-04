from sqlmodel import Field, SQLModel


rfc_5322_email_regex: str = (
    r"""^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"""
)


class UserBase(SQLModel):
    name: str = Field(max_length=30, nullable=False)
    email: str = Field(max_length=320, nullable=False, pattern=rfc_5322_email_regex)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field()


class UserPublic(UserBase):
    id: int


class UserCreate(UserBase):
    password: str = Field(min_length=10, nullable=False)


class UserUpdate(SQLModel):
    name: str | None = Field(max_length=30, nullable=False)
    email: str | None = Field(
        max_length=320, nullable=False, pattern=rfc_5322_email_regex
    )
    password: str | None = Field(min_length=10, nullable=False)


class UserReplace(UserCreate):
    pass


if __name__ == "__main__":
    import re

    try:
        user = UserBase(name="John", email="string")
        print(user)
    except Exception as e:
        print("Error:")
        print(e)
