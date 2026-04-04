from pydantic import BaseModel


class Books(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    price: float


class BookUpdate(BaseModel):
    title: str
    author: str
    price: float


class BookStore(BaseModel):
    id : int
    title : str
    author : str
    isbn : str
    price : float


class Student(BaseModel):
    name: str
    age: int
    roll: int

class StudentReturn(BaseModel): # for post and put method we have to use this pydantic model
    name: str
    age: int
    roll: int
