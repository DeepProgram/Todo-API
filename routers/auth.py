from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from db import database_models
from exceptions import authenticate_credentials_exceptions, unauthorized_token_exception
from logics.bcrypt_process import verify_password
from logics.json_web_token import create_jwt_access_token, oauth2_bearer, SECRET_KEY, ALGORITHM
from db.database import SessionLocal

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def authenticate_user(user_name: str, password: str, db: Session):
    query_result = db.query(database_models.User).filter_by(username=user_name).first()
    if query_result:
        if verify_password(password, query_result.hashed_password):
            return query_result
    return None


@router.post("/token")
async def get_access_token_by_login(form_data: OAuth2PasswordRequestForm = Depends(),
                                    db: Session = Depends(get_db)):
    authenticated_user = authenticate_user(form_data.username, form_data.password, db)
    if authenticated_user:
        token_expires = timedelta(minutes=20)
        token = create_jwt_access_token(authenticated_user.username, authenticated_user.id, token_expires)
        return {"token": token}
    raise authenticate_credentials_exceptions()


def get_current_user_from_jwt_token(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise unauthorized_token_exception()
        return {"username": username, "id": user_id}
    except JWTError:
        raise unauthorized_token_exception()
