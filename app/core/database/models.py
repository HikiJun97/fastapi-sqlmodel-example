from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    name: str = Field(max_length=30, nullable=False)
    email: str = Field(max_length=50, nullable=False)
    password: str = Field(max_length=30, nullable=False)
