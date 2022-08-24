import re
from typing import Optional

from fastapi import FastAPI, Depends, Request
from pydantic import BaseModel, validator, Field
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import database_models
from database import engine, SessionLocal


class Todo(BaseModel):
    title: str = Field(max_length=80)
    description: str = Field(max_length=100)
    priority: int = Field(le=10, ge=1)
    complete: Optional[bool]

    @validator("title")
    def validate_title(cls, value):
        regex = r'^((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?$'
        if re.match(regex, value):
            raise ValueError("Url Found In Your Title.. Not Allowed..")
        return value


class DataBaseTableException(Exception):
    def __init__(self):
        pass


app = FastAPI()

database_models.Base.metadata.create_all(engine)


@app.exception_handler(DataBaseTableException)
async def database_exception_handler(request: Request, exception: DataBaseTableException):
    database_models.Base.metadata.create_all(engine)
    return JSONResponse(
        status_code=418,
        content={"message": "Database Not Available"}
    )


@app.get("/")
async def root():
    return {"message": "Welcome To Heaven"}


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/db")
async def get_all_todo(db: Session = Depends(get_db)):
    try:
        todo_lists = db.query(database_models.Todo).all()
        if not todo_lists:
            return {"message": "No Data Found On Database"}
        return todo_lists
    except Exception:
        raise DataBaseTableException


@app.post("/save-todo")
async def save_todo(todo: Todo, db: Session = Depends(get_db)):
    todo_model = database_models.Todo()
    todo_model.Title = todo.title
    todo_model.Description = todo.description
    todo_model.Priority = todo.priority
    db.add(todo_model)
    db.commit()
    return {"data": [todo.title, todo.description, todo.priority, todo.complete]}
