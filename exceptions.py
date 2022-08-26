from fastapi import HTTPException
from fastapi import status


def unauthorized_token_exception():
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Bearer Token",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return exception


def authenticate_credentials_exceptions():
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Username Or password Doesn't Match",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return exception
