from typing import List, Optional, Union, Dict
from collections import Counter
from fastapi import FastAPI, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from db import database_models
from db.database import engine, SessionLocal
import schemas
from db.database_operation import get_all_todo_list, save_todo_in_database, get_todo_by_id_from_database, \
    update_todo_status_in_database
from auth.auth import get_current_user_from_jwt_token, unauthorized_token_exception


class DataBaseTableException(Exception):
    def __init__(self):
        pass


app = FastAPI()

database_models.Base.metadata.create_all(engine)


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


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


@app.get("/db", response_model=Union[Dict[str, List[schemas.TodoInfo]], Dict[str, schemas.TodoInfo], Dict[str, str]])
async def get_todo(_id: Optional[int] = None, db: Session = Depends(get_db),
                   user: Dict[str, Union[str, int]] = Depends(get_current_user_from_jwt_token)):
    if not user:
        raise unauthorized_token_exception()
    if _id:
        todo = get_todo_by_id_from_database(db, _id, user["id"])
        if todo:
            return {"data": todo}
        else:
            raise HTTPException(status_code=422, detail="No Todo Found On This ID")
    try:
        todo_lists = get_all_todo_list(db, user["id"])
        if not todo_lists:
            raise HTTPException(status_code=421, detail="No Data Found On Database")
        return {"data": todo_lists}
    except Exception:
        raise DataBaseTableException


@app.post("/save-todo")
async def save_todo(todo: schemas.TodoInfoWithoutComplete, db: Session = Depends(get_db),
                    user: Dict[str, Union[str,int]] = Depends(get_current_user_from_jwt_token)):
    if user:
        save_todo_in_database(db, todo, user["id"])
        return {"message": "Todo Created Successfully"}
    raise unauthorized_token_exception()


@app.put("/update")
async def update_todo(todo: schemas.TodoInfo = Depends(), db: Session = Depends(get_db),
                      user: Dict[str, Union[str, int]] = Depends(get_current_user_from_jwt_token)):
    if user:
        processed_todo_params = {}
        for keys, value in dict(todo).items():
            if value is not None:
                processed_todo_params[keys] = value
        if Counter(processed_todo_params.values())[None] == 4:
            raise HTTPException(status_code=419, detail="No Query Is Passed In The Parameter")
        else:
            update_success = update_todo_status_in_database(db, todo.id, processed_todo_params, user["id"])
            if not update_success:
                raise HTTPException(status_code=420, detail="Update Failed")
            return {
                "message": "Successfully Update Data",
                "data": processed_todo_params
            }
    else:
        raise unauthorized_token_exception()



