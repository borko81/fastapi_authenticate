from pydantic import BaseModel


"""
    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False)
    email = Column(String(32), nullable=False, unique=True)
    password = Column(String(52), nullable=False)
    active = Column(Boolean, default=True)
"""


class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    active: bool | None = None


class UserListSchema(UserCreateSchema):
    id: int
    active: bool

    class Config:
        orm_mode = True
