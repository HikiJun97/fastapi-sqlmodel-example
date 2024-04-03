from pydantic import BaseModel, Field


class UserData(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=30)
    email: str = Field(pattern=r"^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$")
    password: str = Field(min_length=10, max_length=30)


class UserUpdate(BaseModel):
    name: str = Field(default=None)
    email: str = Field(default=None, pattern=r"^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$")
    password: str = Field(default=None, min_length=10, max_length=30)


class UserReplace(BaseModel):
    name: str = Field(min_length=1, max_length=30)
    email: str = Field(pattern=r"^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$")
    password: str = Field(min_length=10, max_length=30)


class UserCreate(BaseModel):
    # "id" column has AUTOINCREMENT property
    name: str = Field(min_length=1, max_length=30)
    email: str = Field(pattern=r"^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$")
    password: str = Field(min_length=10, max_length=30)
