from typing import List, Optional, Union, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
from db.database import SessionLocal
from logics.database_operation import get_all_todo_list, save_todo_in_database, get_todo_by_id_from_database, \
    update_todo_status_in_database
from routers.auth import get_current_user_from_jwt_token, unauthorized_token_exception

router = APIRouter(
    prefix="/todo",
    tags=["todo"]
)


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/")
async def root():
    return {"message": "Welcome To Heaven"}


@router.get("/db", response_model=Union[Dict[str, List[schemas.TodoInfo]], Dict[str, schemas.TodoInfo], Dict[str, str]])
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
        raise HTTPException(status_code=400, detail="No Database Found")


@router.post("/save")
async def save_todo(todo: schemas.TodoInfoWithoutComplete, db: Session = Depends(get_db),
                    user: Dict[str, Union[str, int]] = Depends(get_current_user_from_jwt_token)):
    if user:
        save_todo_in_database(db, todo, user["id"])
        return {"message": "Todo Created Successfully"}
    raise unauthorized_token_exception()


@router.put("/update")
async def update_todo(todo: schemas.TodoInfo = Depends(), db: Session = Depends(get_db),
                      user: Dict[str, Union[str, int]] = Depends(get_current_user_from_jwt_token)):
    # print(todo.dict())
    if user:
        update_success = update_todo_status_in_database(db, todo, user["id"])
        if not update_success:
            raise HTTPException(status_code=420, detail="Update Failed.. Check Url Params")
        return {"message": "Successfully Update Data"}
    else:
        raise unauthorized_token_exception()
