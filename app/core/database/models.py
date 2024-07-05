from sqlmodel import Field, SQLModel


rfc_5322_email_regex: str = (
    r"""^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"""
)


class UserBase(SQLModel):
    name: str = Field(max_length=30, nullable=False)
    # Issue with pattern argument, regex arg doesn't work
    email: str = Field(max_length=320, nullable=False)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field()


class UserPublic(UserBase):
    id: int


class UserCreate(UserBase):
    password: str = Field(min_length=10, nullable=False)


class UserUpdate(SQLModel):
    name: str | None = Field(max_length=30, nullable=False)
    # Issue with pattern argument, regex arg doesn't work
    email: str | None = Field(max_length=320, nullable=False)
    password: str | None = Field(min_length=10, nullable=False)


class UserReplace(UserCreate):
    pass
