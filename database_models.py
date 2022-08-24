from sqlalchemy import Column, String, Integer, Boolean

from database import Base


class Todo(Base):
    __tablename__ = "todo"
    Id = Column(Integer, primary_key=True, index=True)
    Title = Column(String)
    Description = Column(String)
    Priority = Column(Integer)
    Complete = Column(Boolean, default=False)
