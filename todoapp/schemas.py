from pydantic import BaseModel, Field


# Schemas
class ToDoRequest(BaseModel):
    task: str


class ToDoResponse(BaseModel):
    id: int
    task: str = Field(max_length=50)
    finished: bool


class TodoUpdate(ToDoRequest):
    task: str | None = Field(max_length=50, default=None)
    finished: bool | None = None


class TodoPut(ToDoRequest):
    task: str = Field(max_length=50)
    finished: bool
