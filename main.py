from fastapi import FastAPI

from db import database_models
from db.database import engine
from routers import auth, signup, todos

app = FastAPI()
database_models.Base.metadata.create_all(engine)
app.include_router(signup.router)
app.include_router(auth.router)
app.include_router(todos.router)
