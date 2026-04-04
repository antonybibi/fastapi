from sqlalchemy import Column, Integer, String, Float
from database import Base
from pydantic import BaseModel


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    author = Column(String(255))
    isbn = Column(String(100), unique=True, index=True)
    price = Column(Float)



