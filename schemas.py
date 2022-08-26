import re
from typing import Optional

from fastapi import HTTPException, Form
from pydantic import BaseModel, Field, validator


class TodoInfo(BaseModel):
    id: int
    title: Optional[str] = Field(max_length=80)
    description: Optional[str] = Field(max_length=100)
    priority: Optional[int] = Field(le=10, ge=1)
    complete: Optional[bool]

    @validator("title")
    def validate_title(cls, value):
        if value is None:
            return None
        if re.findall(r'(?:https?://(?:www\.)?|https:(?://)?)?\w+(?:[-.]\w+)+(?:/[^/\s]+)*$', value):
            raise HTTPException(status_code=420, detail="Url Or Domain Is Not Allowed In Title..")
        return value


class TodoInfoWithoutComplete(BaseModel):
    title: str = Field(max_length=80)
    description: str = Field(max_length=100)
    priority: int = Field(le=10, ge=1)

    class Config:
        schema_extra = {
            "example": {
                "title": "REACT Study",
                "description": "Need To Complete Some REACT Concept",
                "priority": 1
            }
        }

    @validator("title")
    def validate_title(cls, value):
        if re.findall(r'(?:https?://(?:www\.)?|https:(?://)?)?\w+(?:[-.]\w+)+(?:/[^/\s]+)*$', value):
            raise ValueError("Url Or Domain Is Not Allowed In Title..")
        return value


class CreateUser(BaseModel):
    email: str
    username: str
    password: str
    first_name: str
    last_name: str
    is_active: bool

    @validator("email")
    def validate_email(cls, value):
        if re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', value):
            return value
        else:
            raise HTTPException(status_code=419, detail="Email Is Not Valid")

    @classmethod
    def as_form(cls, email: str = Form(...), username: str = Form(...), password: str = Form(...),
                first_name: str = Form(...), last_name: str = Form(...), is_active: bool = Form(...)):
        return cls(email=email, username=username, password=password, first_name=first_name, last_name=last_name,
                   is_active=is_active)

