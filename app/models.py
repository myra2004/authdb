from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String(10), nullable=False)
