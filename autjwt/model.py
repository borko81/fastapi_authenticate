from pydantic import BaseModel, Field, EmailStr


class PostSchema(BaseModel):
    title: str = Field(...)
    content: str = Field(...)

    class Config:
        schema_extra = {
            "example": {"title": "Security tab", "content": "Security content"}
        }


class PostsShow(PostSchema):
    id: int = Field(default=None)


class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Boris St",
                "email": "boris@abv.bg",
                "password": "password",
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {"example": {"email": "boris@abv.bg", "password": "password"}}
