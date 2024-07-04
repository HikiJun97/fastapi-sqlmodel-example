from sqlmodel import Field, SQLModel


rfc_5322_email_regex: str = (
    r"/^[-0-9A-Za-z!#$%&'*+/=?^_`{|}~.]+@[-0-9A-Za-z!#$%&'*+/=?^_`{|}~]+[.]{1}[0-9A-Za-z]/"
)


class UserBase(SQLModel):
    name: str = Field(max_length=30, nullable=False)
    email: str = Field(max_length=320, nullable=False,
                       regex=rfc_5322_email_regex)


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
        max_length=320, nullable=False, regex=rfc_5322_email_regex
    )
    password: str | None = Field(min_length=10, nullable=False)


# class UserReplace(SQLModel):
#     name: str
#     email: str
#     password: str
