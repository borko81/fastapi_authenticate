from database import Base
from sqlalchemy import Column, Integer, String, Boolean


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False)
    email = Column(String(32), nullable=False, unique=True)
    password = Column(String(52), nullable=False)
    active = Column(Boolean, default=True)
