from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class TodoDB(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)
    task = Column(String(50))
    finished = Column(Boolean, default=False)

    class Config:
        orm_mode = True
