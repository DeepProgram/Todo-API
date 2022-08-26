from typing import Dict
from sqlalchemy.orm import Session
from sqlalchemy import exists
from db import database_models
import schemas
from fastapi import Form
from auth.bcrypt_process import get_password_hash


def get_all_todo_list(db: Session, user_id: int):
    todo_list = list(map(
        lambda x: {"id": x.id, "title": x.title, "description": x.description, "priority": x.priority, "complete": x.complete},
        db.query(database_models.Todo).filter_by(owner_id=user_id).all()))
    return todo_list


def save_todo_in_database(db: Session, todo_info: schemas.TodoInfoWithoutComplete,
                          user_id: int):
    todo_model = database_models.Todo()
    todo_model.title = todo_info.title
    todo_model.description = todo_info.description
    todo_model.priority = todo_info.priority
    todo_model.owner_id = user_id
    db.add(todo_model)
    db.commit()


def get_todo_by_id_from_database(db: Session, _id, user_id: int):
    todo = db.query(database_models.Todo).filter_by(id=_id, owner_id=user_id).first()
    if todo:
        return {"title": todo.title, "description": todo.description, "priority": todo.priority,
                "complete": todo.complete}
    else:
        return None


def update_todo_status_in_database(db: Session, _id: int, query_params: Dict[str, str], user_id: int):
    update_status = db.query(database_models.Todo).filter_by(id=_id, owner_id=user_id).update(
        query_params
    )
    db.commit()
    return update_status


def is_already_exist_in_database(db: Session, search_colum, search_value):
    if search_colum == "username":
        return db.query(exists().where(database_models.User.username == search_value)).scalar()
    elif search_colum == "email":
        return db.query(exists().where(database_models.User.email == search_value)).scalar()


def save_user_in_database(db: Session, form_data: Form):
    user_table_row = database_models.User()
    if is_already_exist_in_database(db, "email", form_data.email):
        return False
    user_table_row.email = form_data.email
    if is_already_exist_in_database(db, "username", form_data.username):
        return False
    user_table_row.username = form_data.username
    user_table_row.hashed_password = get_password_hash(form_data.password)
    user_table_row.first_name = form_data.first_name
    user_table_row.last_name = form_data.last_name
    user_table_row.is_active = form_data.is_active
    db.add(user_table_row)
    db.commit()
    return True
