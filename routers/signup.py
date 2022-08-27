from fastapi import APIRouter, Depends
import schemas
from sqlalchemy.orm import Session

from logics.database_operation import save_user_in_database
from db.database import SessionLocal

router = APIRouter(
    prefix="/signup",
    tags=["signup"]
)


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post("/email")
async def save_user(form_data: schemas.CreateUser = Depends(schemas.CreateUser.as_form),
                    db: Session = Depends(get_db)):
    response = save_user_in_database(db, form_data)
    if response:
        return {"message": "User Added Successfully"}
    else:
        return {"message": "Username Or Email Already In Use"}
