from pydantic import BaseModel


class Todo(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    complete: bool


class TodoRequest(BaseModel):
    title: str
    description: str
    priority: int
    complete: bool
