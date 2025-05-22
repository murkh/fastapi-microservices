from enum import IntEnum
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

api = FastAPI()


class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1


class TodoBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=512,
                      description="Name of the Todo")
    description: str = Field(..., description="Description of the Todo")
    priority: Priority = Field(
        default=Priority.LOW, description="Priority of the Todo")


class CreateTodo(TodoBase):
    pass


class Todo(TodoBase):
    id: int = Field(..., description="Unique identifier of the todo")


class UpdateTodo(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=512,
                                description="Name of the Todo")
    description: Optional[str] = Field(None,
                                       description="Description of the Todo")
    priority: Optional[Priority] = Field(None,
                                         description="Priority of the Todo")


all_todos = [
    Todo(id=1, name="Sports", description="Go to gyml", priority=Priority.LOW),
    Todo(id=2, name="Scroll", description="Go to Instagram", priority=Priority.HIGH),
]


@api.get("/")
def index():
    return {"message": "Hello World"}


@api.get("/todos/{id}", response_model=Todo)
def get_todo(id: int) -> Todo:
    for todo in all_todos:
        if todo.id == id:
            return todo
    raise HTTPException(404)


@api.get("/todos", response_model=List[Todo])
def get_todos(first_n: int = None) -> List[Todo]:
    if first_n:
        return all_todos[:first_n]
    return all_todos


@api.post("/todos", response_model=Todo)
def create_todo(todo: CreateTodo) -> Todo:
    id = max(todo.id for todo in all_todos) + 1
    new_todo = Todo(
        id=id,
        name=todo.name,
        description=todo.description,
        priority=todo.priority
    )
    all_todos.append(new_todo)

    return new_todo
