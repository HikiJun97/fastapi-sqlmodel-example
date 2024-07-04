from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    name: str = Field(max_length=30, nullable=False)
    email: str = Field(
        max_length=320,
        nullable=False,
        regex=r"^(?=.{1,64}@.{1,255}$)(?=.{6,320}$)[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
    )


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
        max_length=320,
        nullable=False,
        regex=r"^(?=.{1,64}@.{1,255}$)(?=.{6,320}$)[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
    )
    password: str | None = Field(min_length=10, nullable=False)


# class UserReplace(SQLModel):
#     name: str
#     email: str
#     password: str
